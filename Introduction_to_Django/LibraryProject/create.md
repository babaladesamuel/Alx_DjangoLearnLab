```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
book
# <Book: 1984 by George Orwell (1949)>

curl -X POST http://localhost:8000/books/ -H "Content-Type: application/json" -d '{"title": "New Book", "author": "John Doe"}'





