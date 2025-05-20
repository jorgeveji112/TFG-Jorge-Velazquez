from autogen_core import AgentId, RoutedAgent, MessageContext, message_handler, default_subscription
from messages.message_types import ListaPedidos, Asignaciones, Pedido
from collections import defaultdict

@default_subscription
class OrderPlannerAgent(RoutedAgent):
    def __init__(self):
        super().__init__("Agrupa los pedidos por estado")

    @message_handler
    async def plan(self, message: ListaPedidos, ctx: MessageContext) -> None:
        resultado = defaultdict(list)
        for pedido in message.pedidos:
            estado = pedido.customer_state
            resultado[estado].append(pedido)

        print(f"[{self.__class__.__name__}] Agrupación por estado:")
        for estado, pedidos in resultado.items():
            print(f"  - {estado}: {len(pedidos)} pedidos")

        await self.publish_message(Asignaciones(asignados=dict(resultado)), AgentId("optimizer", "default"))

