from autogen_core import AgentId, RoutedAgent, MessageContext, message_handler, default_subscription
from messages.message_types import Asignaciones, Rutas, Pedido

@default_subscription
class RouteOptimizerAgent(RoutedAgent):
    def __init__(self):
        super().__init__("Optimiza rutas por código postal")

    @message_handler
    async def optimize(self, message: Asignaciones, ctx: MessageContext) -> None:
        rutas = {}
        for estado, pedidos in message.asignados.items():
            rutas[estado] = sorted(pedidos, key=lambda x: x.customer_zip_code_prefix)

        print(f"[{self.__class__.__name__}] Rutas optimizadas por ZIP para {len(rutas)} estados.")
        await self.publish_message(Rutas(rutas=rutas), AgentId("logger", "default"))

