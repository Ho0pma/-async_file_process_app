from django.urls import path, include
from rest_framework.routers import DefaultRouter


from .views import FileViewSet, CustomApiRootView

router = DefaultRouter()
router.register(r'files', FileViewSet)


urlpatterns = [
   path('', CustomApiRootView.as_view(), name='api-root'),
   path('', include(router.urls))
]

