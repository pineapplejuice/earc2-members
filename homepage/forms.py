from django import forms


class ContactForm(forms.Form):
    contact_name = forms.CharField(
        required=True, label="Contact name", max_length=255)
    contact_email = forms.EmailField(
        required=True, label="Contact email", max_length=255)
    contact_message = forms.CharField(
        required=True,
        widget=forms.Textarea,
    )
