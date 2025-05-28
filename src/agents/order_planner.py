from autogen_core import AgentId, RoutedAgent, MessageContext, default_subscription, message_handler
from messages.message_types import ListaPedidos, Asignaciones
from collections import defaultdict
import pandas as pd

@default_subscription
class OrderPlannerAgent(RoutedAgent):
    def __init__(self):
        super().__init__("Agrupa y prioriza los pedidos por estado")

    @message_handler
    async def plan(self, message: ListaPedidos, ctx: MessageContext) -> None:
        print(f"[OrderPlannerAgent] Handler ACTIVADO con {len(message.pedidos)} pedidos")

        ahora = pd.Timestamp.now()

        pedidos_ordenados = sorted(message.pedidos, key=lambda p: (
            (ahora - pd.to_datetime(p.order_purchase_timestamp)).days,
            pd.to_datetime(p.shipping_limit_date)
        ))

        agrupados_por_estado = defaultdict(list)
        for pedido in pedidos_ordenados:
            estado = pedido.customer_state
            agrupados_por_estado[estado].append(pedido)

        resultado = dict(agrupados_por_estado)

        print(f"[OrderPlannerAgent] Enviando asignaciones al optimizer...")
        await self.send_message(Asignaciones(asignados=resultado), AgentId("optimizer", "default"))
