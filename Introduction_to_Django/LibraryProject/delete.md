
#### `delete.md`
```markdown
```python
from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
Book.objects.all()
# <QuerySet []>
curl -X DELETE http://localhost:8000/books/1/




