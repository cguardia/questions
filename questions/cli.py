"""
Console scripts for questions.

 - list_resources PLATFORM THEME [--include-widgets]
     Lists all CSS and JS resources needed to run SurveyJS

 - download_surveyjs PATH PLATFORM THEME
     Downloads all CSS and JS resources needed to run SurveyJS
"""
import click
import requests

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
