from CapaDatos.models import Chat, Message, SenderEnum, ChatStatus, _generate_id


def test_create_chat():
    chat = Chat()
    assert chat.messages == []
    assert isinstance(chat.status, ChatStatus)


def test_add_message_to_chat():
    chat = Chat()
    message = Message(sender=SenderEnum.HumanMessage, message="Hola")
    chat.messages.append(message)
    assert len(chat.messages) == 1
    assert chat.messages[0].message == "Hola"
    assert chat.messages[0].sender == SenderEnum.HumanMessage


def test_id_length():
    generated_id = _generate_id()
    assert len(generated_id) == 36  # generando UUIDs


def test_id_uniqueness():
    ids = {_generate_id() for _ in range(1000)}
    assert len(ids) == 1000  # Verifica que todos los IDs generados sean únicos
