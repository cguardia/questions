from typing import Type

try:
    from typing import Literal
except ImportError:
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


class Form(object):
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

    def __call__(self):
        return self.render_html()

    def _construct_survey(self):
        self._extra_js = []
        self._extra_css = []
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
                    if element.extra_js != []:
                        for js in element.extra_js:
                            if js not in extra_js and js not in self._extra_js and js not in self.required_js:
                                extra_js.append(js)
                    if element.extra_css != []:
                        for css in element.extra_css:
                            if css not in extra_css and css not in self._extra_css and css not in self.required_css:
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

    def render_js(self):
        return get_survey_js(self.to_json(), self.action, self.theme, self.platform)

    def render_html(self, title=None):
        if title is None:
            title = self.params.get("title", self.name)
        return get_form_page(title, self.platform, self.render_js(), self.js, self.css)


class FormPage(object):
    def __init__(self, form: Type[Form], name: str = "", **params):
        self.form = form()
        if name == "":
            name = self.__class__.__name__
        self.name = name
        self.dynamic = False
        self.params = params


class FormPanel(object):
    def __init__(
        self,
        form: Type[Form],
        name: str = "",
        dynamic: bool = False,
        **params,
    ):
        self.form = form()
        if name == "":
            name = self.__class__.__name__
        self.name = name
        self.dynamic = dynamic
        self.params = params
