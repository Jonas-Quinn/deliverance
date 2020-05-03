from django.urls import path

from .views import (
    ItemDetailView,
    ItemListView,
    ItemCreateView,
    ItemUpdateView,
    ItemDeleteView,
    MerchantItemListView,
    MerchantBidListView,
    item_create,
    item_detail,
    bidding
)
from . import views

#app_name = 'bazaar'
urlpatterns = [
    path('', ItemListView.as_view(), name='bazaar-home'),
    path('merchant/<str:username>', MerchantItemListView.as_view(), name='merchant-items'),
    path('merchant/bids/<str:username>', MerchantBidListView.as_view(), name='merchant-bids'),
    path('item/<int:pk>/', item_detail, name='item-detail'),
    path('item/new/', ItemCreateView.as_view(), name='item-create'),
    path('new-item/', item_create, name='item_create'),
    path('item/<int:pk>/update/', ItemUpdateView.as_view(), name='item-update'),
    path('item/<int:pk>/delete/', ItemDeleteView.as_view(), name='item-delete'),
    path('item/<int:pk>/bidding/', bidding, name='bidding'),
    path('about/', views.about, name='bazaar-about'),
]
