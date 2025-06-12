"""Form utilities."""

import logging

from django.forms import Form

from rest_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)


def populate_form_with_drf_errors(form: Form, error: ValidationError) -> None:
    """Populate a Django form with errors from a DRF ValidationError."""
    match error.detail:
        case dict():
            pass
        case _:
            logger.warning("Can't populate form %s with errors", repr(form))
            return
    for field, error_message in error.detail.items():
        # Add a non-field error to '__all__' by setting the field to None
        if field not in form.fields:
            field = None
        match error_message:
            case str():
                form.add_error(field, error_message)
            case list() as error_list:
                for e in error_list:
                    match e:
                        case str():
                            form.add_error(field, e)
                        case _:
                            logger.warning(
                                "When adding errors from a list to field %s "
                                "in form %s, found type %s "
                                "that I don't know how to handle",
                                field,
                                repr(form),
                                type(e),
                            )
            case _:
                logger.warning(
                    "When adding errors to field %s in form %s, found type %s "
                    "that I don't know how to handle",
                    field,
                    repr(form),
                    type(error_message),
                )
