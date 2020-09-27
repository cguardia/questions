#!/usr/bin/env python

"""Tests for `templates` package."""

from questions import templates
from questions.settings import BOOTSTRAP_URL
from questions.settings import SURVEY_JS_CDN


def test_get_platform_js_resources():
    js = templates.get_platform_js_resources("jquery", SURVEY_JS_CDN)
    assert f"{SURVEY_JS_CDN}/survey.jquery.min.js" in js
    js = templates.get_platform_js_resources("jquery", "http://testing")
    assert "http://testing/survey.jquery.min.js" in js


def test_get_theme_css_resources():
    css = templates.get_theme_css_resources("default", SURVEY_JS_CDN)
    assert f"{SURVEY_JS_CDN}/survey.css" in css
    css = templates.get_theme_css_resources("bootstrap", SURVEY_JS_CDN)
    assert BOOTSTRAP_URL in css
    css = templates.get_theme_css_resources("default", "http://testing")
    assert "http://testing/survey.css" in css
    css = templates.get_theme_css_resources("modern", "http://testing")
    assert "http://testing/modern.css" in css
    css = templates.get_theme_css_resources("bootstrap", "http://testing")
    assert "http://testing/bootstrap.min.css" in css


def test_get_survey_js():
    survey_js = templates.get_survey_js(
        "FORM_JSON", "FORM_DATA", "id", "http://testing", "default", "jquery"
    )
    assert "FORM_JSON" in survey_js
    assert "FORM_DATA" in survey_js
    assert "http://testing" in survey_js
    assert "default" in survey_js
    assert templates.PLATFORM_JS["jquery"].format("id") in survey_js


def test_get_survey_js_form_data_is_none():
    survey_js = templates.get_survey_js(
        "FORM_JSON", None, "id", "http://testing", "default", "jquery"
    )
    assert "FORM_JSON" in survey_js
    assert "http://testing" in survey_js
    assert "default" in survey_js
    assert templates.PLATFORM_JS["jquery"].format("id") in survey_js


def test_get_form_page():
    html = templates.get_form_page(
        "Title", "id", "jquery", "GENERATED_JS", ["file.js"], ["file.css"]
    )
    assert "Title" in html
    assert "GENERATED_JS" in html
    assert "file.js" in html
    assert "file.css" in html
