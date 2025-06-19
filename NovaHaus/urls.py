
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.shortcuts import redirect
from main import views

def register_partner_redirect(request):
    """Redirect to partner registration page"""
    return redirect("partner")

# URLs ohne Sprachpräfix (wichtige System-URLs)
urlpatterns = [
    # Django's i18n URLs (inkl. setlang)
    path("i18n/", include("django.conf.urls.i18n")),
    path("offline/", views.offline, name="offline"),
]

# URLs mit Sprachpräfix
urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("services/", views.services, name="services"),
    path("portfolio/", views.portfolio, name="portfolio"),
    path("about/", views.about, name="about"),
    path("reviews/", views.reviews, name="reviews"),
    path("contact/", views.contact, name="contact"),
    # Calculator
    path("calculator/", views.calculator, name="calculator"),
    path("calculate-cost/", views.calculate_cost, name="calculate_cost"),
    path("save-calculation/", views.save_calculation, name="save_calculation"),
    path("get-ai-recommendations/", views.get_ai_recommendations, name="get_ai_recommendations"),
    # Partner System
    path("partner/", views.partner_view, name="partner"),
    path("register-partner/", register_partner_redirect, name="register_partner"),
    path("partner-success/", views.partner_success, name="partner_success"),
    # Blog
    path("blog/", views.blog, name="blog"),
    path("blog/<int:post_id>/", views.blog_post_detail, name="blog_post_detail"),
    # Weitere Features
    path("3d-viewer/", views.view_3d_model, name="view_3d_model"),
    path("chatbot/", views.chatbot, name="chatbot"),
    path("privacy/", views.privacy, name="privacy"),
    # User-Profiles
    path("profiles/", include("profiles.urls", namespace="profiles")),
    # Wichtig: prefix_default_language=False bedeutet die Standard-Sprache hat keinen Präfix
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)