from typing import Type

try:
    from typing import Literal
except ImportError:  # pragma: NO COVER
    from typing_extensions import Literal

from .questions import Page
from .questions import PanelBlock
from .questions import PanelDynamicBlock
from .questions import Question
from .questions import Survey
from .settings import INCLUDE_KEYS
from .settings import SURVEY_JS_CDN
from .settings import SURVEY_JS_PLATFORMS
from .settings import SURVEY_JS_THEMES
from .templates import SURVEY_JS
from .templates import SURVEY_HTML
from .templates import get_form_page
from .templates import get_platform_js_resources
from .templates import get_survey_js
from .templates import get_theme_css_resources
from .validators import call_validator


class Form(object):
    """
    This is the base class used for creating user-defined forms. In addition to
    setting up the form configuration and performing validation, it generates
    the SurveyJS form JSON and keeps track of the required Javascript and CSS
    resources.
    """

    def __init__(
        self,
        name: str = "",
        method: Literal[("GET", "POST")] = "POST",
        action: str = "",
        theme: Literal[SURVEY_JS_THEMES] = "default",
        platform: Literal[SURVEY_JS_PLATFORMS] = "jquery",
        resource_url: str = SURVEY_JS_CDN,
        **params,
    ):
        if name == "":
            name = self.__class__.__name__
        self.name = name
        self.theme = theme
        self.method = method
        self.action = action
        self.platform = platform
        self.resource_url = resource_url
        self.params = params
        self._extra_js = []
        self._extra_css = []
        self._form_elements = {}

    def __call__(self):
        return self.render_html()

    def _construct_survey(self):
        self._extra_js = []
        self._extra_css = []
        self._form_elements = {}
        default_page = Page(name="default")
        survey = Survey(**self.params)
        survey.pages.append(default_page)
        self._add_elements(survey, self, top_level=True)
        return survey

    def _add_elements(self, survey, form, top_level=False, container_name="questions"):
        extra_js = []
        extra_css = []
        for element_name, element in form.__class__.__dict__.items():
            if isinstance(element, (FormPage, FormPanel, Question)):
                name = getattr(element, "name", "")
                if name == "":
                    element.name = element_name
                if isinstance(element, FormPage) and top_level:
                    page = Page(name=name, **element.params)
                    self._add_elements(page, element.form)
                    survey.pages.append(page)
                elif isinstance(element, (FormPage, FormPanel)):
                    container = getattr(survey, container_name)
                    if element.dynamic:
                        panel = PanelDynamicBlock(name=name, **element.params)
                        container_name = "template_elements"
                    else:
                        panel = PanelBlock(name=name, **element.params)
                        container_name = "elements"
                    self._add_elements(
                        panel, element.form, container_name=container_name
                    )
                    container.append(panel)
                else:
                    self._form_elements[element.name] = element
                    if element.extra_js != []:
                        for js in element.extra_js:
                            if (
                                js not in extra_js
                                and js not in self._extra_js
                                and js not in self.required_js
                            ):
                                extra_js.append(js)
                    if element.extra_css != []:
                        for css in element.extra_css:
                            if (
                                css not in extra_css
                                and css not in self._extra_css
                                and css not in self.required_css
                            ):
                                extra_css.append(css)
                    if top_level:
                        container = survey.pages[0].questions
                    else:
                        container = getattr(survey, container_name)
                    container.append(element)
        if extra_js != []:
            survey_widgets = f"{self.resource_url}/surveyjs-widgets.js"
            if survey_widgets not in self._extra_js:
                extra_js.append(survey_widgets)
        self._extra_js = self._extra_js + extra_js
        self._extra_css = self._extra_css + extra_css

    @property
    def extra_js(self):
        self._construct_survey()
        return self._extra_js

    @property
    def extra_css(self):
        self._construct_survey()
        return self._extra_css

    @property
    def required_js(self):
        return get_platform_js_resources(self.platform, self.resource_url)

    @property
    def required_css(self):
        return get_theme_css_resources(self.theme, self.resource_url)

    @property
    def js(self):
        return self.required_js + self.extra_js

    @property
    def css(self):
        return self.required_css + self.extra_css

    def to_json(self):
        survey = self._construct_survey()
        return survey.json(by_alias=True, include=INCLUDE_KEYS)

    def render_js(self, form_data=None):
        return get_survey_js(
            self.to_json(), form_data, self.action, self.theme, self.platform
        )

    def render_html(self, title=None, form_data=None):
        if title is None:
            title = self.params.get("title", self.name)
        if form_data is None:
            form_data = {}
        survey_js = self.render_js(form_data=form_data)
        return get_form_page(title, self.platform, survey_js, self.js, self.css)

    def validate(self, form_data):
        """
        Server side validation mimics what client side validation should do. This
        means that any validation errors here are due to form data being sent from
        outside the SurveyJS form, possibly by directly posting the data to the form.
        Questions keeps track of the errors, even though the UI will show them anyway.
        Validation returns False if at least one validator doesn't pass.
        """
        validated = True
        errors = []
        self._construct_survey()
        for name, element in self._form_elements.items():
            value = form_data.get(name)
            if value is None and element.is_required:
                errors.append({"question": name, "message": "An answer is required"})
                validated = False
            for validator_data in element.validators:
                if not call_validator(validator_data, value, form_data):
                    errors.append(
                        {"question": name, "message": validator_data["message"]}
                    )
                    validated = False
        form_data["__errors__"] = errors
        return validated


class FormPage(object):
    """
    Represents an individual page from a multi-page form.
    """

    def __init__(self, form: Type[Form], name: str = "", **params):
        self.form = form()
        if name == "":
            name = self.form.name
        self.name = name
        self.dynamic = False
        self.params = params


class FormPanel(object):
    """
    A panel is a set of fields that go together. It can be used for visual
    separation, or as a dinamically added group of fields for complex questions.
    """

    def __init__(
        self,
        form: Type[Form],
        name: str = "",
        dynamic: bool = False,
        **params,
    ):
        self.form = form()
        if name == "":
            name = self.form.name
        self.name = name
        self.dynamic = dynamic
        self.params = params
