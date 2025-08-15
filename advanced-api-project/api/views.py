from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer

# -------------------------
# List all books
# -------------------------
class BookListView(generics.ListAPIView):
    """
    GET: Retrieve a list of all books.
    Accessible to everyone (authenticated or not).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# -------------------------
# Retrieve one book by ID
# -------------------------
class BookDetailView(generics.RetrieveAPIView):
    """
    GET: Retrieve a single book by ID.
    Accessible to everyone (authenticated or not).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# -------------------------
# Create a new book
# -------------------------
class BookCreateView(generics.CreateAPIView):
    """
    POST: Create a new book.
    Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Custom behavior: just save normally, but could log user here
        serializer.save()


# -------------------------
# Update a book
# -------------------------
class BookUpdateView(generics.UpdateAPIView):
    """
    PUT/PATCH: Update an existing book.
    Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        # Could add custom logging or validation here
        serializer.save()


# -------------------------
# Delete a book
# -------------------------
class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE: Remove a book.
    Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

