from django.contrib import admin


from ordering.models import Barangay, About, Food, Testimonial, FoodList, Catering, Profile, Order, OrderItems, CateringSchedule, CateringReserve


admin.site.site_header = 'J6 Balbacuahan Admin Site'
admin.site.site_title = 'J6 Balbacuahan'
admin.site.index_title = 'J6 Balbacuahan'


admin.site.register(Food)
admin.site.register(Testimonial)
admin.site.register(Profile)
admin.site.register(About)
admin.site.register(Barangay)
admin.site.register(CateringReserve)
admin.site.register(CateringSchedule)


class OrderItemsInline(admin.StackedInline):
    model = OrderItems


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemsInline]

class FoodListInline(admin.StackedInline):
    model = FoodList


@admin.register(Catering)
class CateringAdmin(admin.ModelAdmin):
    inlines = [FoodListInline]


