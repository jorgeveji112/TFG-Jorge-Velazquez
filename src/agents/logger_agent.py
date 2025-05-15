from autogen_core import RoutedAgent, message_handler, MessageContext
from messages.message_types import Rutas
import csv
from pathlib import Path

class LoggerAgent(RoutedAgent):
    def __init__(self, name="LoggerAgent"):
        super().__init__(name)

    @message_handler
    async def log(self, message: Rutas, ctx: MessageContext) -> None:
        print("\n[LoggerAgent] Resultado final de rutas:")

        output_file = Path("logs/predicciones.csv")
        output_file.parent.mkdir(exist_ok=True)

        with open(output_file, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "order_id",
                "estado",
                "zip_code",
                "predicted_days",
                "delivery_time_days"  # si existe en el objeto
            ])

            for estado, pedidos in message.rutas.items():
                print(f"\n  - {estado}: {len(pedidos)} pedidos")
                for p in pedidos:
                    predicted = getattr(p, "predicted_days", "N/A")
                    real = getattr(p, "delivery_time_days", "N/A")
                    zip_code = getattr(p, "customer_zip_code_prefix", "N/A")

                    print(f"    Pedido {p.order_id} → {predicted} días estimados")

                    writer.writerow([
                        p.order_id,
                        estado,
                        zip_code,
                        predicted,
                        real
                    ])
