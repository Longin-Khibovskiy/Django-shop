from django.contrib import admin
from .models import Shoes, Supplier, Order, Pos_order, Chegue


class ShoesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'supplier', 'exist')  # Отображение полей
    list_display_links = ('id', 'name')  # Установка ссылок на атрибуты
    search_fields = ('name', 'price')  # Поиск по полям
    list_editable = ('price', 'exist')  # Изменяемое поле
    list_filter = ('exist', 'supplier')  # Фильтр полей


admin.site.register(Shoes, ShoesAdmin)  # Модель, Форма админки модель


class SupplierAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'agent_firstname', 'agent_name', 'agent_patronymic', 'exist')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'agent_firstname')
    list_editable = ('exist',)
    list_filter = ('exist',)


admin.site.register(Supplier, SupplierAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_create', 'date_finish', 'status', 'price', 'address_delivery')
    list_display_links = ('id',)
    search_fields = ('date_create', 'address_delivery')
    list_editable = ('date_finish', 'status')
    list_filter = ('status',)


admin.site.register(Order, OrderAdmin)


class Pos_orderAdmin(admin.ModelAdmin):
    list_display = ('id', 'shoes', 'order', 'count_shoes', 'price')
    list_display_links = ('shoes', 'order')
    search_fields = ('shoes', 'order')


admin.site.register(Pos_order, Pos_orderAdmin)


class ChegueAdmin(admin.ModelAdmin):
    list_display = ('order', 'date_print', 'address_print', 'terminal')
    list_display_links = ('order', 'date_print')
    search_fields = ('date_print', 'address_print')


admin.site.register(Chegue, ChegueAdmin)










