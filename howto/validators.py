import regex
from prompt_toolkit.validation import Validator, ValidationError

class PhoneNumberValidator(Validator):
    def validate(self, document):
        ok = regex.match(
            "^([01]{1})?[-.\s]?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})\s?((?:#|ext\.?\s?|x\.?\s?){1}(?:\d+)?)?$",
            document.text,
        )
        if not ok:
            raise ValidationError(
                message="Please enter a valid phone number",
                cursor_position=len(document.text),
            )  # Move cursor to end


class NumberValidator(Validator):
    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(
                message="Please enter a number", cursor_position=len(document.text)
            )  # Move cursor to end


class NotEmpty(Validator):
    def validate(self, document):
        if not document.text:
            raise ValidationError(
                message="Please enter something", cursor_position=len(document.text)
            )  # Move cursor to end
