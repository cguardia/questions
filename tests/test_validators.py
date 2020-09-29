#!/usr/bin/env python

"""Tests for `validators` package."""

from questions import validators
from questions import EmailValidator
from questions import ExpressionValidator
from questions import NumericValidator
from questions import RegexValidator
from questions import TextValidator


def test_text_validator_bad_min_length():
    validator = TextValidator(min_length=7)
    assert validators.text_validator(validator, "hello", {}) is False
    assert validators.text_validator(validator, "goodbye", {}) is True


def test_text_validator_bad_max_length():
    validator = TextValidator(max_length=4)
    assert validators.text_validator(validator, "hello", {}) is False
    assert validators.text_validator(validator, "Bye", {}) is True


def test_text_validator_allow_digits():
    validator = TextValidator(allow_digits=False)
    assert validators.text_validator(validator, "h4ll0", {}) is False
    validator = TextValidator(allow_digits=True)
    assert validators.text_validator(validator, "h4ll0", {}) is True


def test_numeric_validator_bad_min_value():
    validator = NumericValidator(min_value=7)
    assert validators.numeric_validator(validator, 5, {}) is False
    assert validators.numeric_validator(validator, 45, {}) is True


def test_numeric_validator_bad_max_value():
    validator = NumericValidator(max_value=42)
    assert validators.numeric_validator(validator, 99, {}) is False
    assert validators.numeric_validator(validator, 22, {}) is True


def test_email_validator():
    validator = EmailValidator()
    assert validators.email_validator(validator, "my.bad.address.com", {}) is False
    assert validators.email_validator(validator, "my@true.email.com", {}) is True


def test_regex_validator():
    validator = RegexValidator(regex="[A-Z][a-z]+-[0-9][0-9]")
    assert validators.regex_validator(validator, "anything", {}) is False
    assert validators.regex_validator(validator, "Abc-55", {}) is True


def test_expression_validator():
    validator = ExpressionValidator(expression="{var2} notempty and {var3} > 5")
    form_data = {"var1": "something", "var2": "", "var3": 1}
    assert validators.expression_validator(validator, "anything", form_data) is False
    assert validators.expression_validator(validator, "anything", {}) is False
    form_data = {"var1": "something", "var2": "other", "var3": 8}
    assert validators.expression_validator(validator, "anything", form_data) is True
    validator = ExpressionValidator(expression="")
    assert validators.expression_validator(validator, "anything", form_data) is True
