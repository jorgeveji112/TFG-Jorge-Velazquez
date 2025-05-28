from autogen_core import AgentId, RoutedAgent, MessageContext, default_subscription, message_handler
from messages.message_types import Asignaciones, Rutas
from math import radians, cos, sin, asin, sqrt

@default_subscription
class RouteOptimizerAgent(RoutedAgent):
    def __init__(self):
        super().__init__("Optimiza rutas TSP solo entre customers por estado")

    def distancia(self, p1, p2):
        # Distancia entre dos customers (ignorando seller)
        lat1, lon1 = p1.customer_lat, p1.customer_lng
        lat2, lon2 = p2.customer_lat, p2.customer_lng
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        R = 6371
        return R * c

    def tsp_nearest_neighbor(self, pedidos):
        if not pedidos:
            return []
        no_visitados = pedidos.copy()
        ruta = [no_visitados.pop(0)]  # Empieza por el primero
        while no_visitados:
            actual = ruta[-1]
            siguiente = min(no_visitados, key=lambda x: self.distancia(actual, x))
            ruta.append(siguiente)
            no_visitados.remove(siguiente)
        return ruta

    @message_handler
    async def optimize(self, message: Asignaciones, ctx: MessageContext) -> None:
        print(f"[RouteOptimizerAgent] Calculando rutas óptimas tipo TSP solo entre customers...")

        rutas_ordenadas = {}

        for estado, pedidos in message.asignados.items():
            # Ordena pedidos usando TSP Nearest Neighbor entre customers
            ruta = self.tsp_nearest_neighbor(pedidos)
            rutas_ordenadas[estado] = ruta

        await self.send_message(Rutas(rutas=rutas_ordenadas), AgentId("logger", "default"))
