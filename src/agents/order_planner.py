from autogen_core import AgentId, RoutedAgent, MessageContext, default_subscription, message_handler
from messages.message_types import ListaPedidos, GrafoAsignaciones, Pedido
from math import radians, cos, sin, asin, sqrt
from collections import defaultdict
import pandas as pd

@default_subscription
class OrderPlannerAgent(RoutedAgent):
    def __init__(self):
        super().__init__("Planner a nivel de códigos postales")

    def haversine(self, lat1, lon1, lat2, lon2) -> float:
        R = 6371
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat, dlon = lat2 - lat1, lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
        return 2 * R * asin(sqrt(a))

    @message_handler
    async def plan(self, message: ListaPedidos, ctx: MessageContext) -> None:
        print(f"[OrderPlannerAgent] Generando grafo ZIP con {len(message.pedidos)} pedidos")

        ubicaciones = {}
        zip_pedidos = defaultdict(list)

        # Recopilar todos los ZIPs únicos y su lat/lng
        for p in message.pedidos:
            # ZIP del seller
            zip_seller = str(p.seller_zip_code_prefix)
            if zip_seller not in ubicaciones:
                ubicaciones[zip_seller] = (p.seller_lat, p.seller_lng)
            zip_pedidos[zip_seller].append(p)

            # ZIP del customer
            zip_customer = str(p.customer_zip_code_prefix)
            if zip_customer not in ubicaciones:
                ubicaciones[zip_customer] = (p.customer_lat, p.customer_lng)
            zip_pedidos[zip_customer].append(p)

        # Construir grafo completo entre ZIPs
        grafo = {}
        zip_codes = list(ubicaciones.keys())

        for i in range(len(zip_codes)):
            origen = zip_codes[i]
            grafo[origen] = {}
            lat1, lon1 = ubicaciones[origen]
            for j in range(len(zip_codes)):
                if i != j:
                    destino = zip_codes[j]
                    lat2, lon2 = ubicaciones[destino]
                    dist = self.haversine(lat1, lon1, lat2, lon2)
                    grafo[origen][destino] = dist

        # Empaquetar pedidos como diccionario para trazabilidad
        pedidos_dict = {p.order_id: p for p in message.pedidos}

        # Enviar el grafo ZIP al optimizador
        await self.send_message(
            GrafoAsignaciones(
                estado="GLOBAL",
                grafo=grafo,
                pedidos=pedidos_dict,
                origen=zip_codes[0],
                destino=zip_codes[-1]
            ),
            AgentId("optimizer", "default")
        )
