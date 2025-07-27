from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import json

app = FastAPI(title="Smart Study Scheduler API")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class Subject(BaseModel):
    name: str
    priority: int

class ScheduleData(BaseModel):
    duration: str
    dailyTime: int
    subjects: List[Subject]
    generatedAt: str

class CompletedTopic(BaseModel):
    id: int
    subject: str
    topic: str
    completedDate: str
    nextRevision: str
    revisionCount: int

# In-memory storage (replace with database later)
stored_schedules = []
stored_completed_topics = []

@app.get("/")
def read_root():
    return {"message": "Smart Study Scheduler API is running!"}

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}

@app.post("/api/schedule")
def save_schedule(schedule_data: ScheduleData):
    stored_schedules.append(schedule_data.dict())
    return {"message": "Schedule saved successfully", "data": schedule_data}

@app.get("/api/schedule")
def get_schedules():
    return stored_schedules

@app.post("/api/completed-topics")
def save_completed_topic(topic: CompletedTopic):
    stored_completed_topics.append(topic.dict())
    return {"message": "Completed topic saved successfully", "data": topic}

@app.get("/api/completed-topics")
def get_completed_topics():
    return stored_completed_topics