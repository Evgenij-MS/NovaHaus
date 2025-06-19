from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.messages import get_messages

from .models import Profile
from .forms import ProfileForm

class ProfileModelTests(TestCase):
    """Tests for the Profile model."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

    def test_profile_creation(self):
        """Test that a profile can be created."""
        profile = Profile.objects.create(
            user=self.user,
            bio='This is a test bio'
        )
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.bio, 'This is a test bio')
        self.assertFalse(bool(profile.avatar))

    def test_profile_str_method(self):
        """Test the __str__ method of the Profile model."""
        profile = Profile.objects.create(
            user=self.user,
            bio='This is a test bio'
        )
        self.assertEqual(str(profile), "testuser's Profile")

class ProfileFormTests(TestCase):
    """Tests for the ProfileForm."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            bio='This is a test bio'
        )

    def test_valid_form(self):
        """Test that the form is valid with correct data."""
        form_data = {
            'bio': 'Updated bio'
        }
        form = ProfileForm(data=form_data, instance=self.profile)
        self.assertTrue(form.is_valid())

    def test_blank_bio(self):
        """Test that the form is valid with a blank bio."""
        form_data = {
            'bio': ''
        }
        form = ProfileForm(data=form_data, instance=self.profile)
        self.assertTrue(form.is_valid())

class ProfileViewTests(TestCase):
    """Tests for the profile views."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            bio='This is a test bio'
        )
        self.detail_url = reverse('profiles:profile_detail', kwargs={'username': 'testuser'})
        self.edit_url = reverse('profiles:profile_edit')

    def test_profile_detail_view(self):
        """Test the profile detail view."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/detail.html')
        self.assertEqual(response.context['profile'], self.profile)
        self.assertEqual(response.context['user_profile'], self.user)

    def test_profile_edit_view_unauthenticated(self):
        """Test that unauthenticated users cannot access the edit view."""
        response = self.client.get(self.edit_url)
        self.assertNotEqual(response.status_code, 200)

    def test_profile_edit_view_authenticated(self):
        """Test that authenticated users can access the edit view."""
        self.client.force_login(self.user)
        response = self.client.get(self.edit_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/edit.html')

    def test_profile_edit_post(self):
        """Test updating a profile via POST."""
        self.client.login(username='testuser', password='testpassword')
        form_data = {
            'bio': 'Updated bio'
        }
        response = self.client.post(self.edit_url, form_data, follow=True)
        self.assertEqual(response.status_code, 200)

        # Check that the profile was updated
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.bio, 'Updated bio')

        # Check for success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('successfully', str(messages[0]))
