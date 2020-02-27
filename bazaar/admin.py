from django.contrib import admin

from .models import Item, Item_Image

# Register your models here.
class PicsInline(admin.TabularInline):
    model = Item_Image
    extra = 2


class ItemAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,   {'fields': ['title']}),
        (None,  {'fields': ['description']}),
        ('Date information', {'fields': ['date_posted'], 'classes': ['collapse']}),
    ]
    inlines = [PicsInline]
    list_display = ('title', 'merchant', 'date_posted', 'end_of_auction')
    list_filter = ['title', 'date_posted']


class Item_ImageAdmin(admin.ModelAdmin):
    list_display = ('item', 'image')


admin.site.register(Item, ItemAdmin)
admin.site.register(Item_Image, Item_ImageAdmin)