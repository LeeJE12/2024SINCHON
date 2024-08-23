from django.contrib import admin
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


# Registering models to admin site
admin.site.register(Club, ClubAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(MembershipFeeEvent, MembershipFeeEventAdmin)
admin.site.register(PartialFeeEvent, PartialFeeEventAdmin)
admin.site.register(NoFeeEvent, NoFeeEventAdmin)
