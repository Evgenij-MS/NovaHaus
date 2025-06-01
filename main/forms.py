from django import forms
from .models import Partner

# Форма для калькулятора (оставляем без изменений)
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
    partner_type_choices = (
        ('realtor', 'Риелтор/Агентство недвижимости'),
        ('designer', 'Дизайнер интерьеров'),
        ('architect', 'Архитектор'),
        ('business', 'Бизнес-партнёр'),
        ('other', 'Другое'),
    )
    cities_choices = (
        ('cologne', 'Кёльн'),
        ('hamburg', 'Гамбург'),
        ('both', 'Оба города'),
    )

    partner_type = forms.ChoiceField(
        choices=partner_type_choices,
        label='Тип партнёрства',
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    cities = forms.ChoiceField(
        choices=cities_choices,
        label='Города работы',
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    agreement = forms.BooleanField(
        label='Я согласен с условиями партнёрской программы',
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Partner
        fields = ['name', 'email', 'phone', 'company', 'partner_type', 'cities', 'agreement']
        widgets = {
            'name': forms.TextInput(attrs={'required': True, 'class': 'form-control', 'placeholder': 'Введите имя и фамилию'}),
            'email': forms.EmailInput(attrs={'required': True, 'class': 'form-control', 'placeholder': 'Введите email'}),
            'phone': forms.TextInput(attrs={'required': True, 'class': 'form-control', 'placeholder': 'Введите телефон'}),
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название компании (если есть)'}),
        }
        error_messages = {
            'name': {
                'required': 'Пожалуйста, укажите имя и фамилию.',
            },
            'email': {
                'required': 'Пожалуйста, укажите email.',
                'invalid': 'Введите корректный email.',
            },
            'phone': {
                'required': 'Пожалуйста, укажите телефон.',
            },
            'partner_type': {
                'required': 'Пожалуйста, выберите тип партнёрства.',
            },
            'cities': {
                'required': 'Пожалуйста, выберите город работы.',
            },
            'agreement': {
                'required': 'Необходимо согласиться с условиями партнёрской программы.',
            },
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Partner.objects.filter(email=email).exists():
            raise forms.ValidationError('Этот email уже зарегистрирован.')
        return email