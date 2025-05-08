from django import forms
from .models import Partner

# Форма для калькулятора
class CalculatorForm(forms.Form):
    work_type = forms.ChoiceField(choices=[
        ('apartment', 'Ремонт квартиры'),
        ('house', 'Ремонт дома'),
        ('office', 'Ремонт офиса'),
        ('warehouse', 'Ремонт склада'),
        ('facade', 'Фасадные работы'),
        ('bathroom', 'Ремонт ванной'),
        ('electrical', 'Электрические работы'),
        ('demolition', 'Демонтажные работы')
    ], label="Тип работы")
    area = forms.FloatField(min_value=0.1, label="Площадь (м²)")
    material_quality = forms.ChoiceField(choices=[
        ('economy', 'Эконом'),
        ('standard', 'Стандарт'),
        ('premium', 'Премиум')
    ], label="Качество материалов")

# Форма для регистрации партнеров
class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = ['name', 'contact_info', 'email', 'phone']

    def clean_contact_info(self):
        contact_info = self.cleaned_data['contact_info']
        if Partner.objects.filter(contact_info=contact_info).exists():
            raise forms.ValidationError("Контактная информация уже используется.")
        return contact_info