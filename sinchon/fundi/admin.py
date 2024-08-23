from django.contrib import admin
from django.utils.html import format_html
from .models import *
# Register your models here.

# ClubAdmin


class ClubAdmin(admin.ModelAdmin):
    list_display = ('clubname',)
    search_fields = ('clubname',)

# MemberAdmin


class MemberAdmin(admin.ModelAdmin):
    list_display = ('membername', 'club', 'memberdues')
    search_fields = ('membername',)
    list_filter = ('club',)

# EventAdmin (부모 클래스)


class EventAdmin(admin.ModelAdmin):
    list_display = ('eventName', 'club', 'startDate', 'endDate', 'budget')
    search_fields = ('eventName',)
    list_filter = ('club', 'startDate', 'endDate')

# MembershipFeeEventAdmin


class MembershipFeeEventAdmin(admin.ModelAdmin):
    list_display = ('eventName', 'club', 'startDate',
                    'endDate', 'budget', 'money')
    search_fields = ('eventName',)
    list_filter = ('club', 'startDate', 'endDate')

# PartialFeeEventAdmin


class PartialFeeEventAdmin(admin.ModelAdmin):
    list_display = ('eventName', 'club', 'startDate',
                    'endDate', 'budget', 'money')
    search_fields = ('eventName',)
    list_filter = ('club', 'startDate', 'endDate')

# NoFeeEventAdmin


class NoFeeEventAdmin(admin.ModelAdmin):
    list_display = ('eventName', 'club', 'startDate',
                    'endDate', 'budget', 'money')
    search_fields = ('eventName',)
    list_filter = ('club', 'startDate', 'endDate')


class MoneyListAdmin(admin.ModelAdmin):
    list_display = ('list', 'money', 'eventid', 'category', 'receipt_preview')  # 'receipt_preview' 추가
    search_fields = ('list', 'category')
    list_filter = ('category', 'eventid')

    def receipt_preview(self, obj):
        if obj.receipt:
            return format_html('<img src="{}" style="width: 50px; height: 50px;" />'.format(obj.receipt.url))
        return "No Image"
    
    receipt_preview.short_description = "Receipt Preview"



# Registering models to admin site
admin.site.register(Club, ClubAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(MembershipFeeEvent, MembershipFeeEventAdmin)
admin.site.register(PartialFeeEvent, PartialFeeEventAdmin)
admin.site.register(NoFeeEvent, NoFeeEventAdmin)
admin.site.register(MoneyList, MoneyListAdmin)