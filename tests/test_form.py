#!/usr/bin/env python

"""Tests for `form` package."""

from questions import form
from questions import questions
from questions import TextValidator


def test_initialize():
    test_form = form.Form(name="testing", param1=0)
    assert test_form.name == "testing"
    assert "param1" in test_form.params


def test_initialize_no_name():
    test_form = form.Form()
    assert test_form.name == "Form"


def test_call():
    test_form = form.Form()
    assert test_form() == test_form.render_html()


def test_construct_survey():
    class TestForm(form.Form):
        text1 = questions.TextQuestion()

    test_form = TestForm(name="testing")
    survey = test_form._construct_survey()
    assert isinstance(survey, questions.Survey)
    assert "text1" in test_form._form_elements


def test_construct_survey_with_extra_js():
    class TestForm(form.Form):
        text1 = questions.Select2Question()

    test_form = TestForm(name="testing")
    survey = test_form._construct_survey()
    assert isinstance(survey, questions.Survey)
    assert "text1" in test_form._form_elements
    assert "select2.min.js" in test_form.extra_js[0]


def test_construct_survey_with_extra_css():
    class TestForm(form.Form):
        text1 = questions.TagBoxQuestion()

    test_form = TestForm(name="testing")
    survey = test_form._construct_survey()
    assert isinstance(survey, questions.Survey)
    assert "text1" in test_form._form_elements
    assert "select2.min.css" in test_form.extra_css[0]


def test_construct_survey_no_questions_elements():
    class TestForm(form.Form):
        text1 = "just text"

    test_form = TestForm(name="testing")
    survey = test_form._construct_survey()
    assert isinstance(survey, questions.Survey)
    assert test_form._form_elements == {}


def test_construct_survey_with_pages():
    class PageForm(form.Form):
        text1 = questions.TextQuestion()

    class TestForm(form.Form):
        page1 = form.FormPage(PageForm, name="Page1")

    test_form = TestForm(name="testing")
    survey = test_form._construct_survey()
    assert survey.pages[1].name == "Page1"
    assert survey.pages[1].questions[0].name == "text1"


def test_construct_survey_with_pages_no_page_name():
    class PageForm(form.Form):
        text1 = questions.TextQuestion()

    class TestForm(form.Form):
        page1 = form.FormPage(PageForm)

    test_form = TestForm(name="testing")
    survey = test_form._construct_survey()
    assert survey.pages[1].name == "PageForm"
    assert survey.pages[1].questions[0].name == "text1"


def test_construct_survey_with_second_level_panel():
    class PanelForm(form.Form):
        text1 = questions.TextQuestion()

    class PageForm(form.Form):
        panel1 = form.FormPanel(PanelForm, name="Panel1")

    class TestForm(form.Form):
        page1 = form.FormPage(PageForm)

    test_form = TestForm(name="testing")
    survey = test_form._construct_survey()
    assert survey.pages[1].name == "PageForm"
    assert survey.pages[1].questions[0].name == "Panel1"
    assert survey.pages[1].questions[0].elements[0].name == "text1"


def test_construct_survey_with_second_level_panel_no_name():
    class PanelForm(form.Form):
        text1 = questions.TextQuestion()

    class PageForm(form.Form):
        panel1 = form.FormPanel(PanelForm)

    class TestForm(form.Form):
        page1 = form.FormPage(PageForm)

    test_form = TestForm(name="testing")
    survey = test_form._construct_survey()
    assert survey.pages[1].name == "PageForm"
    assert survey.pages[1].questions[0].name == "PanelForm"
    assert survey.pages[1].questions[0].elements[0].name == "text1"


def test_construct_survey_with_second_level_panel_dynamic():
    class PanelForm(form.Form):
        text1 = questions.TextQuestion()

    class PageForm(form.Form):
        panel1 = form.FormPanel(PanelForm, name="Panel1", dynamic=True)

    class TestForm(form.Form):
        page1 = form.FormPage(PageForm)

    test_form = TestForm(name="testing")
    survey = test_form._construct_survey()
    assert survey.pages[1].name == "PageForm"
    assert survey.pages[1].questions[0].name == "Panel1"
    assert survey.pages[1].questions[0].template_elements[0].name == "text1"


def test_validate_no_validators():
    class TestForm(form.Form):
        text1 = questions.TextQuestion()

    test_form = TestForm(name="testing")
    form_data = {}
    assert test_form.validate(form_data) is True


def test_validate_required_valid():
    class TestForm(form.Form):
        text1 = questions.TextQuestion(is_required=True)

    test_form = TestForm(name="testing")
    form_data = {"text1": "hello"}
    assert test_form.validate(form_data) is True


def test_validate_required_invalid():
    class TestForm(form.Form):
        text1 = questions.TextQuestion(is_required=True)

    test_form = TestForm(name="testing")
    form_data = {}
    assert test_form.validate(form_data) is False


def test_validate_with_validators_valid():
    text_validator = TextValidator(min_length=5)

    class TestForm(form.Form):
        text1 = questions.TextQuestion(validators=[text_validator])

    test_form = TestForm(name="testing")
    form_data = {"text1": "hello is enough"}
    assert test_form.validate(form_data) is True
    assert "__errors__" not in form_data


def test_validate_with_validators_invalid_with_set_errors():
    text_validator = TextValidator(min_length=5)

    class TestForm(form.Form):
        text1 = questions.TextQuestion(validators=[text_validator])

    test_form = TestForm(name="testing")
    form_data = {"text1": "Bye"}
    assert test_form.validate(form_data, set_errors=True) is False
    assert form_data["__errors__"][0]["question"] == "text1"
