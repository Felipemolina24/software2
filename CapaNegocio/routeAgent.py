from CapaDatos import models


def route_query(user_query):
    # Ejemplo simple de enrutamiento basado en palabras clave
    if "politica" in user_query.lower() or "cancelación" in user_query.lower():
        return (
            models.ChatStatus.status2
        )  # Suponiendo que este status corresponde al PolicyPricesAgent
    elif "precio" in user_query.lower() or "costo" in user_query.lower():
        return models.ChatStatus.status2  # Usando el mismo agente para ejemplo
    else:
        return models.ChatStatus.status1  # Default al agente estándar de agendamiento
