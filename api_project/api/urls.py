from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet  # Remove BookList here

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    path('', include(router.urls)),  # Only use the router URLs here
]








