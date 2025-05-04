from django.test import TestCase, Client
from django.urls import reverse
from django.utils import translation
from django.contrib.auth.models import User
from main.forms import PartnerForm
from main.models import Service, Portfolio, Review, Calculation, Partner, BlogPost, ChatLog
import json


class LanguageSwitchTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_set_language_valid(self):
        """Проверка переключения на поддерживаемый язык."""
        response = self.client.post(reverse('set_language', args=['en']), {'language': 'en'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.cookies['django_language'].value, 'en')
        self.assertTrue(response.url.startswith('/en/'))

    def test_set_language_invalid(self):
        """Проверка обработки неподдерживаемого языка."""
        response = self.client.post(reverse('set_language', args=['fr']), {'language': 'fr'})
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'success': False, 'error': 'Invalid language or method'})


class HomeViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Создаём тестовые данные
        Service.objects.create(title="Test Service", description="Description", category="renovation")
        Portfolio.objects.create(title="Test Project", description="Description", category="renovation")
        Review.objects.create(author="Test User", text="Great work!", rating=5)

    def test_home_page(self):
        """Проверка загрузки главной страницы."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/home.html')
        self.assertGreaterEqual(len(response.context['services']), 1)
        self.assertGreaterEqual(len(response.context['projects']), 1)
        self.assertGreaterEqual(len(response.context['reviews']), 1)


class PartnerFormTests(TestCase):
    def test_valid_partner_form(self):
        """Проверка валидной формы партнёра."""
        form_data = {
            'name': 'Test Partner',
            'contact_info': 'test@example.com',
            'email': 'test@example.com',
            'phone': '+1234567890'
        }
        form = PartnerForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_duplicate_contact_info(self):
        """Проверка ошибки при дублировании contact_info."""
        Partner.objects.create(
            name='Existing Partner',
            contact_info='test@example.com',
            email='existing@example.com',
            phone='+1234567890',
            referral_code='UNIQUE123'
        )
        form_data = {
            'name': 'New Partner',
            'contact_info': 'test@example.com',
            'email': 'new@example.com',
            'phone': '+0987654321'
        }
        form = PartnerForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('contact_info', form.errors)


class ChatbotTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_chatbot_valid_message(self):
        """Проверка ответа чат-бота на валидное сообщение."""
        response = self.client.post('/chatbot/', data=json.dumps({
            'message': 'Hello, how can you help?',
            'language': 'en'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('response', response.json())

    def test_chatbot_invalid_method(self):
        """Проверка обработки неверного метода."""
        response = self.client.get('/chatbot/')
        self.assertEqual(response.status_code, 405)


class CalculationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_save_calculation(self):
        """Проверка сохранения расчёта."""
        calculation_data = {
            'workType': 'apartment',
            'area': 50,
            'material': 'standard',
            'includeMaterials': 'yes',
            'urgency': 'normal',
            'totalCost': 5000,
            'materialCost': 2000,
            'laborCost': 3000
        }
        response = self.client.post('/save-calculation/', data=json.dumps(calculation_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])
        self.assertTrue(Calculation.objects.filter(work_type='apartment').exists())