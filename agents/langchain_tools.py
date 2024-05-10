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
