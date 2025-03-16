from django import forms
from .models import Partner

# Форма для регистрации партнеров
class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = ['name', 'contact_info']