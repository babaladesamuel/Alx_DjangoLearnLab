from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated  # Import permission class
from rest_framework.authentication import TokenAuthentication  # Import auth class

from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    authentication_classes = [TokenAuthentication]  # Enable token auth
    permission_classes = [IsAuthenticated]           # Require authenticated users





