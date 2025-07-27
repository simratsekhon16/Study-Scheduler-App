import os
from database import database
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
import asyncpg

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:simratdatabase@localhost:5432/study_scheduler_db")

# Create database instance
database = database(DATABASE_URL)
metadata = MetaData()

# Define tables
schedules_table = Table(
    "schedules",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("duration", String(50)),
    Column("daily_time", Integer),
    Column("subjects", Text),  # We'll store JSON string here
    Column("generated_at", String(100)),
    Column("created_at", DateTime, server_default=func.now())
)

completed_topics_table = Table(
    "completed_topics",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("subject", String(100)),
    Column("topic", String(200)),
    Column("completed_date", String(50)),
    Column("next_revision", String(50)),
    Column("revision_count", Integer),
    Column("created_at", DateTime, server_default=func.now())
)

# Create engine for table creation
engine = create_engine(DATABASE_URL)

# Function to create tables
def create_tables():
    metadata.create_all(engine)

# Database connection functions
async def connect_db():
    await database.connect()

async def disconnect_db():
    await database.disconnect()