from autogen_core import RoutedAgent, MessageContext, message_handler, default_subscription
from messages.message_types import Rutas
from collections import defaultdict
from pathlib import Path
import csv
from math import radians, cos, sin, asin, sqrt

@default_subscription
class LoggerAgent(RoutedAgent):
    def __init__(self):
        super().__init__("Registra la ruta optimizada")

    def haversine(self, lat1, lon1, lat2, lon2) -> float:
        R = 6371
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat, dlon = lat2 - lat1, lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
        return 2 * R * asin(sqrt(a))

    @message_handler
    async def log(self, message: Rutas, ctx: MessageContext) -> None:
        print(f"\n[{self.__class__.__name__}] Resultado final de la ruta optimizada:")

        output_file = Path("logs/ruta_tsp.csv")
        output_file.parent.mkdir(exist_ok=True)

        with open(output_file, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["zip_code", "num_pedidos", "distancia_desde_anterior_km", "order_ids", "predicted_days"])

            rutas = list(message.rutas.values())[0]  # solo hay una clave: GLOBAL
            ruta_por_zip = defaultdict(list)

            for p in rutas:
                ruta_por_zip[str(p.customer_zip_code_prefix)].append(p)
                ruta_por_zip[str(p.seller_zip_code_prefix)].append(p)

            visitados = []
            for p in rutas:
                zip_c = str(p.customer_zip_code_prefix)
                zip_s = str(p.seller_zip_code_prefix)
                if zip_s not in visitados:
                    visitados.append(zip_s)
                if zip_c not in visitados:
                    visitados.append(zip_c)

            total_distancia = 0
            zip_coords = {}

            # Obtener coordenadas medias por ZIP
            for p in rutas:
                zip_coords[str(p.customer_zip_code_prefix)] = (p.customer_lat, p.customer_lng)
                zip_coords[str(p.seller_zip_code_prefix)] = (p.seller_lat, p.seller_lng)

            prev_zip = None
            for zip_code in visitados:
                pedidos = ruta_por_zip[zip_code]
                order_ids = [p.order_id for p in pedidos]
                predicted = [round(getattr(p, "predicted_days", 0), 2) for p in pedidos]

                if prev_zip:
                    dist = self.haversine(*zip_coords[prev_zip], *zip_coords[zip_code])
                else:
                    dist = 0.0
                total_distancia += dist

                print(f"  - ZIP {zip_code}: {len(order_ids)} pedidos, +{dist:.2f} km")
                writer.writerow([zip_code, len(order_ids), round(dist, 2), ", ".join(order_ids), ", ".join(map(str, predicted))])
                prev_zip = zip_code

            print(f"\n Distancia total estimada: {total_distancia:.2f} km")
