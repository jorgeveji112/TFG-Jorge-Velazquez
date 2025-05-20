import pandas as pd
import asyncio
from autogen_core import SingleThreadedAgentRuntime, AgentId
from messages.message_types import Pedido, ListaPedidos
from agents.delivery_predictor import DeliveryPredictorAgent
from agents.order_planner import OrderPlannerAgent
from agents.route_optimizer import RouteOptimizerAgent
from agents.logger_agent import LoggerAgent

async def main():
    # 1. Crear runtime
    runtime = SingleThreadedAgentRuntime()

    # 2. Cargar pedidos desde CSV
    df = pd.read_csv("data/processed/orders_filtered_with_delivery_time.csv").fillna(0)
    muestra = df.sample(10, random_state=42)

    pedidos = [
        Pedido(
            order_id=row["order_id"],
            price=row["price"],
            freight_value=row["freight_value"],
            product_weight_g=row["product_weight_g"],
            product_length_cm=row["product_length_cm"],
            product_height_cm=row["product_height_cm"],
            product_width_cm=row["product_width_cm"],
            payment_value=row["payment_value"],
            payment_installments=row["payment_installments"],
            customer_state=row["customer_state"],
            customer_zip_code_prefix=int(row["customer_zip_code_prefix"]),
            delivery_time_days=row.get("delivery_time_days", None)
        )
        for _, row in muestra.iterrows()
    ]

    # 3. Registrar agentes
    await DeliveryPredictorAgent.register(runtime, "predictor", lambda: DeliveryPredictorAgent())
    await OrderPlannerAgent.register(runtime, "planner", lambda: OrderPlannerAgent())
    await RouteOptimizerAgent.register(runtime, "optimizer", lambda: RouteOptimizerAgent())
    await LoggerAgent.register(runtime, "logger", lambda: LoggerAgent())
    
    print(f"Enviando a predictor: {type(ListaPedidos(pedidos=pedidos))}")
    # 4. Lanzar flujo enviando primer mensaje
    await runtime.send_message(ListaPedidos(pedidos=pedidos), AgentId("predictor", "default"))

    # 5. Esperar hasta que todos los agentes finalicen
    await runtime.stop_when_idle()

if __name__ == "__main__":
    asyncio.run(main())
