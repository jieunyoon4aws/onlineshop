"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

app_name = 'shop' # 이름 공간 사용하기 위해 지정
from .views import *

urlpatterns = [
    path('', product_in_category, name='product_all'),
    path('<slug:category_slug>/', product_in_category, name='product_in_category'), # <int:pk> 와 같은 거라고 이해하면 쉬움
    path('<int:id>/<product_slug>/', product_detail, name='product_detail'), # 파이썬은 & 대신 /로 여러 값 넘김

]
