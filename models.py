from dataclasses import dataclass
from datetime import datetime
from typing import Optional 

@dataclass
class Patient:
    id: Optional[int]
    name: str
    age: Optional[int]
    gender: Optional[str]
    created_at: Optional[datetime] = None 
    
@dataclass 
class Doctor:
    id: Optional[int]
    name: str
    specialty: Optional[str]
    created_at: Optional[datetime] = None 
    
@dataclass
class Appointment:
    id: Optional[int]
    patient_id: int 
    doctor_id: int
    scheduled_at: datetime
    notes: Optional[str] = None
    created_at: Optional[datetime] = None