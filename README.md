# Django Blog Project

A simple and functional blog application built with **Django**, featuring posts, categories, comments, user profiles, like system, search functionality, and pagination.  
The project uses **Django Allauth** for user authentication and supports a clean, modular structure without any APIs.

---

## 🚀 Features

- **Post Management**
  - Create, edit, delete posts
  - Slug-based URLs
  - Featured image support (if added)

- **Categories**
  - Each post belongs to a category
  - Category-based filtering

- **Comments**
  - Users can comment on posts
  - Admin moderation support

- **User Profiles**
  - Extended user profile model
  - Avatar / bio fields (if added)

- **Like System**
  - Users can like/unlike posts

- **Search**
  - Full-text search on posts

- **Pagination**
  - Paginated blog listing pages

- **Authentication**
  - Django Allauth login / logout / register
  - Email-based authentication (optional)

---

## 🛠 Installation

### 1. Clone the repository

```bash
git clone https://github.com/YourUsername/your-blog-project.git
cd your-blog-project
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # For Linux/Mac
venv\Scripts\activate      # For Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Create superuser

```bash
python manage.py createsuperuser
```

### 6. Run the server

```bash
python manage.py runserver
```

---

