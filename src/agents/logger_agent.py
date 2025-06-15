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
                "order_id", "estado", "zip_code", "predicted_days", "delivery_time_days", "distancia_recorrida_km",
                "price", "freight_value", "payment_value", "payment_installments",
                "product_weight_g", "product_length_cm", "product_height_cm", "product_width_cm",
                "order_purchase_timestamp", "shipping_limit_date"
            ])

            for estado, pedidos in message.rutas.items():
                print(f"  - {estado}: {len(pedidos)} pedidos")

                distancia_total = 0.0
                prev = None

                for p in pedidos:
                    predicted = getattr(p, "predicted_days", "N/A")
                    real = getattr(p, "delivery_time_days", "N/A")
                    zip_code = getattr(p, "customer_zip_code_prefix", "N/A")

                    if prev is None:
                        dist = 0.0
                    else:
                        dist = self.haversine(
                            prev.customer_lat, prev.customer_lng,
                            p.customer_lat, p.customer_lng
                        )
                    distancia_total += dist

                    print(f"    Pedido {p.order_id} → {predicted} días, distancia desde anterior: {round(dist, 2)} km")

                    writer.writerow([
                        p.order_id, estado, zip_code, predicted, real, round(dist, 2),
                        p.price, p.freight_value, p.payment_value, p.payment_installments,
                        p.product_weight_g, p.product_length_cm, p.product_height_cm, p.product_width_cm,
                        p.order_purchase_timestamp, p.shipping_limit_date
                    ])

                    prev = p

                print(f"    Distancia total para {estado}: {round(distancia_total, 2)} km\n")
