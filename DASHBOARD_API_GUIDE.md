# API Endpoints Testing Guide

## Dynamic Dashboard Features Implemented

### 1. Study Streak API
**Endpoint:** `/dashboard/study-streak/?email=test@example.com`

**Features:**
- Calculates current streak (consecutive days studied)
- Calculates longest streak
- Returns weekly chart data (last 7 days)
- Dynamic streak messages

**Response Example:**
```json
{
  "success": true,
  "study_streak": {
    "current_streak_days": 5,
    "longest_streak_days": 5,
    "last_active_date": "2026-01-21",
    "weekly_data": [
      {"day": "Mon", "minutes": 35, "date": "2026-01-16"},
      {"day": "Tue", "minutes": 48, "date": "2026-01-17"},
      ...
    ],
    "streak_message": "You are on a 5-day learning streak. Keep going!"
  }
}
```

### 2. Focus Analysis API
**Endpoint:** `/dashboard/focus-analysis/?email=test@example.com`

**Features:**
- Analyzes study sessions to find preferred time
- Calculates average session duration
- Calculates focus score (High/Medium/Low)
- Provides personalized focus message

**Response Example:**
```json
{
  "success": true,
  "focus_analysis": {
    "preferred_study_time": "Evening (7 PM – 9 PM)",
    "average_session_minutes": 52,
    "focus_score": "High",
    "focus_score_value": 8.1,
    "focus_message": "You typically focus best around 8:00 PM. Try to start your session before then today."
  }
}
```

## Testing Instructions

1. **Start the server:**
   ```bash
   python manage.py runserver
   ```

2. **Login with test user:**
   - Email: `test@example.com`
   - The dashboard will automatically fetch dynamic data

3. **Test API endpoints directly:**
   ```bash
   # Test Study Streak
   curl "http://127.0.0.1:8000/dashboard/study-streak/?email=test@example.com"
   
   # Test Focus Analysis
   curl "http://127.0.0.1:8000/dashboard/focus-analysis/?email=test@example.com"
   ```

4. **View data in Django Admin:**
   - Go to: http://127.0.0.1:8000/admin/
   - You can now manage StudyStreak and FocusSession records

## What's Updated

### Database Models
- ✅ `StudyStreak` model - tracks daily study minutes and tasks
- ✅ `FocusSession` model - tracks study sessions with timing and scores

### API Endpoints
- ✅ `/dashboard/study-streak/` - now dynamic (fetches from DB)
- ✅ `/dashboard/focus-analysis/` - now dynamic (fetches from DB)

### Dashboard UI
- ✅ Automatically fetches streak data on page load
- ✅ Updates streak counter dynamically
- ✅ Updates weekly chart with real data
- ✅ Updates focus analysis message
- ✅ Shows best streak comparison

### Sample Data
- ✅ 7 days of study streak records
- ✅ 9 focus session records
- ✅ Test user: Sam (test@example.com)

## Next Steps

To add more data or modify existing data:
1. Run `python populate_dashboard_data.py` again
2. Or use Django admin to manually add/edit records
3. Or create more users and add their data

Enjoy your dynamic dashboard! 🎉
