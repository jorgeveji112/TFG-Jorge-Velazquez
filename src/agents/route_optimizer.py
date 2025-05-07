from autogen import Agent, Message

class RouteOptimizerAgent(Agent):
    def __init__(self, name="RouteOptimizer"):
        super().__init__(name=name)

    def receive(self, message: Message):
        asignaciones = message.data.get("assigned_orders", {})
        rutas = {}
        for estado, pedidos in asignaciones.items():
            rutas[estado] = sorted(pedidos, key=lambda x: x.get("customer_zip_code_prefix", 0))
        return Message(sender=self, recipient="LoggerAgent", data={"routes": rutas})
