import pytest
from datetime import datetime, timedelta
from agenda import GoogleCalendarManager


@pytest.fixture(scope="module")
def calendar_manager():
    return GoogleCalendarManager()


def test_full_user_flow(calendar_manager):
    # Datos de entrada
    patient_name = "Juan Pérez"
    patient_age = 34
    patient_motive = "Chequeo anual"
    patient_id = 987654321
    start_time = (datetime.now() + timedelta(days=1)).replace(
        hour=10, minute=0, second=0, microsecond=0
    ).isoformat() + "Z"
    end_time = (datetime.now() + timedelta(days=1, hours=1)).replace(
        hour=11, minute=0, second=0, microsecond=0
    ).isoformat() + "Z"
    description = "Chequeo anual general"
    patient_info = {
        "name": patient_name,
        "age": patient_age,
        "motive": patient_motive,
        "id_patient": patient_id,
        "appointment_time": start_time,
    }

    # Agregar evento al calendario y registrar al paciente
    event_added_successfully = calendar_manager.add_event(
        "Consulta con Juan Pérez", start_time, end_time, description, patient_info
    )

    # Verificación de que el evento fue agregado y el paciente registrado correctamente
    assert (
        event_added_successfully
    ), "El evento debería haber sido agregado correctamente"

    # Búsqueda de paciente en la base de datos para verificación
    patient_record = calendar_manager.db.find_patient(patient_id)
    assert (
        patient_record
    ), "El registro del paciente debería existir en la base de datos"
    assert (
        patient_record["name"] == patient_name
    ), "El nombre del paciente debe coincidir"
    assert patient_record["age"] == patient_age, "La edad del paciente debe coincidir"


@pytest.fixture(autouse=True)
def clean_up(calendar_manager):
    # Limpia los datos de prueba del calendario y la base de datos
    # Asume que tienes métodos para limpiar los datos correctamente
    pass
