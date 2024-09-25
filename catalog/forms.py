from django import forms
from django.core.exceptions import ValidationError
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
        exclude = ('owner',)

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

class ProductModeratorForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ('description', 'category', 'is_published',)

        def clean_description(self):
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

    def clean__product_version(self):
        cleaned_data = super().clean()
        version_number = cleaned_data.get('version_number')
        product = cleaned_data.get('product')

        if Version.objects.filter(product=product, version_number=version_number).exists():
            raise ValidationError(f'Версия {version_number} для этого продукта уже существует.')

        return cleaned_data

    # def clean_is_active(self):
    #     product = self.instance  # получаем продукт, с которым работаем
    #     versions = product.version_set.all()  # все версии этого продукта
    #     cleaned_data = self.cleaned_data["is_active"]
    #
    #     if versions.filter(is_active=True).exists() and cleaned_data:
    #         raise ValidationError('Не может быт несколько актуальных версий')
    #
    #     return cleaned_data

