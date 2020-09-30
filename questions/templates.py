import json
from typing import Any
from typing import Dict
from typing import List

from jinja2 import Environment
from jinja2 import PackageLoader
from jinja2 import select_autoescape

from .settings import BOOTSTRAP_URL
from .settings import SUGGESTED_JS_BY_PLATFORM
from .settings import SURVEY_JS_CDN


# Initialize Jinja environment
env = Environment(
    loader=PackageLoader("questions", "templates"),
    autoescape=select_autoescape(["html", "xml"]),
)


def _render_template(
    kind: str = "js",
    platform: str = "jquery",
    **context_data: Dict,
):
    filename = f"survey_{kind}.{platform}.jinja"
    template = env.get_template(filename)
    return template.render(**context_data)


def get_platform_js_resources(
    platform: str = "jquery",
    resource_url: str = SURVEY_JS_CDN,
):
    """
    Get the list of suggested JS resources for a platform. if not using the
    CDN, only the main SurveyJS JS file is returned.

    :param platform:
        The name of the JS platform.
    :param resource_url:
        The URL where all SurveyJS resources are located.

    :Returns:
        The list of resource URLs.
    """
    survey_js = f"{resource_url}/survey.{platform}.min.js"
    platform_js = []
    for js in SUGGESTED_JS_BY_PLATFORM[platform]:
        if resource_url == SURVEY_JS_CDN:
            platform_js.append(js)
        else:
            filename = js.split("/")[-1]
            platform_js.append(f"{resource_url}/{filename}")
    platform_js.append(survey_js)
    return platform_js


def get_theme_css_resources(
    theme: str = "default",
    resource_url: str = SURVEY_JS_CDN,
):
    """
    Get the list of suggested CSS resources for a theme. if not using the
    CDN, only the main SurveyJS CSS file is returned.

    :param theme:
        The name of the CSS theme.
    :param resource_url:
        The URL where all SurveyJS resources are located.

    :Returns:
        The list of resource URLs.
    """
    if theme == "bootstrap" and resource_url == SURVEY_JS_CDN:
        return [BOOTSTRAP_URL]
    elif theme == "bootstrap":
        return [f"{resource_url}/bootstrap.min.css"]
    name = "survey"
    if theme == "modern":
        name = "modern"
    return [f"{resource_url}/{name}.css"]


def get_survey_js(
    form_json: str = "",
    form_data: Dict[str, Any] = None,
    html_id: str = "questions_form",
    action: str = "",
    theme: str = "default",
    platform: str = "jquery",
):
    """
    Get the SurveyJS initialization script and form definition.

    :param form_json:
        The JSON generated from the questions form.
    :param form_data:
        Any form data to set on the rendered form.
    :param html_id:
        The HTML id of the form placeholder.
    :param action:
        The URL where the submitted form data will be posted.
    :param theme:
        The name of the SurveyJS theme to use.
    :param platform:
        The name of the supported SurveyJS platform to use.

    :Returns:
        The rendered JS as string.
    """
    if form_data is None:
        form_data = {}
    data = json.dumps(form_data)
    return _render_template(
        kind="js",
        platform=platform,
        theme=theme,
        json=form_json,
        data=data,
        action=action,
        html_id=html_id,
    )


def get_form_page(
    title: str = "",
    html_id: str = "questions_form",
    platform: str = "jquery",
    survey_js: str = "",
    js_resources: List = None,
    css_resources: List = None,
):
    """
    Generate a standalone SurveyJS HTML page.

    :param title:
        The form title to display.
    :param html_id:
        The HTML id of the form placeholder.
    :param platform:
        The name of the supported SurveyJS platform to use.
    :param survey_js:
        The generated JS to put in the form.
    :param js_resources:
        The list of JS resources to add to the HTMl head.
    :param css_resources:
        The list of CSS resources to add to the HTMl head.

    :Returns:
        The rendered HTML as string.
    """
    resources = ""
    if js_resources is None:
        js_resources = []
    if css_resources is None:
        css_resources = []
    for resource in js_resources:
        resources += f'<script src="{resource}"></script>\n'
    for resource in css_resources:
        resources += f'<link href="{resource}" type="text/css" rel="stylesheet" />\n'
    return _render_template(
        kind="html",
        platform=platform,
        title=title,
        resources=resources,
        html_id=html_id,
        survey_js=survey_js,
    )
