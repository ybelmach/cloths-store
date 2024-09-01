import re

from django import forms


class CreateOrderForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    phone_number = forms.CharField()
    requires_delivery = forms.ChoiceField(
        choices=[
            ("0", 'False'),
            ("1", 'True'),
        ]
    )
    delivery_address = forms.CharField(required=False)
    payment_on_get = forms.ChoiceField(
        choices=[
            ("0", 'False'),
            ("1", 'True'),
        ],
    )

    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']

        pattern = re.compile(r"^1[3456789]\d{9}$")
        phone_number = re.findall(r'(\d+)', data)
        phone_number = '+' + "".join(phone_number)
        if not re.match(r'^\+?375(?:2[95]|33|44)\d{7}\b', phone_number):
            raise forms.ValidationError("Неверный формат номера")

        return data
