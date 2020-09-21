import re

from email_validator import EmailNotValidError
from email_validator import validate_email
from simpleeval import EvalWithCompoundTypes as Evaluator
from simpleeval import InvalidExpression


def text_validator(validator_data, value, form_data):
    max_length = int(validator_data.get("max_length", "0"))
    min_length = int(validator_data.get("min_length", "0"))
    allow_digits = int(validator_data.get("allow_digits", False))
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


def number_validator(validator_data, value, form_data):
    max_value = float(validator_data.get("max_value", 0))
    min_value = float(validator_data.get("min_value", 0))
    result = True
    value = float(value)
    if value < min_value or max_value > 0 and value > max_value:
        result = False
    return result


def email_validator(validator_data, value, form_data):
    result = True
    try:
        validate_email(value)
    except EmailNotValidError:
        result = False
    return result


def regex_validator(validator_data, value, form_data):
    regex = validator_data["regex"]
    regex = re.compile(regex)
    return regex.match(value) is not None


def expression_validator(validator_data, value, form_data):
    expression = validator_data["expression"]
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
    "number": number_validator,
    "email": email_validator,
    "regex": regex_validator,
    "expression": expression_validator,
}


def call_validator(validator_data, value, form_data):
    validator = VALIDATORS[validator_data["type"]]
    return validator(validator_data, value, form_data)
