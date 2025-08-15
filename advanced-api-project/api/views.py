from django.shortcuts import render
from rest_framework import generics
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
    # Explicit backends (in addition to global settings — harmless and clear)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Filtering: allow multiple lookups on fields (django-filter)
    filterset_fields = {
        'title': ['exact', 'icontains'],
        'publication_year': ['exact', 'gte', 'lte'],
        'author': ['exact'],               # filter by author ID
        'author__name': ['exact', 'icontains'],  # filter by author name
    }

    # Searching (DRF SearchFilter): uses icontains under the hood
    search_fields = ['title', 'author__name']

    # Ordering (DRF OrderingFilter)
    ordering_fields = ['id', 'title', 'publication_year', 'author__name']
    ordering = ['title']  # default

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