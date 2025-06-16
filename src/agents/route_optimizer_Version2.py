from autogen_core import AgentId, RoutedAgent, MessageContext, default_subscription, message_handler
from messages.message_types import GrafoAsignaciones, RutasNodos

@default_subscription
class RouteOptimizerAgent(RoutedAgent):
    def __init__(self):
        super().__init__("Optimiza rutas por ubicación única y devuelve nodos")

    @message_handler
    async def optimize(self, message: GrafoAsignaciones, ctx: MessageContext) -> None:
        print(f"[RouteOptimizerAgent] Optimizando ruta global con nodos únicos")

        nodos = {nodo.id: nodo for nodo in message.nodos}
        distancias = message.distancias
        pedidos = message.pedidos

        visitados = set()
        recogidos = set()
        ruta_nodos = []

        actual_id = next(iter(nodos))  # Primer nodo arbitrario

        while len(visitados) < len(nodos):
            candidatos = [
                nodo for nodo in nodos.values()
                if nodo.id not in visitados and (
                    nodo.tipo == "pickup" or
                    all(p in recogidos for p in nodo.pedidos_ids)
                )
            ]
            if not candidatos:
                break

            siguiente = min(
                candidatos,
                key=lambda n: distancias[actual_id][n.id] if actual_id else 0
            )

            ruta_nodos.append(siguiente)
            visitados.add(siguiente.id)
            if siguiente.tipo == "pickup":
                recogidos.update(siguiente.pedidos_ids)
            actual_id = siguiente.id

        await self.send_message(
            RutasNodos(ruta_nodos=ruta_nodos, pedidos=pedidos),
            AgentId("logger", "default")
        )
