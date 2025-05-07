from autogen import Agent, Message

class OrderPlannerAgent(Agent):
    def __init__(self, name="OrderPlanner"):
        super().__init__(name=name)

    def receive(self, message: Message):
        pedidos = message.data.get("orders", [])
        asignaciones = {}
        for pedido in pedidos:
            estado = pedido.get("customer_state")
            if estado not in asignaciones:
                asignaciones[estado] = []
            asignaciones[estado].append(pedido)
        return Message(sender=self, recipient="RouteOptimizer", data={"assigned_orders": asignaciones})
