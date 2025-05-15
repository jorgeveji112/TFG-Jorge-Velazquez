from autogen_core import RoutedAgent, message_handler, MessageContext
from messages.message_types import ListaPedidos, Asignaciones, Pedido

class OrderPlannerAgent(RoutedAgent):
    def __init__(self, name="OrderPlanner"):
        super().__init__("OrderPlanner")

    @message_handler
    async def plan(self, message: ListaPedidos, ctx: MessageContext) -> Asignaciones:
        resultado = {}
        for pedido in message.pedidos:
            estado = pedido.customer_state
            resultado.setdefault(estado, []).append(pedido)
        print(f"\n[{self.__class__.__name__}] Pedidos agrupados por estado:")
        for estado, pedidos in resultado.items():
            print(f"  - {estado}: {len(pedidos)} pedidos")
        return Asignaciones(asignados=resultado)
