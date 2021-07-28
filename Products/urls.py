from django.urls import path
from . import views
urlpatterns = [
    path('product_details/<int:id>/', views.ProductDetailsView.as_view() , name = 'product_details'),
    path('product_category/<category>' , views.ProductCategoryView.as_view() , name = 'product_category_details'),
    path('mobile_details/<category>/<brand>' , views.BrandProductView.as_view() , name = 'product_details_brand'),
    path('add_to_cart/<int:id>/', views.AddToCartView.as_view() , name ='add_to_cart'),
    path('show_cart/',views.ShowCart,name = 'show_cart'),
    path('plus_cart/',views.PlusCartView.as_view() ),
    path('minus_cart/',views.MinusCartView.as_view()),
    path('remove_cart/',views.RemoveCartView.as_view()),
    path ('checkout/',views.CheckOutView.as_view(),name='checkout'),
    path ('payment/',views.PaymentView.as_view(),name='payment'),
    path ('order/',views.OrderView.as_view(),name='orders'),
    path('buy_now/<int:id>/',views.BuyNowView.as_view(),name='buy_now'),
    
    
]