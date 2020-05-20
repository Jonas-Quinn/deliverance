from django.contrib import admin

from .models import Item, Item_Image, Bid

# Register your models here.
class PicsInline(admin.TabularInline):
    model = Item_Image
    extra = 2


class BidsInline(admin.TabularInline):
    model = Bid


class ItemAdmin(admin.ModelAdmin):
    # fieldsets = [
    #     (None,   {'fields': ['title']}),
    #     (None,  {'fields': ['description']}),
    #     ('Date information', {'fields': ['end_of_auction'], 'classes': ['collapse']}),
    # ]
    inlines = [PicsInline]
    list_display = ('title', 'merchant', 'date_posted', 'remaining_time')
    list_filter = ['title', 'date_posted']
    class Meta:
        model = Item


class ItemBidsAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,   {'fields': ['title']}),
    ]
    inlines = [BidsInline]
    list_display = ('title', 'merchant')


class Item_ImageAdmin(admin.ModelAdmin):
    list_display = ('item', 'image')


class BidAdmin(admin.ModelAdmin):
    list_display = ('item', 'merchant', 'bid', 'date')


admin.site.register(Item, ItemAdmin)
admin.site.register(Item_Image, Item_ImageAdmin)
admin.site.register(Bid, BidAdmin)