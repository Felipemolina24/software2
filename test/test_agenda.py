import pytest
from agenda import GoogleCalendarManager

# Configuración para las pruebas


@pytest.fixture(scope="module")
def calendar_manager():
    return GoogleCalendarManager()


def test_check_availability(calendar_manager):
    start_time = "2024-01-01T09:00:00Z"
    end_time = "2024-01-01T10:00:00Z"
    available = calendar_manager.check_availability(start_time, end_time)
    assert isinstance(available, bool)


def test_add_event(calendar_manager):
    summary = "Consulta de prueba"
    start_time = "2024-01-01T09:00:00Z"
    end_time = "2024-01-01T10:00:00Z"
    description = "Esta es una descripción de prueba"
    patient_info = {
        "name": "Paciente Prueba",
        "age": 30,
        "motive": "Consulta general",
        "id_patient": 123456789,
        "appointment_time": start_time,
    }
    success = calendar_manager.add_event(
        summary, start_time, end_time, description, patient_info
    )
    assert success is True  # evento agregado correctamente"


def test_get_upcoming_events(calendar_manager):
    events = calendar_manager.get_upcoming_events()
    assert isinstance(events, list)  # lista de eventos


def test_get_free_busy_agenda(calendar_manager):
    busy_info = calendar_manager.get_free_busy_agenda()
    assert isinstance(busy_info, dict)  # información en formato diccionario
