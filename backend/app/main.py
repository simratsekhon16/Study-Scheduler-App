from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import json
import os
from database import database, schedules_table, completed_topics_table, create_tables, connect_db, disconnect_db

app = FastAPI(title="Smart Study Scheduler API")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://simratsekhon16.github.io",
        "http://localhost:3000"
    ],
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

# Startup and shutdown events
@app.on_event("startup")
async def startup():
    # Create tables if they don't exist
    create_tables()
    # Connect to database
    await connect_db()

@app.on_event("shutdown")
async def shutdown():
    await disconnect_db()

@app.get("/")
def read_root():
    return {"message": "Smart Study Scheduler API is running with PostgreSQL!"}

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "database": "connected"}

@app.post("/api/schedule")
async def save_schedule(schedule_data: ScheduleData):
    try:
        # Convert subjects list to JSON string for storage
        subjects_json = json.dumps([subject.dict() for subject in schedule_data.subjects])
        
        query = schedules_table.insert().values(
            duration=schedule_data.duration,
            daily_time=schedule_data.dailyTime,
            subjects=subjects_json,
            generated_at=schedule_data.generatedAt
        )
        
        result = await database.execute(query)
        return {"message": "Schedule saved successfully", "id": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving schedule: {str(e)}")

@app.get("/api/schedule")
async def get_schedules():
    try:
        query = schedules_table.select()
        results = await database.fetch_all(query)
        
        # Convert results to proper format
        schedules = []
        for row in results:
            schedule = {
                "id": row["id"],
                "duration": row["duration"],
                "dailyTime": row["daily_time"],
                "subjects": json.loads(row["subjects"]),
                "generatedAt": row["generated_at"],
                "createdAt": str(row["created_at"])
            }
            schedules.append(schedule)
        
        return schedules
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching schedules: {str(e)}")

@app.post("/api/completed-topics")
async def save_completed_topic(topic: CompletedTopic):
    try:
        query = completed_topics_table.insert().values(
            subject=topic.subject,
            topic=topic.topic,
            completed_date=topic.completedDate,
            next_revision=topic.nextRevision,
            revision_count=topic.revisionCount
        )
        
        result = await database.execute(query)
        return {"message": "Completed topic saved successfully", "id": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving completed topic: {str(e)}")

@app.get("/api/completed-topics")
async def get_completed_topics():
    try:
        query = completed_topics_table.select()
        results = await database.fetch_all(query)
        
        # Convert results to proper format
        topics = []
        for row in results:
            topic = {
                "id": row["id"],
                "subject": row["subject"],
                "topic": row["topic"],
                "completedDate": row["completed_date"],
                "nextRevision": row["next_revision"],
                "revisionCount": row["revision_count"],
                "createdAt": str(row["created_at"])
            }
            topics.append(topic)
        
        return topics
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching completed topics: {str(e)}")

# For deployment
if __name__ == "__main__":
    import uvicorn
    PORT = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=PORT)