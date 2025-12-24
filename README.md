# Learnly - AI-Powered Learning Platform

An educational technology platform built with Django that provides personalized learning experiences powered by artificial intelligence.

## Features

- **User Authentication**: Secure sign-up and sign-in functionality with password hashing
- **Personalized Dashboard**: Track your learning progress and view recommended courses
- **Subject Management**: Browse and enroll in various subjects (Python, Maths, DBMS, etc.)
- **Session Tracking**: Monitor your study sessions and time spent learning
- **AI Recommendations**: Get personalized course recommendations based on your progress
- **AI Chat History**: Save and manage multiple AI chat conversations with persistence

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
- **Conversation**: Stores metadata for AI chat sessions per user
- **Message**: Individual chat messages (User/Assistant/System) within a conversation

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

## AI Chat Configuration

To use the AI-powered chat feature, you must have Ollama installed and the correct model loaded.

### CLI Setup
1. **Install Ollama**: Download from [ollama.com](https://ollama.com).
2. **Pull the Model**: Run the following command to download the Gemma model:
   ```bash
   ollama pull gemma3:4b
   ```
3. **Run the Server**: Ensure Ollama is running (default port 11434).
   ```bash
   ollama serve
   ```

### Client Usage
You can also chat with the model directly from the command line to verify it works:
```bash
ollama run gemma3:4b
```

### Configuration in Code
To change the model or inference device, modify the `chatbot_api` function in `website/views.py`:

- **Model**: Update the `"model"` key in the `payload` dictionary (e.g., `"model": "llama3"`).
- **GPU Acceleration**: Adjust `"num_gpu"` in the `"options"` dictionary:
    - `0`: Use CPU only.
    - `1`: Enable GPU acceleration (requires compatible hardware and Ollama configuration).
- **Response Length**: Adjust `"num_predict"` to control the maximum number of tokens generated.

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Landing page |
| `/auth/` | GET | Authentication page (login/signup) |
| `/dashboard/` | GET | User dashboard |
| `/chatbot/` | GET | AI Chatbot interface |
| `/api/signup/` | POST | User registration |
| `/api/login/` | POST | User login |
| `/api/dashboard/stats/` | GET | Dashboard statistics |
| `/api/sessions/recent/` | GET | Recent learning sessions |
| `/api/recommendations/` | GET | User recommendations |
| `/api/chatbot/` | POST | Get AI response from Ollama |
| `/api/conversations/` | GET/POST/DELETE | Manage chat history |
| `/api/messages/` | GET | Load messages for a conversation |

## Usage

1. Visit the landing page and click "Get Started" to create an account
2. Fill in your details (name, email, age, password) to sign up
3. After registration, you'll be redirected to your personalized dashboard
4. Browse available subjects and track your learning progress
5. View recommendations tailored to your learning journey
6. Access the **AI Chat** from the sidebar to ask questions and save your conversation history

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
