from django.urls import path
from django.conf.urls import url

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
    #  ordering of these lines is crucial,
    #  if the item_detail url entry in code is evaluated before
    #  item_create url. This gives item_detail more priority over item_create.
    #
    # Since item_detail url is /auction/ + anything that matches [-_\w]+
    # and new matches the regex, Django thinks that you are passing new
    # as the slug for item_detail view and passes it as a keyword argument
    # to the view. Since there is no post with new as slug, the view
    # returns 404 Not found
    path('', ItemListView.as_view(), name='bazaar-home'),
    path('about/', views.about, name='bazaar-about' ),
    path('merchant/<str:username>', MerchantItemListView.as_view(), name='merchant-items'),
    path('merchant/bids/<str:username>', MerchantBidListView.as_view(), name='merchant-bids'),
    url(r'^new-auction/$', item_create, name='item_create' ),
    url(r'^auction/(?P<slug>[\w-]+)/$',  item_detail, name='item-detail'),
    path('item/new/', ItemCreateView.as_view(), name='item-create'),
    url(r'^auction/(?P<slug>[\w-]+)/update/$', ItemUpdateView.as_view(), name='item-update'),
    url(r'^auction/(?P<slug>[\w-]+)/delete/$', ItemDeleteView.as_view(), name='item-delete'),
    url(r'^auction/(?P<slug>[\w-]+)/bidding/$', bidding, name='bidding'),
]
