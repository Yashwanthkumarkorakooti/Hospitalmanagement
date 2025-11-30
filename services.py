from repositories import PatientRepository,DoctorRepository,AppointmentRepository
from models import Patient,Doctor,Appointment 
from utils import parse_int , parse_datetime
from typing import Optional
from datetime import datetime 


    # --- Patient Service --- #

class PatientService:
    @staticmethod
    def create(name: str, age_raw: str, gender: str) -> int :
        age = parse_int(age_raw)
        if age <= 0:
            raise ValueError("Age must be a positive integer")
        
        if not name.strip():
            raise ValueError("Name cannot be empty")
        
        g = gender.strip()
        if g not in ("M","F","Other","O"):
            raise ValueError("Gender must be M, F, or Other")

        p = Patient(
            id=None,
            name=name.strip(),
            age=age,
            gender=gender.strip() or None
        )

        return PatientRepository.add(p)
    
    @staticmethod
    def list_all():
        return PatientRepository.list_all()
    
    @staticmethod
    def get_by_id(pid: int) -> Optional[Patient]:
        return PatientRepository.get_by_id(pid)
    
    @staticmethod
    def search(name_substr: str):
        return PatientRepository.search_by_name(name_substr)
    
    @staticmethod
    def update(pid: int, name: str, age_raw: str, gender: str) -> bool:
        age = parse_int(age_raw)
        if age <= 0:
            raise ValueError("Age must be a positive integer")
        
        if not name.strip():
            raise ValueError("Name cannot be empty")
        
        g = gender.strip()
        if g not in ("M","F","Other","O"):
            raise ValueError("Gender must be M, F, or Other")

        p = Patient(
            id=pid,
            name=name.strip(),
            age=age,
            gender=gender.strip() or None
        )
        return PatientRepository.update(p)

    @staticmethod
    def delete(pid: int) -> bool:
        return PatientRepository.delete(pid)
    
    
    # --- Doctor Service --- #

class DoctorService:
    @staticmethod
    def create(name: str, specialty: str) -> int:
        if not name.strip():
            raise ValueError("Doctor name cannot be empty")

        if not specialty.strip():
            raise ValueError("Specialty cannot be empty")

        d = Doctor(
            id=None,
            name=name.strip(),
            specialty=specialty.strip()  # ✔ CORRECT
        )
        return DoctorRepository.add(d)

    @staticmethod
    def list_all():
        return DoctorRepository.list_all()

    @staticmethod
    def get_by_id(did: int) -> Optional[Doctor]:
        return DoctorRepository.get_by_id(did)

    @staticmethod
    def search(spec_substr: str):
        return DoctorRepository.search_by_specialist(spec_substr)

    @staticmethod
    def update(did: int, name: str, specialty: str) -> bool:
        if not name.strip():
            raise ValueError("Doctor name cannot be empty")

        if not specialty.strip():
            raise ValueError("Specialty cannot be empty")

        d = Doctor(
            id=did,
            name=name.strip(),
            specialty=specialty.strip()   # ✔ CORRECT
        )
        return DoctorRepository.update(d)

    @staticmethod
    def delete(did: int) -> bool:
        return DoctorRepository.delete(did)

    
    
        # --- Appointment Service --- # 
        
class AppointmentService :
    @staticmethod
    def schedule(patient_id_raw: str, doctor_id_raw: str, dt_raw: str, notes:str=None) -> int :
        pid = parse_int(patient_id_raw)
        did = parse_int(doctor_id_raw)
        scheduled = parse_datetime(dt_raw)
        
        if pid <= 0:
            raise ValueError("Invalid patient id")
        
        if did <= 0:
            raise ValueError("Invalid doctor id")
        
        if scheduled < datetime.now():
            raise ValueError('Cannot schedule an appointment in the past')
        
        appt = Appointment(id= None,patient_id=pid , doctor_id=did,scheduled_at=scheduled,notes=notes)
        return AppointmentRepository.add(appt)
    
    @staticmethod
    def list_upcoming():
        return AppointmentRepository.list_all(upcoming_only=True)
    
    @staticmethod
    def list_detailed():
        return AppointmentRepository.get_detailed_list()
    
    @staticmethod
    def cancel(aid_raw: str) -> bool:
        aid = parse_int(aid_raw)
        if aid <= 0:
            raise ValueError("Invalid appointment id")
        return AppointmentRepository.delete(aid)