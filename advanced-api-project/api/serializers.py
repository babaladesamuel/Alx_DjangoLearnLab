from rest_framework import serializers
from .models import Author, Book
import datetime

class BookSerializer(serializers.ModelSerializer):
    """
    BookSerializer
    - Serializes all Book fields.
    - Custom validation: publication_year cannot be in the future.
    """
    class Meta:
        model = Book
        fields = ["id", "title", "publication_year", "author"]

    def validate_publication_year(self, value: int) -> int:
        current_year = datetime.date.today().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    AuthorSerializer
    - Includes the author's name.
    - Includes a nested, read-only list of related books using BookSerializer.
      The 'books' source comes from Author.books due to related_name='books' on Book.author.

    Notes:
    - By setting books=BookSerializer(many=True, read_only=True), we support nested READS:
      {
        "id": 1,
        "name": "Chinua Achebe",
        "books": [
          {"id": 3, "title": "...", "publication_year": 1958, "author": 1},
          ...
        ]
      }
    - Writes remain simple: create/update Author independently; create/update Book and set its author.
      (You can later implement writable nested behavior if needed.)
    """
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ["id", "name", "books"]





