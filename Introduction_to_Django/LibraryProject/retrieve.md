Repeat the same for:

#### `retrieve.md`
```markdown
```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
book.title, book.author, book.publication_year
# ('1984', 'George Orwell', 1949)

curl http://localhost:8000/books/1/



