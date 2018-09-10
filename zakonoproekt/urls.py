# from django.contrib import admin
# from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

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

if settings.DEBUG:
    media = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += media
