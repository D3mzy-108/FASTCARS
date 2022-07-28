from django.contrib import admin
from .models import AboutUs, Branch, Brand, NewCar, Vehicle, VehicleComment

# Register your models here.


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    pass


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    pass


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    pass


@admin.register(VehicleComment)
class VehicleCommentAdmin(admin.ModelAdmin):
    pass


@admin.register(NewCar)
class NewCarAdmin(admin.ModelAdmin):
    pass


@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    pass
