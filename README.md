# Learnly - AI-Powered Learning Platform

An educational technology platform built with Django that provides personalized learning experiences powered by artificial intelligence.

## Features

- **User Authentication**: Secure sign-up and sign-in functionality with password hashing
- **Personalized Dashboard**: Track your learning progress and view recommended courses
- **Subject Management**: Browse and enroll in various subjects (Python, Maths, DBMS, etc.)
- **Session Tracking**: Monitor your study sessions and time spent learning
- **AI Recommendations**: Get personalized course recommendations based on your progress

## Tech Stack

- **Backend**: Django 5.2.9
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript (embedded)
- **Package Manager**: uv

## Project Structure

```
EduTech/
├── EduTech/                 # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── website/                 # Main application
│   ├── models.py           # Database models (User, Subject, Session, Recommendation)
│   ├── views.py            # View functions and API endpoints
│   ├── templates/          # HTML templates
│   │   ├── index.html      # Landing page
│   │   ├── auth.html       # Login/Signup page
│   │   └── dashboard.html  # User dashboard
│   ├── static/website/     # Static files (CSS, JS)
│   └── migrations/         # Database migrations
├── db.sqlite3              # SQLite database
├── manage.py               # Django management script
└── README.md
```

## Database Models

- **User**: Stores user credentials and profile information
- **Subject**: Available learning subjects with slug and title
- **Session**: Tracks user learning sessions with subject and timestamps
- **Recommendation**: Personalized course recommendations for users

## Installation

### Using uv (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/dheepakshakthi/EduTech.git
   cd EduTech
   ```

2. **Install dependencies using uv**
   ```bash
   uv sync
   ```

3. **Run database migrations**
   ```bash
   uv run manage.py migrate
   ```

4. **Start the development server**
   ```bash
   uv run manage.py runserver
   ```

5. **Access the application**
   Open your browser and navigate to `http://127.0.0.1:8000`

### Using pip

1. **Clone the repository**
   ```bash
   git clone https://github.com/dheepakshakthi/EduTech.git
   cd EduTech
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install django
   ```

5. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   Open your browser and navigate to `http://127.0.0.1:8000`

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Landing page |
| `/auth/` | GET | Authentication page (login/signup) |
| `/dashboard/` | GET | User dashboard |
| `/api/signup/` | POST | User registration |
| `/api/login/` | POST | User login |
| `/api/dashboard/stats/` | GET | Dashboard statistics |
| `/api/sessions/recent/` | GET | Recent learning sessions |
| `/api/recommendations/` | GET | User recommendations |

## Usage

1. Visit the landing page and click "Get Started" to create an account
2. Fill in your details (name, email, age, password) to sign up
3. After registration, you'll be redirected to your personalized dashboard
4. Browse available subjects and track your learning progress
5. View recommendations tailored to your learning journey

## Development

### Creating a new migration
```bash
uv run manage.py makemigrations
uv run manage.py migrate
```

### Running the Django shell
```bash
uv run manage.py shell
```

### Creating a superuser for admin access
```bash
uv run manage.py createsuperuser
```
