from django_filters import rest_framework as filters
from rest_framework import generics, permissions, filters as drf_filters
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book
from .serializers import BookSerializer


# List all books or create a new one (read is open, write requires auth)
class BookListView(generics.ListCreateAPIView):
    """
    Supports:
    - Filtering:
        ?title=Things Fall Apart
        ?title__icontains=fall
        ?publication_year=1958
        ?publication_year__gte=1950&publication_year__lte=1965
        ?author=1                       (by author ID)
        ?author__name=Chinua Achebe     (exact name)
        ?author__name__icontains=achebe (partial name)
    - Searching (OR across fields):
        ?search=achebe                  (matches title OR author name)
    - Ordering:
        ?ordering=title
        ?ordering=-publication_year
        ?ordering=author__name
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Enable filtering, searching, ordering
    filter_backends = [filters.DjangoFilterBackend, drf_filters.SearchFilter, drf_filters.OrderingFilter]

    # Filtering options (Step 1)
    filterset_fields = {
        'title': ['exact', 'icontains'],
        'publication_year': ['exact', 'gte', 'lte'],
        'author': ['exact'],                # filter by author ID
        'author__name': ['exact', 'icontains'],  # filter by author name
    }

    # Search options (Step 2)
    search_fields = ['title', 'author__name']

    # Ordering options (Step 3)
    ordering_fields = ['id', 'title', 'publication_year', 'author__name']
    ordering = ['title']  # Default ordering


# Retrieve a single book (read is open, write requires auth)
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# Create a book (only logged-in users)
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


# Update a book (only logged-in users)
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


# Delete a book (only logged-in users)
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]