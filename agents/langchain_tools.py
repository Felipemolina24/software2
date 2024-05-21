from typing import Type, Any, Optional
from datetime import datetime, timedelta

import pydantic
from langchain_core import (
    tools as langchain_core_tools,
    callbacks as langchain_core_callbacks,
)

from CapaDatos import models
from agenda import GoogleCalendarManager


class _PatientInfo(pydantic.BaseModel):
    name: str = pydantic.Field(..., description="Nombre del paciente")
    age: int = pydantic.Field(..., description="Edad del paciente")
    motive: str = pydantic.Field(..., description="Motivo de la consulta")
    start_time: str = pydantic.Field(..., description="Hora de la cita")
    id_patient: int = pydantic.Field(..., description="numero de identificacion")


class ProvideInfoTool(langchain_core_tools.BaseTool):
    name: str = "provide_info_tool"
    description: str = (
        "Proporciona información sobre políticas de atención y precios de consulta."
    )

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    def _run(
        self,
        *args,
        run_manager: Optional[langchain_core_tools.CallbackManagerForToolRun] = None,
        **kwargs,
    ) -> str:
        # Ignorar args y kwargs adicionales que podrían ser pasados por el sistema
        # Aquí puedes implementar lógica para buscar en una base de datos o configuración
        # Por ahora, simplemente devolvemos un mensaje estático
        return """
                Políticas de Atención:
                - Todas las citas deben ser reservadas con al menos 48 horas de antelación.
                - Se requiere un aviso de cancelación con 24 horas de anticipación para evitar cargos.
                - Las citas que no sean canceladas con al menos 24 horas de antelación serán sujetas a un cargo del 50% del costo de la consulta.
                - Los pacientes deben llegar al menos 15 minutos antes de su hora programada para completar el papeleo necesario.

                Precios:
                - El costo de la consulta en Colombia es de 150,000 pesos colombianos.
                - Para pacientes fuera de Colombia, el costo de la consulta es de 50 dólares estadounidenses.
                """


class SendPatientInfo(langchain_core_tools.BaseTool):
    """Tool that fetches active deployments."""

    name: str = "send_patient_info_to_professional"
    description: str = "Util cuando el paciente quiere agendar una cita con la doctora, para enviar informacion"
    args_schema: Type[pydantic.BaseModel] = _PatientInfo
    chat_history: Optional[models.Chat] = None
    return_direct = True

    def __init__(
        self, chat_history: Optional[models.Chat] = None, **kwargs: Any
    ) -> None:
        super().__init__(**kwargs)
        self.chat_history = chat_history

    def _run(
        self,
        name: str,
        age: int,
        id_patient: int,
        motive: str,
        start_time: str,
        run_manager: Optional[
            langchain_core_callbacks.CallbackManagerForToolRun
        ] = None,
    ) -> str:
        if self.chat_history:
            self.chat_history.status = models.ChatStatus.status2
            response = "Vale, regálame un momento."
            try:
                # Calcular tiempo de finalización (2 hora después del tiempo de inicio)
                start_time_dt = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
                end_time_dt = start_time_dt + timedelta(hours=1)
                # end_time = end_time_dt.isoformat()

                # Convertir a ISO 8601
                start_time_iso = start_time_dt.isoformat() + "Z"
                end_time_iso = (end_time_dt + timedelta(hours=1)).isoformat() + "Z"

                patient_info = {
                    "name": name,
                    "age": age,
                    "id_patient": id_patient,
                    "motive": motive,
                    "start_time": start_time_iso,
                }

                # Verificar disponibilidad
                calendar_manager = GoogleCalendarManager()
                if calendar_manager.check_availability(start_time_iso, end_time_iso):
                    # Agregar evento al calendario
                    calendar_manager.add_event(
                        summary=f"Cita con {name}",
                        start_time=start_time_iso,
                        end_time=end_time_iso,
                        description=f"Edad: {age}, Motivo: {motive}",
                        patient_info=patient_info,
                    )
                    response += " He agendado tu cita exitosamente."
                else:
                    response += (
                        " Lo siento, no hay disponibilidad en el horario seleccionado."
                    )
            except Exception as e:
                print(f"Error al agregar evento al calendario: {e}")
                response += " Ha ocurrido un error al agregar el evento al calendario."
            return response
