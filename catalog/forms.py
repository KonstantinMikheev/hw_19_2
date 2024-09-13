from django import forms
from django.forms import BooleanField

from catalog.models import ContactData, Product, Version

REJECTED_WORDS = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар', ]


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactData
        fields = ['name', 'phone', 'message']


class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def clean_title(self):
        cleaned_data = self.cleaned_data['title']
        for word in REJECTED_WORDS:
            if word in cleaned_data.lower().strip():
                raise forms.ValidationError(
                    f'Нельзя использовать слова: "{", ".join(str(i) for i in REJECTED_WORDS)}" в названии продукта.')
        return cleaned_data

    def clean_description(self, *args, **kwargs):
        cleaned_data = self.cleaned_data['description']
        for word in REJECTED_WORDS:
            if word in cleaned_data.lower().strip():
                raise forms.ValidationError(
                    f'Нельзя использовать слова: "{", ".join(str(i) for i in REJECTED_WORDS)}" в описании продукта.'
                )
        return cleaned_data


class VersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = '__all__'
    #
    # def clean_ver_number(self, *args, **kwargs):
    #     cleaned_data = self.cleaned_data['version_number']
    #     versions_list = Version.objects.filter(КАК ЗДЕСЬ СДЕЛАТЬ ФИЛЬТРАЦИЮ, ЧТОБЫ НЕЛЬЗЯ БЫЛО УКАЗЫВАТЬ УЖЕ ИСПОЛЬЗОВАННУЮ ВЕРСИЮ?)
    #     if cleaned_data in versions_list:
    #         raise forms.ValidationError(
    #             f'Данная версия уже существует.'
    #         )
    #
    #     return cleaned_data
