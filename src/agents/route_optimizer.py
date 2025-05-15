from autogen_core import RoutedAgent, message_handler, MessageContext
from messages.message_types import Asignaciones, Rutas, Pedido

class RouteOptimizerAgent(RoutedAgent):
    def __init__(self, name="RouteOptimizer"):
        super().__init__("RouteOptimizer")

    @message_handler
    async def optimize(self, message: Asignaciones, ctx: MessageContext) -> Rutas:
        rutas = {}
        for estado, pedidos in message.asignados.items():
            rutas[estado] = sorted(pedidos, key=lambda x: x.customer_zip_code_prefix)
        print(f"\n[{self.__class__.__name__}] Rutas optimizadas por código postal.")
        return Rutas(rutas=rutas)

