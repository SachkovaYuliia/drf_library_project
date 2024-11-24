from django_filters import rest_framework as filters
from .models import Book

class BookFilter(filters.FilterSet):
    author = filters.CharFilter(field_name="author", lookup_expr="icontains")
    genre = filters.CharFilter(field_name="genre", lookup_expr="icontains")
    published_year = filters.NumberFilter(field_name="publication_year")
    title = filters.CharFilter(field_name="title", lookup_expr="icontains")  

    class Meta:
        model = Book
        fields = ['author', 'genre', 'publication_year', 'title']
