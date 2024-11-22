from django import forms
from django.core import validators


class UserValidator(forms.Form):
    """
    UserValidator is a form that validates the name, last name, and identification of a user.
    """

    name = forms.CharField(
        max_length=100,
        required=True,
        validators=[
            validators.RegexValidator(
                regex=r"^[a-zA-ZáéíóúÁÉÍÓÚ\s]+$",
                code="invalid_name",
            )
        ],
    )

    last_name = forms.CharField(
        max_length=100,
        required=True,
        validators=[
            validators.RegexValidator(
                regex=r"^[a-zA-ZáéíóúÁÉÍÓÚ\s]+$",
                code="invalid_last_name",
            )
        ],
    )

    identification = forms.CharField(
        max_length=100,
        required=True,
        validators=[
            validators.RegexValidator(
                regex=r"^[0-9]+$",
                code="invalid_identification",
            )
        ],
    )
