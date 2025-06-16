from autogen_core import AgentId, RoutedAgent, MessageContext, default_subscription, message_handler
from messages.message_types import ListaPedidos, GrafoAsignaciones
from dataclasses import dataclass
from typing import Dict, List, Literal, Tuple
import pandas as pd
from math import radians, cos, sin, asin, sqrt
from collections import defaultdict

@dataclass
class Nodo:
    id: str
    lat: float
    lng: float
    tipo: Literal["pickup", "dropoff"]
    pedidos_ids: List[str]

@default_subscription
class OrderPlannerAgent(RoutedAgent):
    def __init__(self):
        super().__init__("Genera grafo global agrupando ubicaciones únicas")

    def haversine(self, lat1, lon1, lat2, lon2):
        R = 6371
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        return R * c

    @message_handler
    async def plan(self, message: ListaPedidos, ctx: MessageContext) -> None:
        print(f"[OrderPlannerAgent] Generando grafo optimizado con {len(message.pedidos)} pedidos...")

        ahora = pd.Timestamp.now()
        pedidos_ordenados = sorted(
            message.pedidos,
            key=lambda p: (
                (ahora - pd.to_datetime(p.order_purchase_timestamp)).days,
                pd.to_datetime(p.shipping_limit_date)
            )
        )

        pedidos_dict: Dict[str, object] = {}
        nodos_dict: Dict[Tuple[str, float, float], Nodo] = {}

        pickups = defaultdict(list)
        dropoffs = defaultdict(list)

        for pedido in pedidos_ordenados:
            pedidos_dict[pedido.order_id] = pedido

            # Agrupar por ubicación de seller
            pickup_coord = (f"pickup", round(pedido.seller_lat, 6), round(pedido.seller_lng, 6))
            pickups[pickup_coord].append(pedido.order_id)

            # Agrupar por ubicación de customer
            dropoff_coord = (f"dropoff", round(pedido.customer_lat, 6), round(pedido.customer_lng, 6))
            dropoffs[dropoff_coord].append(pedido.order_id)

        # Crear nodos únicos
        nodos: List[Nodo] = []
        for (tipo, lat, lng), pedidos_ids in {**pickups, **dropoffs}.items():
            nodo_id = f"{tipo}_{abs(hash((lat, lng))) % 1_000_000}"
            nodos.append(Nodo(
                id=nodo_id,
                lat=lat,
                lng=lng,
                tipo=tipo,
                pedidos_ids=pedidos_ids
            ))

        # Calcular distancias entre nodos
        distancias: Dict[str, Dict[str, float]] = {}
        for nodo1 in nodos:
            distancias[nodo1.id] = {}
            for nodo2 in nodos:
                if nodo1.id == nodo2.id:
                    distancias[nodo1.id][nodo2.id] = 0.0
                else:
                    dist = self.haversine(nodo1.lat, nodo1.lng, nodo2.lat, nodo2.lng)
                    distancias[nodo1.id][nodo2.id] = dist

        print(f"[OrderPlannerAgent] Grafo final: {len(nodos)} nodos únicos.")
        await self.send_message(
            GrafoAsignaciones(nodos=nodos, distancias=distancias, pedidos=pedidos_dict),
            AgentId("optimizer", "default")
        )
