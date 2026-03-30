from django.contrib import admin
from django.utils.html import format_html
from .models import Hotel, RoomType, HotelContact


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'city', 'country', 'category', 'stars', 'status', 
        'created_at', 'contact_info'
    ]
    list_filter = ['status', 'category', 'stars', 'city', 'country']
    search_fields = ['name', 'city', 'code', 'email']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'code', 'description', 'status', 'category', 'stars')
        }),
        ('Контактная информация', {
            'fields': ('address', 'city', 'country', 'postal_code', 'phone', 'email', 'website')
        }),
        ('Географические данные', {
            'fields': ('latitude', 'longitude', 'timezone')
        }),
        ('Настройки времени', {
            'fields': ('check_in_time', 'check_out_time')
        }),
        ('Настройки управления', {
            'fields': ('is_auto_confirm', 'max_advance_days')
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def contact_info(self, obj):
        return format_html(
            '{}<br>{}<br>{}',
            obj.phone,
            obj.email,
            obj.city
        )
    contact_info.short_description = 'Контактная информация'


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'hotel', 'max_adults', 'max_children', 'bed_type', 
        'has_wifi', 'has_tv', 'sort_order'
    ]
    list_filter = ['hotel', 'bed_type', 'has_wifi', 'has_tv', 'has_ac']
    search_fields = ['name', 'code', 'hotel__name']
    list_editable = ['sort_order']


@admin.register(HotelContact)
class HotelContactAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'hotel', 'role', 'is_primary']
    list_filter = ['hotel', 'role', 'is_primary']
    search_fields = ['first_name', 'last_name', 'hotel__name']