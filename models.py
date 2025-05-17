#
# <one line to give the program's name and a brief idea of what it does.>
# SPDX-FileCopyrightText: 2025 <copyright holder> <email>
# SPDX-License-Identifier: GPL-3.0-or-later
#


from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum

# Enumerations
class InitiativeType(str, Enum):
    project = "project"
    operation = "operation"

class InitiativeStatus(str, Enum):
    proposal = "proposal"
    active = "active"
    completed = "completed"
    maintenance = "maintenance"
    ongoing = "ongoing"
    canceled = "canceled"

class PriorityLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    emergency = "emergency"

class TaskStatus(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    review = "review"
    done = "done"

class AgentType(str, Enum):
    human = "human"
    llm = "llm"
    solver = "solver"
    bulk_processor = "bulk_processor"
    custom = "custom"

class AgentFamily(str, Enum):
    qwen = "qwen"
    mistral = "mistral"
    llama = "llama"
    other = "other"

# Competency junction table
class Competency(SQLModel, table=True):
    agent_id: str = Field(foreign_key="agent.id", primary_key=True)
    domain:   str = Field(primary_key=True, description="Subject area")

class Initiative(SQLModel, table=True):
    id:             str                  = Field(primary_key=True)
    title:          str
    description:    Optional[str]        = None
    type:           InitiativeType
    status:         InitiativeStatus
    priority:       PriorityLevel
    custom_interval: Optional[str]       = Field(default=None, description="ISO 8601 or RRULE override")
    tasks:          List["Task"]         = Relationship(back_populates="initiative")

class Task(SQLModel, table=True):
    id:                  str                = Field(primary_key=True)
    initiative_id:       str                = Field(foreign_key="initiative.id", index=True)
    title:               str
    status:              TaskStatus
    due_date:            Optional[datetime] = None
    review_interval:     Optional[str]      = Field(default=None, description="ISO 8601 or RRULE")
    last_reviewed:       Optional[datetime] = None
    next_review:         Optional[datetime] = None
    initiative_priority: PriorityLevel      = Field(description="Snapshot at creation")
    initiative:          Initiative         = Relationship(back_populates="tasks")

class Agent(SQLModel, table=True):
    id:            str              = Field(primary_key=True)
    type:          AgentType
    family:        AgentFamily
    version:       str              = Field(description="Model/config version")
    domain:        str
    status:        str              = Field(description="idle|busy|error")
    competencies:  List[Competency] = Relationship(back_populates="agent")

class Asset(SQLModel, table=True):
    id:       str               = Field(primary_key=True)
    type:     str
    metadata: Optional[dict]    = Field(default_factory=dict)

class Document(SQLModel, table=True):
    id:             str               = Field(primary_key=True)
    initiative_id:  str               = Field(foreign_key="initiative.id", index=True)
    agent_id:       Optional[str]     = Field(default=None, index=True)
    doc_type:       str               = Field(description="mission_statement|correspondence|report|deliverable")
    title:          str
    description:    Optional[str]     = None
    created_at:     datetime          = Field(default_factory=datetime.utcnow)
    updated_at:     datetime          = Field(default_factory=datetime.utcnow)
    file_path:      Optional[str]     = Field(description="URL or FS path to artifact")
