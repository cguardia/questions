"""
Console scripts for questions.

 - list_resources PLATFORM THEME [--include-widgets]
     Lists all CSS and JS resources needed to run SurveyJS

 - download_surveyjs PATH PLATFORM THEME
     Downloads all CSS and JS resources needed to run SurveyJS
"""
import click
import json
import requests

from .form import Form
from .form import FormPage
from .form import FormPanel
from .questions import Question
from .questions import QUESTION_TYPES
from .settings import SURVEY_JS_CDN
from .templates import get_platform_js_resources
from .templates import get_theme_css_resources


@click.command()
@click.argument("path", type=click.Path(exists=True))
@click.argument("platform")
@click.argument("theme")
def download_surveyjs(path, platform, theme):
    """
    Download SurveyJS files to specified location.

    Supplied path must exist.

    Platforms are: angular, jquery, knockout, react, vue.

    Themes are: default, bootstrap, darkblue, darkrose, modern, orange, stone
                winter, winterstone.
    """
    click.echo()
    js = get_platform_js_resources(platform=platform, resource_url=SURVEY_JS_CDN)
    css = get_theme_css_resources(theme=theme, resource_url=SURVEY_JS_CDN)
    widgets_js = set()
    widgets_css = set()
    for question in QUESTION_TYPES:
        extra_js = question.__fields__.get("extra_js").get_default()
        widgets_js.update(extra_js)
        extra_css = question.__fields__.get("extra_css").get_default()
        widgets_css.update(extra_css)
    for url in js + css + list(widgets_js) + list(widgets_css):
        resource = requests.get(url, allow_redirects=True)
        filename = path + "/" + resource.url.split("/")[-1]
        with open(filename, "wb") as downloaded:
            downloaded.write(resource.content)
            click.echo(f"Downloaded {filename}")
    click.echo()


@click.command()
@click.argument("platform")
@click.argument("theme")
@click.option(
    "--include-widgets", default=False, help="include widget resources", is_flag=True
)
def list_resources(platform, theme, include_widgets):
    """
    List required resources for a platform and theme.

    Platforms are: angular, jquery, knockout, react, vue.

    Themes are: default, bootstrap, darkblue, darkrose, modern, orange, stone
                winter, winterstone.
    """
    click.echo()
    js = get_platform_js_resources(platform=platform, resource_url=SURVEY_JS_CDN)
    css = get_theme_css_resources(theme=theme, resource_url=SURVEY_JS_CDN)
    click.echo("Required Javascript resources:")
    for url in js:
        click.echo(f"    {url}")
    if include_widgets:
        click.echo()
        click.echo("Widget specific Javascript resources:")
        for question in QUESTION_TYPES:
            extra_js = question.__fields__.get("extra_js").get_default()
            if extra_js:
                click.echo()
                click.echo(f"{question.__name__}:")
                for url in extra_js:
                    click.echo(f"    {url}")
        click.echo()
    click.echo()
    click.echo("Required CSS resources:")
    for url in css:
        click.echo(f"    {url}")
    if include_widgets:
        click.echo()
        click.echo("Widget specific CSS resources:")
        for question in QUESTION_TYPES:
            extra_css = question.__fields__.get("extra_css").get_default()
            if extra_css:
                click.echo()
                click.echo(f"{question.__name__}:")
                for url in extra_css:
                    click.echo(f"    {url}")
    click.echo()


@click.command()
@click.argument("name")
@click.argument("json_file", type=click.File("r"))
def generate_code(name, json_file):
    """
    Generate Questions form code from SurveyJS JSON file.
    """
    imports = ["from questions import Form"]
    code = []
    NewForm = Form.from_json(json_file.read(), name)
    current = [NewForm]
    while current != []:
        fragment = []
        next_batch = []
        for member in current:
            fragment.append(f"\n\nclass {member.__name__}(Form):\n")
            for element_name, element in member.__dict__.items():
                if isinstance(element, (FormPage, FormPanel)):
                    next_batch.append(element.form.__class__)
                if isinstance(element, (FormPage, FormPanel, Question)):
                    statement = f"from questions import {element.__class__.__name__}"
                    if statement not in imports:
                        imports.append(statement)
                if element_name.startswith("_"):
                    continue
                element_repr = repr(element)
                element_repr = element_repr.replace(": false,", ": False,")
                element_repr = element_repr.replace(": true,", ": True,")
                element_repr = element_repr.replace(": false}", ": False}")
                element_repr = element_repr.replace(": true}", ": True}")
                fragment.append(f"    {element_name} = {element_repr}\n")
        code.append(fragment)
        current = next_batch
    click.echo()
    for statement in imports:
        click.echo(statement)
    code.reverse()
    for fragment in code:
        click.echo("".join(fragment))
