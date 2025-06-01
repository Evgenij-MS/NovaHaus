from django.contrib import admin
from .models import Service, Portfolio, Partner, Calculation, Review, BlogPost, ChatLog

# Регистрация модели Service
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'labor_cost_per_m2', 'base_material_cost_per_m2')
    search_fields = ('title', 'description')
    list_filter = ('category',)
    list_editable = ('labor_cost_per_m2', 'base_material_cost_per_m2')
    ordering = ('title',)

# Регистрация модели Portfolio
@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('title', 'category')
    search_fields = ('title', 'description')
    list_filter = ('category',)
    ordering = ('title',)

# Регистрация модели Partner
@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'company', 'partner_type', 'cities', 'agreement', 'referral_code', 'total_referrals', 'total_earnings', 'created_at')
    search_fields = ('name', 'email', 'phone', 'company', 'referral_code')
    list_filter = ('partner_type', 'cities', 'agreement', 'created_at')
    readonly_fields = ('referral_code', 'total_referrals', 'total_earnings', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('user', 'name', 'email', 'phone', 'company')
        }),
        ('Partner Details', {
            'fields': ('partner_type', 'cities', 'agreement')
        }),
        ('Referral Information', {
            'fields': ('referral_code', 'total_referrals', 'total_earnings')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    ordering = ('-created_at',)

# Регистрация модели Calculation
@admin.register(Calculation)
class CalculationAdmin(admin.ModelAdmin):
    list_display = ('user', 'work_type', 'area', 'total_cost', 'status', 'created_at')
    search_fields = ('work_type', 'status', 'user__username')
    list_filter = ('status', 'created_at')
    ordering = ('-created_at',)

# Регистрация модели Review
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'rating', 'created_at')
    search_fields = ('author', 'text', 'user__username')
    list_filter = ('rating', 'created_at')
    ordering = ('-created_at',)

# Регистрация модели BlogPost
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date')
    search_fields = ('title', 'content')
    list_filter = ('published_date',)
    ordering = ('-published_date',)

# Регистрация модели ChatLog
@admin.register(ChatLog)
class ChatLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'language', 'created_at')
    search_fields = ('message', 'response', 'user__username')
    list_filter = ('language', 'created_at')
    ordering = ('-created_at',)