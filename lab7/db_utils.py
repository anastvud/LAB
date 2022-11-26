from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=create_engine('mysql+pymysql://root:Busy18being@localhost/travelLab', echo=True))
session = Session()


def create_entry(model_class, *, commit=True, **kwargs):
    entry = model_class(**kwargs)
    session.add(entry)
    if commit:
        session.commit()
    return entry


def update_entry(entry, *, commit=True, **kwargs):
    for key, value in kwargs.items():
        setattr(entry, key, value)
    if commit:
        session.commit()
    return entry

def json_error(msg, code):
    return {'error': {'code': code, 'message': msg}}, code


class errors:
    not_found = json_error('Not found', 404)
    not_found1 = json_error("User doesn't exist", 404)
    bad_request = json_error('Invalid request', 400)
    val_exc = json_error('Validation exception', 405)
    exists = json_error('Forbidden. Already exists', 403)
    no_access = json_error('Forbidden. No rights to access', 403)
    no_auth = json_error('Authorization is not successful', 401)