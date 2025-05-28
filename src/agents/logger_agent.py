from autogen_core import RoutedAgent, MessageContext, message_handler, default_subscription
from messages.message_types import Rutas
import csv
from pathlib import Path
from math import radians, cos, sin, asin, sqrt

@default_subscription
class LoggerAgent(RoutedAgent):
    def __init__(self):
        super().__init__("Registra las rutas finales")

    def haversine(self, lat1, lon1, lat2, lon2):
        R = 6371
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * asin(sqrt(a))
        return R * c

    @message_handler
    async def log(self, message: Rutas, ctx: MessageContext) -> None:
        print(f"\n[{self.__class__.__name__}] Resultado final de rutas:")

        output_file = Path("logs/predicciones.csv")
        output_file.parent.mkdir(exist_ok=True)

        with open(output_file, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "order_id", "estado", "zip_code", "predicted_days", "delivery_time_days", "distancia_recorrida_km"
            ])

            for estado, pedidos in message.rutas.items():
                print(f"  - {estado}: {len(pedidos)} pedidos")

                distancia_total = 0.0
                prev = None

                for idx, p in enumerate(pedidos):
                    predicted = getattr(p, "predicted_days", "N/A")
                    real = getattr(p, "delivery_time_days", "N/A")
                    zip_code = getattr(p, "customer_zip_code_prefix", "N/A")

                    if prev is None:
                        dist = 0.0  # Primer customer del estado
                    else:
                        dist = self.haversine(
                            prev.customer_lat, prev.customer_lng,
                            p.customer_lat, p.customer_lng
                        )
                    distancia_total += dist

                    print(f"    Pedido {p.order_id} → {predicted} días, distancia recorrida desde anterior: {round(dist, 2)} km")

                    writer.writerow([
                        p.order_id, estado, zip_code, predicted, real, round(dist, 2)
                    ])

                    prev = p

                print(f"    Distancia total de la ruta para {estado}: {round(distancia_total, 2)} km\n")
