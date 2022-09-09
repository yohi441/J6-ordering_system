from django.contrib import admin

from ordering.models import Food, Checkout, Testimonial, FoodList, Catering, Profile


admin.site.register(Food)
admin.site.register(Checkout)
admin.site.register(Testimonial)
admin.site.register(Profile)

class FoodListInline(admin.StackedInline):
    model = FoodList


@admin.register(Catering)
class CateringAdmin(admin.ModelAdmin):
    inlines = [FoodListInline]