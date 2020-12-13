import json
import re

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
from .questions import QUESTION_NAMES_TO_TYPES
from .questions import Survey
from .settings import INCLUDE_KEYS
from .settings import SURVEY_JS_CDN
from .settings import SURVEY_JS_PLATFORMS
from .settings import SURVEY_JS_THEMES
from .settings import SURVEY_JS_WIDGETS
from .templates import get_form_page
from .templates import get_platform_js_resources
from .templates import get_survey_js
from .templates import get_theme_css_resources
from .utils import get_params_for_repr
from .validators import call_validator
from .validators import ValidationError


RENAMED_FIELDS = {
    "type": "kind",
    "isAllRowRequired": "all_rows_required",
    "format": "expression_format",
    "max": "max_value",
    "min": "min_value",
    "isRequired": "required",
}


def to_camel_case(name):
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


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

    questions_resource_url = SURVEY_JS_CDN

    default_params = {}

    @classmethod
    def set_resource_url(cls, url: str):
        cls.questions_resource_url = url

    def __init__(
        self,
        name: str = "",
        action: str = "",
        html_id: str = "questions_form",
        theme: Literal[SURVEY_JS_THEMES] = "default",
        platform: Literal[SURVEY_JS_PLATFORMS] = "jquery",
        resource_url: str = None,
        **params,
    ):
        if name == "":
            name = self.__class__.__name__
        self.name = name
        self.action = action
        self.html_id = html_id
        self.theme = theme
        self.platform = platform
        if resource_url is None:
            resource_url = self.questions_resource_url
        self.resource_url = resource_url
        self.params = self.default_params.copy()
        self.params.update(params)
        self._extra_js = []
        self._extra_css = []
        self._form_elements = {}

    def __call__(self, form_data=None):
        return self.render_html(form_data=form_data)

    def __repr__(self):
        class_name = self.__class__.__name__
        class_name = class_name[0].upper() + class_name[1:]
        form_repr = f'{class_name}(\n        name="{self.name}"'
        if self.params:
            params = get_params_for_repr(self.params)
            form_repr += f",{params}"
        form_repr += "\n    )"
        return form_repr

    @classmethod
    def from_json(
        cls,
        form_json: str,
        name: str,
    ):
        """
        Generate a Form class definition from properly formatted JSON data. The
        The generated form class can then be instantiated as needed.

        :param form_json:
            A well formed JSON string with a SurveyJS definition.
        :param name:
            The name of the generated class.

        :Returns:
            A new Python Type that is a subclass of Form.
        """
        NewForm = type(name, (cls,), {})
        form_json = json.loads(form_json)
        elements = form_json.items()
        cls._add_type_elements(NewForm, elements)
        return NewForm

    @classmethod
    def _add_type_elements(cls, NewForm, elements):
        """
        Recursively go through the JSON elements to add all specified form
        elements to the passed in Type.
        """
        for name, element in elements:
            if name == "pages":
                for page in element:
                    page_title = page.get("title", "Page")
                    page_name = page.get("name", page_title)
                    page_name = page_name[0].upper() + page_name[1:]
                    NewPage = type(page_name, (cls,), {})
                    page_items = {}
                    page_params = {}
                    for key, value in page.items():
                        if key in ["questions", "elements", "templateElements"]:
                            page_items[key] = value
                        else:
                            if key in RENAMED_FIELDS:
                                new_key = RENAMED_FIELDS[key]
                            else:
                                new_key = to_camel_case(key)
                            page_params[new_key] = value
                    if "name" in page_params:
                        del page_params["name"]
                    if page_items:
                        cls._add_type_elements(NewPage, page_items.items())
                    form_page = FormPage(NewPage, name=page_name, **page_params)
                    setattr(NewForm, page_name, form_page)
            elif name in ["questions", "elements", "templateElements"]:
                for question_element in element:
                    if question_element["type"] in QUESTION_NAMES_TO_TYPES:
                        question_params = {}
                        for key, value in question_element.items():
                            if key in RENAMED_FIELDS:
                                new_key = RENAMED_FIELDS[key]
                            else:
                                new_key = to_camel_case(key)
                            question_params[new_key] = value
                        new_element = QUESTION_NAMES_TO_TYPES[question_element["type"]](
                            **question_params
                        )
                        setattr(NewForm, new_element.name, new_element)
                    elif question_element["type"] in ["panel", "paneldynamic"]:
                        panel_title = question_element.get("title", "Panel")
                        panel_name = question_element.get("name", panel_title)
                        panel_name = panel_name[0].upper() + panel_name[1:]
                        Panel = type(panel_name, (cls,), {})
                        dynamic = question_element["type"] == "paneldynamic"
                        panel_items = {}
                        panel_params = {}
                        for key, value in question_element.items():
                            if key in ["questions", "elements", "templateElements"]:
                                panel_items[key] = value
                            else:
                                if key in RENAMED_FIELDS:
                                    new_key = RENAMED_FIELDS[key]
                                else:
                                    new_key = to_camel_case(key)
                                panel_params[new_key] = value
                        if "name" in panel_params:
                            del panel_params["name"]
                        if panel_items:
                            cls._add_type_elements(Panel, panel_items.items())
                        form_panel = FormPanel(
                            Panel, name=panel_name, dynamic=dynamic, **panel_params
                        )
                        setattr(NewForm, panel_name, form_panel)
            else:
                NewForm.default_params[name] = element

    def _construct_survey(self):
        """
        Goes through all the form elements and creates a Survey object, which will
        be used to generate the JSON for initializing SurveyJS. As a side effect,
        populates extra CSS and JS resources. Also keeps a dictionary of all form
        elements, used by validation and update object methods.
        """
        self._extra_js = []
        self._extra_css = []
        self._form_elements = {}
        default_page = Page(name="default")
        survey = Survey(**self.params)
        survey.pages.append(default_page)
        self._add_elements(survey, self, top_level=True)
        # get rid of duplicates
        self._extra_js = list(set(self._extra_js))
        self._extra_css = list(set(self._extra_css))
        if self._extra_js:
            self._extra_js.append(f"{self.resource_url}/{SURVEY_JS_WIDGETS}")
        return survey

    def _add_elements(self, survey, form, top_level=False, container_name="questions"):
        """
        Method to put form elements inside a container. Needs to be recursive so that
        pages and panels are properly nested.
        """
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
                        new_container_name = "template_elements"
                    else:
                        panel = PanelBlock(name=name, **element.params)
                        new_container_name = "elements"
                    self._add_elements(
                        panel, element.form, container_name=new_container_name
                    )
                    container.append(panel)
                else:
                    self._form_elements[element.name] = element
                    if element.extra_js != []:
                        for js in element.extra_js:
                            url = js
                            if self.resource_url != SURVEY_JS_CDN:
                                filename = js.split("/")[-1]
                                url = f"{self.resource_url}/{filename}"
                            if (
                                url not in extra_js
                                and url not in self._extra_js
                                and url not in self.required_js
                            ):
                                extra_js.append(url)
                    if element.extra_css != []:
                        for css in element.extra_css:
                            url = css
                            if self.resource_url != SURVEY_JS_CDN:
                                filename = css.split("/")[-1]
                                url = f"{self.resource_url}/{filename}"
                            if (
                                url not in extra_css
                                and url not in self._extra_css
                                and url not in self.required_css
                            ):
                                extra_css.append(url)
                    if top_level:
                        container = survey.pages[0].questions
                    else:
                        container = getattr(survey, container_name)
                    container.append(element)
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

    def __repr__(self):
        class_name = self.form.__class__.__name__
        class_name = class_name[0].upper() + class_name[1:]
        page_repr = f'FormPage(\n        {class_name},\n        name="{self.name}"'
        if self.params:
            params = get_params_for_repr(self.params)
            page_repr += f",{params}"
        page_repr += "\n    )"
        return page_repr


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

    def __repr__(self):
        class_name = self.form.__class__.__name__
        class_name = class_name[0].upper() + class_name[1:]
        panel_repr = f'FormPanel(\n        {class_name},\n        name="{self.name}",'
        panel_repr += f"\n        dynamic={self.dynamic}"
        if self.params:
            params = get_params_for_repr(self.params)
            panel_repr += f",{params}"
        panel_repr += "\n    )"
        return panel_repr
