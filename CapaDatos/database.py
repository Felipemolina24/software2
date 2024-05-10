from pymongo import MongoClient, IndexModel, ASCENDING
from pymongo.collection import Collection
from pymongo.database import Database
import pymongo.errors as mongo_errors


class MongoDatabase:
    def __init__(self, uri: str, dbname: str):
        self.client: MongoClient = MongoClient(uri)
        self.db: Database = self.client[dbname]
        self.patients: Collection = self.db["patients"]

    def add_patient(
        self, name: str, age: int, motive: str, id_patient: int, appointment_time: str
    ):
        """Agrega un nuevo paciente a la base de datos."""
        try:
            patient_data = {
                "name": name,
                "age": age,
                "motive": motive,
                "id_patient": id_patient,
                "appointment_time": appointment_time,
            }
            result = self.patients.insert_one(patient_data)
            return result.inserted_id
        except mongo_errors.PyMongoError as e:
            print(f"Error adding patient: {e}")
            return None

    def find_patient(self, id_patient: int):
        """Busca un paciente por id."""
        try:
            return self.patients.find_one({"id_patient": id_patient})
        except mongo_errors.PyMongoError as e:
            print(f"Error finding patient: {e}")
            return None


db = MongoDatabase(
    uri="mongodb+srv://felipemolina:admin@edya2.zgsyghc.mongodb.net", dbname="Software2"
)


# Buscar un paciente
patient = db.find_patient(id_patient=1193246904)
print(patient)
