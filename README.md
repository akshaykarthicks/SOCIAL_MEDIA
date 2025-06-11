# Social Media Platform

A social media platform built with Django.
https://our-social.onrender.com
## HOME 
![image](https://github.com/user-attachments/assets/f75adedf-5a87-4659-8180-96cc7f2665ef)
## Account Setting
![image](https://github.com/user-attachments/assets/bd1b7b3a-53a5-4296-bbf8-e883fda1cb20)
## User Profile
![image](https://github.com/user-attachments/assets/eb4ddfde-61d6-4179-82d0-21ed81171f8c)
## Search Other User 
![image](https://github.com/user-attachments/assets/55c6b4e7-ae21-4d00-beb4-49be19dbe667)



## Features

- User authentication (signup, signin, logout)
- Post creation and display
- User profiles
- Follow functionality
- Liking posts
- Image uploads
- Search for users

## Requirements

- Python 3.11+
- Django 5.0.x
- Gunicorn
- Pillow
- Whitenoise

## Setup Instructions

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url-here> 
    cd <repository-directory-name> 
    ```
    (Replace `<your-repository-url-here>` with the actual URL of your Git repository, and `<repository-directory-name>` with the name of the directory created after cloning, if different from the repository name).

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    # For Windows:
    # venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser (optional, for admin access):**
    ```bash
    python manage.py createsuperuser
    ```
    (Follow the prompts to set a username, email, and password.)

6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

## Usage

After starting the development server, access the application by navigating to `http://120.0.0.1:8000/` in your web browser.
- Sign up for a new account or sign in if you already have one.
- Explore user profiles, follow users, create posts, and like posts.

## Technologies Used

- Python 3.11+
- Django 5.0.x
- SQLite (default database)
- Gunicorn (for deployment)
- Whitenoise (for serving static files in production)
- Pillow (for image processing)
- HTML5
- CSS3 (including Tailwind CSS, UIKit)
- JavaScript
