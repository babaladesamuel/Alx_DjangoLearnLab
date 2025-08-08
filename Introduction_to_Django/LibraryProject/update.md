
#### `update.md`
```markdown
```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
book
# <Book: Nineteen Eighty-Four by George Orwell (1949)>

curl -X PUT http://localhost:8000/books/1/ -H "Content-Type: application/json" -d '{"title": "Updated Book", "author": "Jane Doe"}'




