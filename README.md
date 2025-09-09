# Overview
Event management system api is a system built using django and django rest framework, it helps in planning and coordination
of events.

# Features 
- Authentication. The user can register, login and logout 
- The users can create, update and delete events.
- Users can also register new events and add comments on upcoming events.
- Permissions, there is different permissions for participants and organisers.

# Registering a new user 
POST http://127.0.0.1:8000/api/register/

{
    "username": "Kipkorir",
    "email": "kipkorir@example.com",
    "password": "StrongPassword123",
    "confirm_password": "StrongPassword123"
}


# login 
POST http://127.0.0.1:8000/api/login/

{
    "username": "newuser",
    "password": "StrongPassword123"
}

# registering a new event
POST http://127.0.0.1:8000/api/events/

{
    "title": "Alx Graduation",
    "location": "Nairobi",
    "date_time": "2025-9-45",
    "capacity": "4000"
}

# Adding comments
POST http://127.0.0.1:8000/api/comments/

{
    "event": "Alx Graduation",
    "text": "Congratulations to you all",
}


# API Endpoints.
POST	/api/register/ - Register a new user.
POST	/api/login/ - User login & get token.
GET	/api/events/ - List all events.
POST	/api/events/ - Create a new event.
GET	/api/events/{id}/ - Retrieve event details.
PUT	/api/events/{id}/ - Update an event.
DELETE	/api/events/{id}/ - Delete an event.
POST	/api/comments/ - Add a comment to an event.
