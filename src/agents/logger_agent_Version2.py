from autogen_core import RoutedAgent, MessageContext, message_handler, default_subscription
from messages.message_types import RutasNodos
import csv, json
from pathlib import Path
from math import radians, cos, sin, asin, sqrt

@default_subscription
class LoggerAgent(RoutedAgent):
    def __init__(self):
        super().__init__("Registra rutas desde nodos únicos")

    def haversine(self, lat1, lon1, lat2, lon2):
        R = 6371
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * asin(sqrt(a))
        return R * c

    @message_handler
    async def log(self, message: RutasNodos, ctx: MessageContext) -> None:
        print(f"\n[LoggerAgent] Ruta por nodos únicos recibida")

        output_dir = Path("logs")
        output_dir.mkdir(exist_ok=True)

        csv_file = output_dir / "predicciones_Version2.csv"
        geojson_file = "rutas/ruta_Version2.geojson"

        coordenadas_geojson = []
        coordenadas_visitadas = set()
        distancia_total = 0.0
        prev = None

        # GeoJSON desde nodos
        for nodo in message.ruta_nodos:
            key = (round(nodo.lat, 6), round(nodo.lng, 6))
            if key not in coordenadas_visitadas:
                coordenadas_geojson.append([nodo.lng, nodo.lat])
                coordenadas_visitadas.add(key)

        # CSV por pedido
        with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "order_id", "tipo_nodo", "predicted_days", "delivery_time_days", "distancia_recorrida_km",
                "price", "freight_value", "payment_value", "payment_installments",
                "product_weight_g", "product_length_cm", "product_height_cm", "product_width_cm",
                "order_purchase_timestamp", "shipping_limit_date"
            ])

            for nodo in message.ruta_nodos:
                lat, lng = nodo.lat, nodo.lng
                if prev is None:
                    dist = 0.0
                else:
                    dist = self.haversine(prev.lat, prev.lng, lat, lng)
                distancia_total += dist
                prev = nodo

                for pid in nodo.pedidos_ids:
                    p = message.pedidos[pid]
                    writer.writerow([
                        p.order_id, nodo.tipo, getattr(p, "predicted_days", "N/A"), getattr(p, "delivery_time_days", "N/A"),
                        round(dist, 2),
                        p.price, p.freight_value, p.payment_value, p.payment_installments,
                        p.product_weight_g, p.product_length_cm, p.product_height_cm, p.product_width_cm,
                        p.order_purchase_timestamp, p.shipping_limit_date
                    ])

        # GeoJSON export
        geojson = {
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "properties": {"name": "Ruta Óptima por Nodos"},
                "geometry": {
                    "type": "LineString",
                    "coordinates": coordenadas_geojson
                }
            }]
        }

        with open(geojson_file, "w", encoding="utf-8") as gjson:
            json.dump(geojson, gjson, ensure_ascii=False, indent=2)

        print(f"✅ CSV y GeoJSON finalizados. Distancia total: {round(distancia_total, 2)} km")
