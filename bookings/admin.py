from django.contrib import admin

from .models import Booking, Cake, Payment


@admin.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'flavor', 'is_available')
    list_filter = ('flavor', 'is_available')
    search_fields = ('name', 'description')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'cake', 'weight_kg', 'quantity', 'total_price', 'status', 'payment_status')
    list_filter = ('status', 'payment_status', 'delivery_date')
    search_fields = ('user__username', 'user__email', 'cake__name', 'delivery_address')
    readonly_fields = ('total_price', 'created_at', 'updated_at')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'amount', 'payment_method', 'transaction_id', 'paid_at')
    list_filter = ('payment_method', 'paid_at')
    search_fields = ('transaction_id', 'booking__user__username')
