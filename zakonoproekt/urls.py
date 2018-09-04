"""zakonoproekt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
# from django.contrib import admin
# from django.urls import path, include

from rest_framework.routers import DefaultRouter

from initiators.views import InitiatorViewSet
from committees.views import CommitteeViewSet
from bills.views import BillViewSet


router = DefaultRouter()
router.register(r'intiators', InitiatorViewSet, base_name='initiators')
router.register(r'committees', CommitteeViewSet, base_name='committees')
router.register(r'bills', BillViewSet, base_name='bills')

urlpatterns = router.urls

# urlpatterns = [
#    path('admin/', admin.site.urls),
# ]
