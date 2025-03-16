from django.contrib import admin
from .models import Service, Portfolio, Partner

admin.site.register(Service)
admin.site.register(Portfolio)


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_info', 'referral_code', 'total_referrals', 'total_earnings')
    search_fields = ('name', 'referral_code')

