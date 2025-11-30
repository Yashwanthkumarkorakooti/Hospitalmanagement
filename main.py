from database import initialize_db 
from services import PatientService, DoctorService, AppointmentService

def print_menu():
    print('\n --- Hospital Management ---')
    print("1. Add Patient")
    print("2. View Patients")
    print("3. Search Patients")
    print("4. Update Patient")
    print("5. Delete Patient")
    print("6. Add Doctor")
    print("7. View Doctors")
    print("8. Search Doctors by Specialty")
    print("9. Schedule Appointment")
    print("10. View Upcoming Appointments")
    print("11. View Appointments (detailed)")
    print("12. Cancel Appointment")
    print("0. Exit")

def main():
    initialize_db()
    
    while True:
        print_menu()
        ch = input('Enter choice: ').strip()
        
        try:
            if ch == '1' :
                name = input('Name: ')
                age = input('Age: ')
                gender = input('Gender: ')
                pid = PatientService.create(name,age,gender)
                print(f'✅ Patient added with Id: {pid}') 
                
            elif ch == '2':
                patients = PatientService.list_all()
                if not patients:
                    print('No patients found')
                for p in patients:
                    print(p) 
                    
            elif ch == '3':
                q = input('Search name substring: ')
                results = PatientService.search(q)
                for r in results:
                    print(r)
                    
            elif ch == '4':
                pid = input("ID: ")
                name = input("Name: ")
                age = input("Age: ")
                gender = input("Gender: ")
                
                ok = PatientService.update(int(pid), name, age, gender)
                print('✅ Updated' if ok else '❌ Not Found')

            elif ch == '5':
                pid = input('Id to delete')
                ok = PatientService.delete(int(pid))
                print('✅ Deleted' if ok else '❌ Not Found')
                
            elif ch == '6':
                name = input("Name: ")
                specialty = input("Specialty: ")
                did = DoctorService.create(name,specialty)
                print(f'✅ Doctor added with Id : {did}')
                
            elif ch == '7':
                doctors = DoctorService.list_all()
                if not doctors:
                    print("No doctors found")
                else:
                    for d in doctors:
                        print(d)
                    
            elif ch == '8':
                q = input('Speciality substring: ')
                for d in DoctorService.search(q):
                    print(d)
                    
            elif ch == '9':
                print("Provide patient_id, doctor_id and datetime (YYYY-MM-DD HH:MM)")
                pid = input("Patient ID: ")
                did = input("Doctor ID: ")
                dt = input("Scheduled At: ")
                notes = input("Notes (optional): ")
                
                aid = AppointmentService.schedule(pid,did,dt,notes)
                print(f'✅ Appointment scheduled (ID: {aid})')

            elif ch == '10':
                for a in AppointmentService.list_upcoming():
                    print(a)
                
            elif ch == '11':
                for d in AppointmentService.list_detailed():
                    print(d)
                     
            elif ch == '12':
                aid = input('Appointment ID to cancel: ')
                ok = AppointmentService.cancel(aid)
                print('✅ Cancelled' if ok else '❌ Not found')
                
            elif ch == '0':
                break
            
            else:
                print('Invalid Option')
                
        except Exception as e :
            print(f'Error: {e}')
            
if __name__ == '__main__':
    main()