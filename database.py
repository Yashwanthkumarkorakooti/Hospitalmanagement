import os 
import time 
import pyodbc
from dotenv import load_dotenv
from contextlib import contextmanager 

load_dotenv()

DRIVER = os.getenv('DB_DRIVER','{ODBC Driver 17 for SQL Server}')
DATABASE = os.getenv('DB_NAME','HospitalDB')
SERVER = os.getenv('DB_SERVER', 'localhost')
ENCRYPT = os.getenv('ENCRYPT', 'no')


CONN_STR_TEMPLATE = (
    'DRIVER={driver};'
    'SERVER={server};'
    'DATABASE={database};'
    'Trusted_Connection=Yes;'
    'Encrypt={encrypt};'
    'TrustServerCertificate=yes'
)

def _build_conn_str(server=SERVER, database=DATABASE):
    return CONN_STR_TEMPLATE.format(
        driver=DRIVER ,
        server=server ,
        database=database,
        encrypt=ENCRYPT 
    )

@contextmanager
def get_connection(server: str = SERVER ,database : str = DATABASE , max_retries : int = 3 , retry_delay : float = 1.0):
    attempt = 0 
    last_exc = None
    
    while attempt < max_retries :
        try :
            conn = pyodbc.connect(_build_conn_str(server=server, database=database))
            try :
                yield conn 
            finally:
                try :
                    conn.close()
                except :
                    pass 
            return 
        except Exception as e :
            attempt += 1 
            last_exc = e 
            time.sleep(retry_delay)
    raise last_exc
    
def initialize_db():
    master_conn_str = _build_conn_str(server=SERVER, database='master')

    with pyodbc.connect(master_conn_str, autocommit=True) as conn:
        cur = conn.cursor()
        cur.execute('SELECT 1 FROM sys.databases WHERE name = ?', (DATABASE,))
        row = cur.fetchone()

        if not row:
            cur.execute(f'CREATE DATABASE [{DATABASE}]')

    with get_connection(server=SERVER, database=DATABASE) as conn:
        cur = conn.cursor()

        cur.execute('''
            IF NOT EXISTS(
                SELECT 1 FROM information_schema.tables WHERE table_name = 'patients'
            )
            CREATE TABLE patients(
                id INT IDENTITY(1,1) PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                age INT NULL,
                gender VARCHAR(20) NULL,
                created_at DATETIME2 DEFAULT GETDATE()
            )
        ''')

        cur.execute('''
            IF NOT EXISTS(
                SELECT 1 FROM information_schema.tables WHERE table_name = 'doctors'
            )
            CREATE TABLE doctors(
                id INT IDENTITY(1,1) PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                specialty VARCHAR(100) NULL,
                created_at DATETIME2 DEFAULT GETDATE()
            )
        ''')

        cur.execute('''
            IF NOT EXISTS(
                SELECT 1 FROM information_schema.tables WHERE table_name = 'appointments'
            )
            CREATE TABLE appointments(
                id INT IDENTITY(1,1) PRIMARY KEY,
                patient_id INT NOT NULL,
                doctor_id INT NOT NULL,
                scheduled_at DATETIME2 NOT NULL,
                notes VARCHAR(500) NULL,
                created_at DATETIME2 DEFAULT GETDATE(),
                CONSTRAINT FK_App_Patient FOREIGN KEY (patient_id) REFERENCES patients(id),
                CONSTRAINT FK_App_Doctor FOREIGN KEY (doctor_id) REFERENCES doctors(id)
            )
        ''')

        conn.commit()
