# Gutenberg-API

This project provides an API to query and access books from the Project Gutenberg repository. It allows filtering books based on various criteria and returns detailed information about the books, including download links and metadata.

## Features
- **Filter books** by:
  - Book ID (Project Gutenberg ID)
  - Language
  - Mime-type
  - Topic (subject or bookshelf)
  - Author
  - Title
- **Pagination**: If there are more than 25 books matching the query, the API will paginate and provide links to retrieve the next set of books.
- **Sorted results**: Books are sorted by the number of downloads (popularity) in descending order.
- **Case-insensitive partial matches** for all filters.

## API Endpoints
You can use the following filters in the API queries:

- **Book ID**: Filter books by Project Gutenberg ID numbers.
- **Language**: Filter by language codes (e.g., `en`, `fr`).
- **Mime-type**: Filter by mime-type (e.g., `application/epub+zip`).
- **Topic**: Filter by topics such as `subject` or `bookshelf` (case-insensitive).
- **Author**: Filter by author name (case-insensitive).
- **Title**: Filter by book title (case-insensitive).

### Example Request

```http
GET /api/books?language=en,fr&topic=child&author=Shakespeare
```

# Project Setup

## Step 1: Configure Environment
Change the environment according to the target environment:
- Use `.dev.env` for development
- Use `.prod.env` for production

## Step 2: Set Executable Permissions
Run the following command to set the correct permissions for `start.sh`:

```bash
chmod +x start.sh
```

## Step 3: Execute start.sh
Run the script to start the application:

By default, it will run in development mode:
```bash
./start.sh
```
or
```bash
sudo ./start.sh
```

For production mode, run the following:
```bash
./start.sh prod
```
or
```bash
./start.sh production
```
## Step 4: Test Your API
Once the application is running, you can test the API with the following queries:

- Get books by language:

```bash
/books?language=en,fr
```
- Get books by topic:
```bash
/books?topic=child,infant
```
- Get books by author:

```bash
/books?author=austen
```
- Get books by genre:

```bash
/books?genre=fiction,romance
```
- Get books by Gutenberg ID:

```bash
/books?gutenberg_id=1342,12345
```
- Get books by title:

```bash
/books?title=pride
```


