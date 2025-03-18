from django import forms
from .models import Partner

# Форма для регистрации партнеров
class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = ['name', 'contact_info', 'email', 'phone']  # Добавлены новые поля

    def clean_contact_info(self):
        contact_info = self.cleaned_data['contact_info']
        if Partner.objects.filter(contact_info=contact_info).exists():
            raise forms.ValidationError("Контактная информация уже используется.")
        return contact_info