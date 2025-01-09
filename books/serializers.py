from rest_framework import serializers
from .models import BooksBook, BooksAuthor, BooksFormat, BooksLanguage, BooksSubject, BooksBookshelf


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the BooksAuthor model, representing author details such as name and birth/death years.
    """
    class Meta:
        model = BooksAuthor
        fields = ['id', 'name', 'birth_year', 'death_year']


class FormatSerializer(serializers.ModelSerializer):
    """
    Serializer for the BooksFormat model, representing the format of the book, including mime type and URL.
    """
    class Meta:
        model = BooksFormat
        fields = ['mime_type', 'url']


class LanguageSerializer(serializers.ModelSerializer):
    """
    Serializer for the BooksLanguage model, representing the language code of the book.
    """
    class Meta:
        model = BooksLanguage
        fields = ['code']


class SubjectSerializer(serializers.ModelSerializer):
    """
    Serializer for the BooksSubject model, representing the subject or category of the book.
    """
    class Meta:
        model = BooksSubject
        fields = ['name']


class BookshelfSerializer(serializers.ModelSerializer):
    """
    Serializer for the BooksBookshelf model, representing the bookshelf or collection the book belongs to.
    """
    class Meta:
        model = BooksBookshelf
        fields = ['name']


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the BooksBook model, representing book details including title, authors, genres, languages,
    subjects, bookshelves, and formats.
    """
    authors = serializers.SerializerMethodField()
    genres = serializers.SerializerMethodField()
    bookshelves = serializers.SerializerMethodField()
    languages = serializers.SerializerMethodField()
    subjects = serializers.SerializerMethodField()
    book_formats = FormatSerializer(many=True, read_only=True, source='booksformat_set')

    class Meta:
        model = BooksBook
        fields = [
            'title', 'gutenberg_id', 'download_count', 'media_type',
            'authors', 'book_formats', 'languages', 'subjects', 'bookshelves', 'genres'
        ]

    def get_genres(self, obj):
        """
        Returns a list of unique genres associated with the book, by cleaning the subject names.
        Splits on ' -- ' and picks the last part of each subject name to determine the genre.
        """
        try:
            subjects = obj.booksbooksubjects_set.all().values_list('subject__name', flat=True)
            cleaned_genres = [genre.split(' -- ')[-1] for genre in subjects]
            return list(set(cleaned_genres))
        except Exception as e:
            raise serializers.ValidationError(f"Error retrieving genres: {e}")

    def get_authors(self, obj):
        """
        Returns a list of authors for the current book, serialized using AuthorSerializer.
        Handles potential errors in fetching authors.
        """
        try:
            authors = BooksAuthor.objects.filter(booksbookauthors__book=obj)
            return AuthorSerializer(authors, many=True).data
        except Exception as e:
            raise serializers.ValidationError(f"Error retrieving authors: {e}")

    def get_languages(self, obj):
        """
        Returns a list of languages for the current book, serialized as a list of language codes.
        Handles potential errors in fetching languages.
        """
        try:
            languages = obj.booksbooklanguages_set.all().values_list('language__code', flat=True)
            return list(languages)
        except Exception as e:
            raise serializers.ValidationError(f"Error retrieving languages: {e}")

    def get_subjects(self, obj):
        """
        Returns a list of subjects associated with the current book.
        Handles potential errors in fetching subjects.
        """
        try:
            subjects = obj.booksbooksubjects_set.all().values_list('subject__name', flat=True)
            return list(subjects)
        except Exception as e:
            raise serializers.ValidationError(f"Error retrieving subjects: {e}")

    def get_bookshelves(self, obj):
        """
        Returns a list of bookshelves associated with the current book.
        Handles potential errors in fetching bookshelves.
        """
        try:
            bookshelves = obj.booksbookbookshelves_set.all().values_list('bookshelf__name', flat=True)
            return list(bookshelves)
        except Exception as e:
            raise serializers.ValidationError(f"Error retrieving bookshelves: {e}")
