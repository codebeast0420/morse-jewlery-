from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/email', views.email, name="email"),
    path('api/variants', views.variants, name="variants"),
    path('api/variants/create', views.variantsCreate, name="variants.create"),
    path('convertor', views.convertor, name="convertor"),
    path('<str:key>', views.customiseProduct, name="customise.product"),
    #path('customiser', views.customiser, name="customiser"),
    
    
]