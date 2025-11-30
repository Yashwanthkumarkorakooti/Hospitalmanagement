from typing import List, Optional
from datetime import datetime
from database import get_connection
from models import Patient, Doctor, Appointment
import pyodbc


# -------------------- PATIENT REPOSITORY --------------------

class PatientRepository:

    @staticmethod
    def add(patient: Patient) -> int:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                'INSERT INTO patients (name, age, gender) VALUES (?, ?, ?)',
                (patient.name, patient.age, patient.gender)
            )
            conn.commit()
            cur.execute('SELECT CAST(SCOPE_IDENTITY() AS INT)')
            return cur.fetchone()[0]

    @staticmethod
    def list_all() -> List[Patient]:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute('SELECT id, name, age, gender, created_at FROM patients ORDER BY id')
            rows = cur.fetchall()
            return [Patient(*r) for r in rows]

    @staticmethod
    def get_by_id(pid: int) -> Optional[Patient]:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute('SELECT id, name, age, gender, created_at FROM patients WHERE id = ?', (pid,))
            row = cur.fetchone()
            return Patient(*row) if row else None

    @staticmethod
    def search_by_name(name_substr: str) -> List[Patient]:
        like = f'%{name_substr}%'
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                'SELECT id, name, age, gender, created_at FROM patients WHERE name LIKE ?',
                (like,)
            )
            rows = cur.fetchall()
            return [Patient(*r) for r in rows]

    @staticmethod
    def update(patient: Patient) -> bool:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                'UPDATE patients SET name = ?, age = ?, gender = ? WHERE id = ?',
                (patient.name, patient.age, patient.gender, patient.id)
            )
            conn.commit()
            return cur.rowcount > 0

    @staticmethod
    def delete(pid: int) -> bool:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute('DELETE FROM patients WHERE id = ?', (pid,))
            conn.commit()
            return cur.rowcount > 0



# -------------------- DOCTOR REPOSITORY --------------------

class DoctorRepository:

    @staticmethod
    def add(doctor: Doctor) -> int:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                'INSERT INTO doctors (name, specialty) VALUES (?, ?)',
                (doctor.name, doctor.specialty)
            )
            conn.commit()
            cur.execute('SELECT CAST(SCOPE_IDENTITY() AS INT)')
            return cur.fetchone()[0]

    @staticmethod
    def list_all() -> List[Doctor]:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute('SELECT id, name, specialty, created_at FROM doctors ORDER BY id')
            rows = cur.fetchall()
            return [Doctor(*row) for row in rows]

    @staticmethod
    def get_by_id(did: int) -> Optional[Doctor]:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute('SELECT id, name, specialty, created_at FROM doctors WHERE id = ?', (did,))
            row = cur.fetchone()
            return Doctor(*row) if row else None

    @staticmethod
    def search_by_specialist(spec_substr: str) -> List[Doctor]:
        like = f'%{spec_substr}%'
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                'SELECT id, name, specialty, created_at FROM doctors WHERE specialty LIKE ?',
                (like,)
            )
            rows = cur.fetchall()
            return [Doctor(*r) for r in rows]

    @staticmethod
    def update(doctor: Doctor) -> bool:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                'UPDATE doctors SET name = ?, specialty = ? WHERE id = ?',
                (doctor.name, doctor.specialty, doctor.id)
            )
            conn.commit()
            return cur.rowcount > 0

    @staticmethod
    def delete(did: int) -> bool:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute('DELETE FROM doctors WHERE id = ?', (did,))
            conn.commit()
            return cur.rowcount > 0



# -------------------- APPOINTMENT REPOSITORY --------------------

class AppointmentRepository:

    @staticmethod
    def add(appointment: Appointment) -> int:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                'INSERT INTO appointments (patient_id, doctor_id, scheduled_at, notes) VALUES (?, ?, ?, ?)',
                (appointment.patient_id, appointment.doctor_id, appointment.scheduled_at, appointment.notes)
            )
            conn.commit()
            cur.execute('SELECT CAST(SCOPE_IDENTITY() AS INT)')
            return cur.fetchone()[0]

    @staticmethod
    def list_all(upcoming_only: bool = False) -> List[Appointment]:
        with get_connection() as conn:
            cur = conn.cursor()
            if upcoming_only:
                cur.execute(
                    'SELECT id, patient_id, doctor_id, scheduled_at, notes, created_at '
                    'FROM appointments WHERE scheduled_at >= GETDATE() ORDER BY scheduled_at'
                )
            else:
                cur.execute(
                    'SELECT id, patient_id, doctor_id, scheduled_at, notes, created_at '
                    'FROM appointments ORDER BY scheduled_at DESC'
                )

            rows = cur.fetchall()
            return [Appointment(*r) for r in rows]

    @staticmethod
    def get_detailed_list():
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                '''SELECT a.id, p.id, p.name, d.id, d.name, a.scheduled_at, a.notes
                   FROM appointments a
                   JOIN patients p ON a.patient_id = p.id
                   JOIN doctors d ON a.doctor_id = d.id
                   ORDER BY a.scheduled_at'''
            )
            rows = cur.fetchall()
            return [
                {
                    'appointment_id': r[0],
                    'patient_id': r[1],
                    'patient_name': r[2],
                    'doctor_id': r[3],
                    'doctor_name': r[4],
                    'scheduled_at': r[5],
                    'notes': r[6]
                }
                for r in rows
            ]

    @staticmethod
    def delete(aid: int) -> bool:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute('DELETE FROM appointments WHERE id = ?', (aid,))
            conn.commit()
            return cur.rowcount > 0
