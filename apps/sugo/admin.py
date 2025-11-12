from django.contrib import admin
from .models import *

class AccountTypeAdmin(admin.ModelAdmin):
    model = AccountType
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)
admin.site.register(AccountType, AccountTypeAdmin)

class StreamerAdmin(admin.ModelAdmin):
    model = Streamer
    list_display = ("id", "name", "real_name", "join_date", "country", "vip_level", "status", "charm_level")
    search_fields = ("id", "name", "real_name")
    list_filter = ("country", "vip_level", "charm_level", "status", 'enable')
    ordering = ("id",)
admin.site.register(Streamer, StreamerAdmin)

class WithdrawalGroupAdmin(admin.ModelAdmin):
    model = WithdrawalGroup
    list_display = ("name", "created_at")
    search_fields = ("created_at",)
    ordering = ("created_at",)
admin.site.register(WithdrawalGroup, WithdrawalGroupAdmin)

class WithdrawalAdmin(admin.ModelAdmin):
    model = Withdrawal
    list_display = ("streamer", "group","amount_usd","withdrawal_date")
    search_fields = ("streamer", "group", "withdrawal_date")
    ordering = ("withdrawal_date",)
admin.site.register(Withdrawal, WithdrawalAdmin)

class AgencyLevelAdmin(admin.ModelAdmin):
    model = AgencyLevel
    list_display = ("name", "level")
admin.site.register(AgencyLevel, AgencyLevelAdmin)

class DailyPerformanceAdmin(admin.ModelAdmin):
    model = DailyPerformance
    list_display = ("date","streamer","streamer_name","total_diamonds","diamonds_chat","diamonds_gifts","diamonds_video")
    search_fields = ("streamer", "date", "streamer_name")
admin.site.register(DailyPerformance, DailyPerformanceAdmin)
