from django.urls import path

from .views import (
    ItemDetailView,
    ItemListView,
    ItemCreateView,
    ItemUpdateView,
    ItemDeleteView,
    MerchantItemListView,
    item_create
)
from . import views

urlpatterns = [
    path('', ItemListView.as_view(), name='bazaar-home'),
    path('merchant/<str:username>', MerchantItemListView.as_view(), name='merchant-items'),
    path('item/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
    path('item/new/', ItemCreateView.as_view(), name='item-create'),
    # path('item/<int:pk>/new-image/', Item_ImageCreateView.as_view(), name='item-image-create'),
    path('new-item/', item_create, name='item_create'),
    path('item/<int:pk>/update/', ItemUpdateView.as_view(), name='item-update'),
    path('item/<int:pk>/delete/', ItemDeleteView.as_view(), name='item-delete'),
    path('about/', views.about, name='bazaar-about'),
]
