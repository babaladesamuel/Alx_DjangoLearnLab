from django.db import models

class Author(models.Model):
    """
    Author model
    - Represents an author entity.
    - Fields:
        name: The author's display name (e.g., "Chinua Achebe").
    - Relationships:
        One Author -> Many Books (see Book.author).
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Book model
    - Represents a book entity written by an Author.
    - Fields:
        title: Title of the book (e.g., "Things Fall Apart").
        publication_year: The year the book was published (int).
        author: ForeignKey to Author, establishing a one-to-many relationship.
                 related_name='books' lets us access an author's books via author.books
    """
    title = models.CharField(max_length=255)
    publication_year = models.PositiveIntegerField()
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books'
    )

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
