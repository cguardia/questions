import re
from typing import Any
from typing import Dict

from email_validator import EmailNotValidError
from email_validator import validate_email
from simpleeval import EvalWithCompoundTypes as Evaluator
from simpleeval import InvalidExpression

from .questions import Validator


class ValidationError(Exception):
    """
    Validation error exception, for use by Form.update_object.
    """


def text_validator(validator: Validator, value: Any, form_data: Dict[str, Any]):
    """Validate length of a text value, and whether digits are allowed.

    :param validator:
        The validator instance for the current question.
    :param value:
        The value to be validated.
    :param form_data:
        The dictionary containing from data entered for current form.

    :Returns:
        If validation passes, :data:`True`, else :data:`False`.
    """
    max_length = int(validator.max_length)
    min_length = int(validator.min_length)
    allow_digits = validator.allow_digits
    result = True
    value = str(value)
    length = len(value)
    if length < min_length or max_length > 0 and length > max_length:
        result = False
    if not allow_digits:
        for number in range(10):
            if str(number) in value:
                result = False
    return result


def numeric_validator(validator: Validator, value: Any, form_data: Dict[str, Any]):
    """Validate if number value is within set limits.

    :param validator:
        The validator instance for the current question.
    :param value:
        The value to be validated.
    :param form_data:
        The dictionary containing from data entered for current form.

    :Returns:
        If validation passes, :data:`True`, else :data:`False`.
    """
    max_value = float(validator.max_value)
    min_value = float(validator.min_value)
    result = True
    value = float(value)
    if value < min_value or max_value > 0 and value > max_value:
        result = False
    return result


def email_validator(validator: Validator, value: Any, form_data: Dict[str, Any]):
    """Validate if value is a valid email address.

    :param validator:
        The validator instance for the current question.
    :param value:
        The value to be validated.
    :param form_data:
        The dictionary containing from data entered for current form.

    :Returns:
        If validation passes, :data:`True`, else :data:`False`.
    """
    result = True
    try:
        validate_email(value)
    except EmailNotValidError:
        result = False
    return result


def regex_validator(validator: Validator, value: Any, form_data: Dict[str, Any]):
    """Validate if value matches regular expression.

    :param validator:
        The validator instance for the current question.
    :param value:
        The value to be validated.
    :param form_data:
        The dictionary containing from data entered for current form.

    :Returns:
        If validation passes, :data:`True`, else :data:`False`.
    """
    regex = validator.regex
    regex = re.compile(regex)
    return regex.match(value) is not None


def expression_validator(validator: Validator, value: Any, form_data: Dict[str, Any]):
    """Validate if expression associated with value is true.

    :param validator:
        The validator instance for the current question.
    :param value:
        The value to be validated.
    :param form_data:
        The dictionary containing from data entered for current form.

    :Returns:
        If validation passes, :data:`True`, else :data:`False`.
    """
    expression = validator.expression
    result = True
    if expression:
        expression = expression.replace("{", "").replace("}", "")
        expression = expression.replace(" empty", " in [[], {}]")
        expression = expression.replace(" notempty", " not in [[], {}]")
        expression = expression.replace(" anyof ", " in ")
        try:
            evaluator = Evaluator(names=form_data)
            result = evaluator.eval(expression) is True
        except (ValueError, TypeError, SyntaxError, KeyError, InvalidExpression):
            result = False
    return result


VALIDATORS = {
    "text": text_validator,
    "numeric": numeric_validator,
    "email": email_validator,
    "regex": regex_validator,
    "expression": expression_validator,
}


def call_validator(validator: Validator, value: Any, form_data: Dict[str, Any]):
    """Call correct validation method depending on validator type.

    :param validator:
        The validator instance for the current question.
    :param value:
        The value to be validated.
    :param form_data:
        The dictionary containing from data entered for current form.

    :Returns:
        If validation passes, :data:`True`, else :data:`False`.
    """
    validator_method = VALIDATORS[validator.kind]
    return validator_method(validator, value, form_data)
