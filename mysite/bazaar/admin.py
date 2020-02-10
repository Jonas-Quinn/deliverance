from django.contrib import admin

from .models import Item, Item_Pics

# Register your models here.
class PicsInline(admin.TabularInline):
    model = Item_Pics
    extra = 2


class ItemAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,   {'fields': ['title']}),
        (None,  {'fields': ['description']}),
        ('Date information', {'fields': ['date_posted'], 'classes': ['collapse']}),
    ]
    inlines = [PicsInline]
    list_display = ('title', 'date_posted', 'end_of_auction')
    list_filter = ['date_posted']

admin.site.register(Item, ItemAdmin)