from autogen_core import RoutedAgent, MessageContext, message_handler, default_subscription
from messages.message_types import Rutas
import csv
from pathlib import Path

@default_subscription
class LoggerAgent(RoutedAgent):
    def __init__(self):
        super().__init__("Registra las rutas finales")

    @message_handler
    async def log(self, message: Rutas, ctx: MessageContext) -> None:
        print(f"\n[{self.__class__.__name__}] Resultado final de rutas:")

        output_file = Path("logs/predicciones.csv")
        output_file.parent.mkdir(exist_ok=True)

        with open(output_file, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "order_id", "estado", "zip_code", "predicted_days", "delivery_time_days"
            ])

            for estado, pedidos in message.rutas.items():
                print(f"  - {estado}: {len(pedidos)} pedidos")
                for p in pedidos:
                    predicted = getattr(p, "predicted_days", "N/A")
                    real = getattr(p, "delivery_time_days", "N/A")
                    zip_code = getattr(p, "customer_zip_code_prefix", "N/A")
                    print(f"    Pedido {p.order_id} → {predicted} días")

                    writer.writerow([
                        p.order_id, estado, zip_code, predicted, real
                    ])
