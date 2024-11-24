from rest_framework import viewsets, permissions, filters
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer
from .filters import BookFilter

class BookPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('title')
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = BookPagination  

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BookFilter  
    filterset_fields = ['author', 'genre', 'publication_year'] 
    search_fields = ['title']  
    ordering_fields = ['publication_year', 'author']  

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_staff:
            self.permission_denied(
                request, message="Only administrators can delete books."
            )
        return super().destroy(request, *args, **kwargs)
