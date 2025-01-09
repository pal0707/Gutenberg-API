from django.db.models import Q
from rest_framework import viewsets, pagination, filters
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .serializers import BookSerializer
from .models import BooksBook


class BookPagination(pagination.PageNumberPagination):
    """
    Custom pagination class for paginating book listings.
    Sets a default page size and allows the client to modify it through the 'page_size' query parameter.
    """
    page_size = 25  # Default page size
    page_size_query_param = 'page_size'  # Allow the client to modify the page size using this query parameter


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset to handle API requests related to books.
    Supports filtering by language, topic, author, title, genre, and Gutenberg ID.
    """
    queryset = BooksBook.objects.all().order_by('-download_count')
    serializer_class = BookSerializer
    pagination_class = BookPagination
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'title', 'booksbookauthors__author__name',
        'booksbooksubjects__subject__name', 'booksbookbookshelves__bookshelf__name'
    ]

    def get_queryset(self):
        """
        Retrieves a filtered queryset based on query parameters:
        - language: Filter books by language code (e.g., 'en,fr')
        - topic: Filter books by subject or bookshelf name (e.g., 'child,infant')
        - author: Filter books by author name (e.g., 'austen')
        - title: Filter books by title (e.g., 'pride')
        - genre: Filter books by genre (e.g., 'fiction,romance')
        - gutenberg_id: Filter books by Gutenberg ID (e.g., '1342,12345')
        """
        try:
            queryset = super().get_queryset()  # Get the base queryset of books

            # Fetch filter parameters from query parameters
            language = self.request.query_params.get('language')
            topic = self.request.query_params.get('topic')
            author = self.request.query_params.get('author')
            title = self.request.query_params.get('title')
            genre = self.request.query_params.get('genre')
            gutenberg_id = self.request.query_params.get('gutenberg_id')

            # Apply filters based on provided query parameters

            # Filter by language
            if language:
                languages = language.split(',')
                queryset = queryset.filter(booksbooklanguages__language__code__in=languages)

            # Filter by topic (subject or bookshelf)
            if topic:
                topics = topic.split(',')
                topic_filter = Q()  # Initialize a Q object to combine topic filters
                for t in topics:
                    topic_filter |= Q(booksbooksubjects__subject__name__icontains=t) | Q(booksbookbookshelves__bookshelf__name__icontains=t)
                queryset = queryset.filter(topic_filter)

            # Filter by author (case insensitive partial match)
            if author:
                queryset = queryset.filter(booksbookauthors__author__name__icontains=author)

            # Filter by title (case insensitive partial match)
            if title:
                queryset = queryset.filter(title__icontains=title)

            # Filter by genre (either subject or bookshelf)
            if genre:
                genres = genre.split(',')
                genre_filter = Q()  # Initialize a Q object to combine genre filters
                for g in genres:
                    genre_filter |= Q(booksbooksubjects__subject__name__icontains=g) | Q(booksbookbookshelves__bookshelf__name__icontains=g)
                queryset = queryset.filter(genre_filter)

            # Filter by Gutenberg ID
            if gutenberg_id:
                gutenberg_ids = gutenberg_id.split(',')
                queryset = queryset.filter(gutenberg_id__in=gutenberg_ids)

            return queryset.distinct()  # Ensure the result set is distinct (no duplicates)
        
        except Exception as e:
            # Catch any unforeseen exceptions and raise a validation error with the exception message
            raise ValidationError(f"Error applying filters: {str(e)}")
    
    def list(self, request, *args, **kwargs):
        """
        Override the default list method to format the response data as required.
        The response will include 'data', 'status', 'message', and 'error' fields.
        """
        try:
            # Get the queryset with pagination
            queryset = self.get_queryset()
            page = self.paginate_queryset(queryset)
            
            if page is not None:
                # Paginated response
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response({
                    "data": serializer.data,
                    "status": 200,
                    "message": "success",
                    "error": False,
                })
            
            # If pagination is not required, return the response without pagination
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                "data": serializer.data,
                "status": 200,
                "message": "success",
                "error": False,
            })
        except Exception as e:
            # Handle any unforeseen exceptions
            return Response({
                "data": {},
                "status": 500,
                "message": f"Error occurred: {str(e)}",
                "error": True,
            }, status=500)
