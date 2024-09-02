from django import forms

from catalog.models import ContactData


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactData
        fields = ['name', 'phone','message' ]