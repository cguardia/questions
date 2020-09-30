from typing import Any
from typing import Dict
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
from .templates import get_form_page
from .templates import get_platform_js_resources
from .templates import get_survey_js
from .templates import get_theme_css_resources
from .validators import call_validator
from .validators import ValidationError


class Form(object):
    """
    This is the base class used for creating user-defined forms. In addition to
    setting up the form configuration and performing validation, it generates
    the SurveyJS form JSON and keeps track of the required Javascript and CSS
    resources.

    :param name:
        The name of the form. If empty, the class name is used.
    :param action:
        The URL where the form data will be posted. If empty, the
        same URL for the form is used.
    :param html_id:
        The id for the div element that will be used to render the form.
    :param theme:
        The name of the base theme for the form. Default value is 'default'.
    :param platform:
        The JS platform to use for generating the form. Default value is 'jquery'.
    :param resource_url:
        The base URL for the theme resources. If provided,
        Questions will expect to find all resources under this URL. If
        empty, the SurveyJS CDN will be used for all resources.
    :param params:
        Optional list of parameters to be passed to the SurveyJS form object.
    """

    def __init__(
        self,
        name: str = "",
        action: str = "",
        html_id: str = "questions_form",
        theme: Literal[SURVEY_JS_THEMES] = "default",
        platform: Literal[SURVEY_JS_PLATFORMS] = "jquery",
        resource_url: str = SURVEY_JS_CDN,
        **params,
    ):
        if name == "":
            name = self.__class__.__name__
        self.name = name
        self.action = action
        self.html_id = html_id
        self.theme = theme
        self.platform = platform
        self.resource_url = resource_url
        self.params = params
        self._extra_js = []
        self._extra_css = []
        self._form_elements = {}

    def __call__(self, form_data=None):
        return self.render_html(form_data=form_data)

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
        """
        Any extra JS resources required by the form's question types.
        """
        self._construct_survey()
        return self._extra_js

    @property
    def extra_css(self):
        """
        Any extra CSS resources required by the form's question types.
        """
        self._construct_survey()
        return self._extra_css

    @property
    def required_js(self):
        """
        Required JS resources needed to run SurveyJS on chosen platform.
        """
        return get_platform_js_resources(self.platform, self.resource_url)

    @property
    def required_css(self):
        """
        Required CSS resources needed to run SurveyJS on chosen platform.
        """
        return get_theme_css_resources(self.theme, self.resource_url)

    @property
    def js(self):
        """
        Combined JS resources for this form.
        """
        return self.required_js + self.extra_js

    @property
    def css(self):
        """
        Combined CSS resources for this form.
        """
        return self.required_css + self.extra_css

    def to_json(self):
        """
        Convert the form to JSON, in the SurveyJS format.

        :Returns:
            JSON object with the form definition.
        """
        survey = self._construct_survey()
        return survey.json(by_alias=True, include=INCLUDE_KEYS)

    def render_js(self, form_data: Dict[str, Any] = None):
        """
        Generate the SurveyJS initialization code for the chosen platform.

        :param form_data: answers to show on the form for each
            question (for edit forms).

        :Returns:
            String with the generated javascript.
        """
        return get_survey_js(
            form_json=self.to_json(),
            form_data=form_data,
            html_id=self.html_id,
            action=self.action,
            theme=self.theme,
            platform=self.platform,
        )

    def render_html(self, title: str = None, form_data: Dict[str, Any] = None):
        """
        Render a full HTML page showing this form.

        :param title:
            The form title.
        :param form_data:
            answers to show on the form for each question (for edit forms).

        :Returns:
            String with the generated HTML.
        """
        if title is None:
            title = self.params.get("title", self.name)
        if form_data is None:
            form_data = {}
        survey_js = self.render_js(form_data=form_data)
        return get_form_page(
            title=title,
            html_id=self.html_id,
            platform=self.platform,
            survey_js=survey_js,
            js_resources=self.js,
            css_resources=self.css,
        )

    def validate(self, form_data: Dict[str, Any], set_errors: bool = False):
        """
        Server side validation mimics what client side validation should do. This
        means that any validation errors here are due to form data being sent from
        outside the SurveyJS form, possibly by directly posting the data to the form.
        Questions keeps track of the errors, even though the UI will show them anyway.
        Validation returns False if at least one validator doesn't pass.

        :param form_data:
            A dictionary-like object with the form data to be validated.
        :param set_errors:
            set to :data:`True` to add an `__errors__` key to the
            form data dictionary, containing the validation errors.

        :Returns:
            :data:`True` if the validation passes, :data:`False` otherwise.
        """
        validated = True
        errors = []
        self._construct_survey()
        for name, element in self._form_elements.items():
            value = form_data.get(name)
            if value is None and element.required:
                errors.append({"question": name, "message": "An answer is required"})
                validated = False
            for validator in element.validators:
                if not call_validator(validator, value, form_data):
                    errors.append({"question": name, "message": validator.message})
                    validated = False
        if set_errors:
            form_data["__errors__"] = errors
        return validated

    def update_object(self, obj: Any, form_data: Dict[str, Any]):
        """
        Utility method to set an object's attributes with data obtained from a form.
        This method validates the data before setting the object's attributes.

        :param obj:
            The object to set attributes on.

        :param form_data:
            A dictionary-like object with the form data to be validated.

        :Raises:
            questions.validators.ValidationError if validation does not pass.
        """
        if self.validate(form_data):
            # call to validate sets the form elements beforehand
            for name in self._form_elements.keys():
                setattr(obj, name, form_data[name])
        else:
            raise ValidationError


class FormPage(object):
    """
    Represents an individual page from a multi-page form.

    :param form:
        A subclass of questions.Form (not an instance). The form
        to be shown in its own page.
    :param name:
        The name of the form.
    :param params:
        Optional list of parameters to be passed to the SurveyJS page object.
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
    separation, or as a dynamically added group of fields for complex questions.

    :param form:
        A subclass of questions.Form (not an instance). The form
        to be shown in its own page.
    :param name:
        The name of the form.
    :param dynamic:
        Set to :data:`True` if the panel will be used as a template for adding
         or removing groups of questions.
    :param params:
        Optional list of parameters to be passed to the SurveyJS panel object.
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
