from django.contrib import admin

from .models import FAQ, Booking, CustomerQuery, CustomerReview

# Register your models here.


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    pass


@admin.register(CustomerReview)
class CustomerReviewAdmin(admin.ModelAdmin):
    pass


@admin.register(CustomerQuery)
class CustomerQueryAdmin(admin.ModelAdmin):
    pass


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    pass
