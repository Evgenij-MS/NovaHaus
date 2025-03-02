from modeltranslation.translator import register, TranslationOptions
from .models import Service, Portfolio

@register(Service)
class ServiceTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'category')  # Поля для перевода

@register(Portfolio)
class PortfolioTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'category')  # Поля для перевода