import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

import socketio

# Load environment variables
load_dotenv()

# Import routes
from routes import auth, users, ideas, votes, comments, support, messages, notifications, search, reports, admin, ai

# Initialize FastAPI App
app = FastAPI(
    title="Nexora API",
    description="Backend API for Nexora - A hyper-local idea sharing and community networking platform.",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Socket.io
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
socket_app = socketio.ASGIApp(sio, app)

# Mount Socket.io app
app.mount("/ws", socket_app)

# Register Routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(ideas.router, prefix="/ideas", tags=["Ideas"])
app.include_router(votes.router, prefix="/ideas", tags=["Votes"]) # Mounted under ideas logically but conceptually votes
app.include_router(comments.router, tags=["Comments"]) # Handled individually inside
app.include_router(support.router, tags=["Support Pledges"])
app.include_router(messages.router, prefix="/messages", tags=["Messages"])
app.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])
app.include_router(search.router, prefix="/search", tags=["Search"])
app.include_router(reports.router, prefix="/reports", tags=["Reports"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(ai.router, prefix="/ai", tags=["AI Integration"])

@app.get("/")
def root():
    return {"message": "Welcome to Nexora API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Socket.io events
@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")

@sio.event
async def message(sid, data):
    # Basic ping/pong test or message format check
    print(f"Message from {sid}: {data}")
    await sio.emit('reply', room=sid, data={'message': 'Received'})
