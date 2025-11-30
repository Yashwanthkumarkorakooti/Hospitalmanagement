from datetime import datetime 
from typing import Optional 

def parse_int(value: str) -> Optional[int]:
    try:
        v = int(value)
        return v 
    except ValueError :
        raise ValueError(f'Invalid Integer: {value}')
    
def parse_datetime(value: str) -> datetime:
    fmts = ['%Y-%m-%d %H:%M', '%Y-%m-%d', '%d-%m-%Y %H:%M',  '%d-%m-%Y']
    for f in fmts:
        try:
            return datetime.strptime(value,f)
        except ValueError :
            continue
    raise ValueError(f'Invalid datetime. Expected formats: {fmts}')
