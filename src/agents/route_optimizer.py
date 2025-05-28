from autogen_core import AgentId, RoutedAgent, MessageContext, default_subscription, message_handler
import pandas as pd
from messages.message_types import GrafoAsignaciones, Rutas, Pedido
import networkx as nx
from itertools import permutations
from collections import defaultdict

@default_subscription
class RouteOptimizerAgent(RoutedAgent):
    def __init__(self):
        super().__init__("TSP por ZIPs con prioridad")

    def tsp_con_prioridad(self, G: nx.Graph, start: str):
        nodos = list(G.nodes)
        nodos.remove(start)

        mejor_ruta = None
        menor_coste = float("inf")

        for perm in permutations(nodos):
            ruta = [start] + list(perm) + [start]
            coste = sum(G[ruta[i]][ruta[i+1]]['weight'] for i in range(len(ruta)-1))
            if coste < menor_coste:
                menor_coste = coste
                mejor_ruta = ruta

        return mejor_ruta, menor_coste

    @message_handler
    async def optimize(self, message: GrafoAsignaciones, ctx: MessageContext) -> None:
        print(f"[RouteOptimizerAgent] TSP con prioridad para {len(message.grafo)} ZIPs")

        # Agrupar pedidos por ZIP y calcular prioridad acumulada
        zip_prioridades = defaultdict(int)
        zip_pedidos = defaultdict(list)

        for pedido in message.pedidos.values():
            # Seller ZIP
            zip_seller = str(pedido.seller_zip_code_prefix)
            zip_pedidos[zip_seller].append(pedido)
            zip_prioridades[zip_seller] += self._prioridad(pedido)

            # Customer ZIP
            zip_customer = str(pedido.customer_zip_code_prefix)
            zip_pedidos[zip_customer].append(pedido)
            zip_prioridades[zip_customer] += self._prioridad(pedido)

        # Crear grafo con peso = distancia - prioridad * α
        G = nx.Graph()
        factor = 2.0

        for origen, vecinos in message.grafo.items():
            for destino, distancia in vecinos.items():
                prioridad_destino = zip_prioridades[destino]
                peso = distancia - factor * prioridad_destino
                G.add_edge(origen, destino, weight=max(peso, 0.1))

        if message.origen not in G.nodes:
            print(f"[RouteOptimizerAgent] Origen {message.origen} no está en el grafo")
            return

        try:
            ruta_zip, coste_total = self.tsp_con_prioridad(G, message.origen)

            pedidos_ordenados = []
            for zip in ruta_zip:
                pedidos_ordenados.extend(zip_pedidos[zip])  # puede haber varios por ZIP

            print(f"[RouteOptimizerAgent] Ruta TSP optimizada con {len(pedidos_ordenados)} pedidos")

            await self.send_message(
                Rutas(rutas={message.estado: pedidos_ordenados}),
                AgentId("logger", "default")
            )
        except Exception as e:
            print(f"[RouteOptimizerAgent] Error en TSP: {e}")

    def _prioridad(self, p: Pedido) -> int:
        ahora = pd.Timestamp.now()
        orden = pd.to_datetime(p.order_purchase_timestamp)
        limite = pd.to_datetime(p.shipping_limit_date)
        return (ahora - orden).days - (limite - ahora).days
