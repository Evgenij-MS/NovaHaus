from django.contrib import admin
from .models import Service, Portfolio, Partner, Calculation, Review

# Регистрация модели Service
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price')
    search_fields = ('title', 'category')
    list_filter = ('category',)

# Регистрация модели Portfolio
@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('title', 'category')
    search_fields = ('title', 'category')
    list_filter = ('category',)

# Регистрация модели Partner
@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_info', 'referral_code', 'total_referrals', 'total_earnings', 'created_at')
    search_fields = ('name', 'referral_code')
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'updated_at')

# Регистрация модели Calculation
@admin.register(Calculation)
class CalculationAdmin(admin.ModelAdmin):
    list_display = ('user', 'work_type', 'total_cost', 'status')
    search_fields = ('work_type', 'status')
    list_filter = ('status',)

# Регистрация модели Review
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'created_at')
    search_fields = ('user__username', 'text')
    list_filter = ('rating', 'created_at')