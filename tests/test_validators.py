#!/usr/bin/env python

"""Tests for `validators` package."""

from questions import validators


def test_text_validator_bad_min_length():
    validator_data = {"min_length": "7"}
    assert validators.text_validator(validator_data, "hello", {}) is False
    assert validators.text_validator(validator_data, "goodbye", {}) is True


def test_text_validator_bad_max_length():
    validator_data = {"max_length": "4"}
    assert validators.text_validator(validator_data, "hello", {}) is False
    assert validators.text_validator(validator_data, "Bye", {}) is True


def test_text_validator_allow_digits():
    validator_data = {"allow_digits": False}
    assert validators.text_validator(validator_data, "h4ll0", {}) is False
    validator_data = {"allow_digits": True}
    assert validators.text_validator(validator_data, "h4ll0", {}) is True


def test_number_validator_bad_min_value():
    validator_data = {"min_value": 7}
    assert validators.number_validator(validator_data, 5, {}) is False
    assert validators.number_validator(validator_data, 45, {}) is True


def test_number_validator_bad_max_value():
    validator_data = {"max_value": 42}
    assert validators.number_validator(validator_data, 99, {}) is False
    assert validators.number_validator(validator_data, 22, {}) is True


def test_email_validator():
    assert validators.email_validator({}, "my.bad.address.com", {}) is False
    assert validators.email_validator({}, "my@true.email.com", {}) is True


def test_regex_validator():
    validator_data = {"regex": "[A-Z][a-z]+-[0-9][0-9]"}
    assert validators.regex_validator(validator_data, "anything", {}) is False
    assert validators.regex_validator(validator_data, "Abc-55", {}) is True


def test_expression_validator():
    validator_data = {"expression": "{var2} notempty and {var3} > 5"}
    form_data = {"var1": "something", "var2": "", "var3": 1}
    assert (
        validators.expression_validator(validator_data, "anything", form_data) is False
    )
    assert validators.expression_validator(validator_data, "anything", {}) is False
    form_data = {"var1": "something", "var2": "other", "var3": 8}
    assert (
        validators.expression_validator(validator_data, "anything", form_data) is True
    )
    validator_data = {"expression": ""}
    assert (
        validators.expression_validator(validator_data, "anything", form_data) is True
    )


def test_call_validator():
    validator_data = {"type": "text"}
    validators.call_validator(validator_data, "anything", {})
