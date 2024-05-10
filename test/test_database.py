import pytest
from CapaDatos.database import MongoDatabase
from bson import ObjectId


# Configuración de la base de datos de prueba
@pytest.fixture(scope="module")
def db():
    test_uri = "mongodb+srv://felipemolina:admin@edya2.zgsyghc.mongodb.net"
    test_dbname = "Software2"
    return MongoDatabase(uri=test_uri, dbname=test_dbname)


def test_add_patient(db):
    name = "Test Patient"
    age = 30
    motive = "Consulta de prueba"
    id_patient = 123456
    appointment_time = "2024-05-05 10:00"
    result = db.add_patient(name, age, motive, id_patient, appointment_time)
    assert isinstance(result, ObjectId)


def test_find_patient(db):
    id_patient = 123456  #  ID existente en la base de datos
    patient = db.find_patient(id_patient)
    assert patient is not None
    assert patient["name"] == "Test Patient"
    assert patient["age"] == 30
