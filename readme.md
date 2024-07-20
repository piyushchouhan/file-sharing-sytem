# File Sharing System

## Overview

Welcome to the File Sharing System project! This Django-based application allows users to sign up, sign in, upload files, and download files. The project includes both client and operations user types, with authentication and file handling functionalities.

## Features

- **User Authentication**: Secure sign-up and sign-in processes for both client and operations users.
- **File Management**: Upload, list, and download files.
- **Email Confirmation**: Email verification for user accounts.
- **Django Allauth Integration**: Enhanced user account management and authentication.

## Technologies Used

- **Django**: Web framework for Python.
- **PostgreSQL**: Relational database system.
- **Gmail SMTP**: For sending confirmation emails.
- **Django Allauth**: For user authentication and account management.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- PostgreSQL
- Gmail account for email backend

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/filesharing.git
    cd filesharing
    ```

2. **Create a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**

    Create a `.env` file in the root directory with the following content:

    ```ini
    EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST='smtp.gmail.com'
    EMAIL_PORT=587
    EMAIL_USE_TLS=True
    EMAIL_HOST_USER='your-email@gmail.com'
    EMAIL_HOST_PASSWORD='your-email-password'
    EMAIL_USE_SSL=False

    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'filesharing',
            'USER': 'postgres',
            'PASSWORD': 'your-password',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
    ```

5. **Run migrations:**

    ```bash
    python manage.py migrate
    ```

6. **Create a superuser (optional):**

    ```bash
    python manage.py createsuperuser
    ```

7. **Run the development server:**

    ```bash
    python manage.py runserver
    ```

8. **Access the application:**

    Open your browser and go to `http://127.0.0.1:8000/` to see the application in action.

## Testing

To run tests, use:

```bash
python manage.py test
