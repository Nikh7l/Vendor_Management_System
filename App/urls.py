from django.urls import path
from . import views

urlpatterns = [
    path('api/vendors/', views.vendor,name='vendor'),
    path('api/vendors/<int:vendor_id>/', views.vendor_detail, name = 'vendor_detail'),
    path('api/purchase_orders/', views.purchase_orders , name = 'purchase_orders'),
    path('api/purchase_orders/<int:po_id>/', views.purchase_order_detail , name = 'purchase_order_detail'),
    path('api/purchase_orders/<int:po_id>/acknowledge/', views.acknowledge_purchase_order , name = 'acknowledge_purchase_order'),
    path('api/vendors/<int:vendor_id>/performance/', views.vendor_performance, name='vendor_performance'),
]
