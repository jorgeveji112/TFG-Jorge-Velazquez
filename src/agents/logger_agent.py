from autogen import Agent, Message

class LoggerAgent(Agent):
    def __init__(self, name="LoggerAgent"):
        super().__init__(name=name)

    def receive(self, message: Message):
        print("=== Log de rutas generadas ===")
        rutas = message.data.get("routes", {})
        for estado, pedidos in rutas.items():
            print(f"{estado}: {len(pedidos)} pedidos")
        return None
