import pandas as pd
import asyncio
from autogen_core import MessageContext, CancellationToken
from agents import (
    DeliveryPredictorAgent,
    OrderPlannerAgent,
    RouteOptimizerAgent,
    LoggerAgent
)
from messages.message_types import Pedido, ListaPedidos

# 1. Cargar pedidos reales desde CSV
df = pd.read_csv("data/processed/orders_filtered_with_delivery_time.csv").fillna(0)
muestra = df.sample(10, random_state=42)

pedidos = []
for _, row in muestra.iterrows():
    try:
        pedidos.append(Pedido(
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
        ))
    except Exception as e:
        print(f"Error al convertir un pedido: {e}")

# 2. Inicializar agentes
delivery = DeliveryPredictorAgent()
planner = OrderPlannerAgent()
optimizer = RouteOptimizerAgent()
logger = LoggerAgent()

# 3. Crear contexto de ejecución
ctx = MessageContext(
    topic_id="simulacion",
    sender="main",
    is_rpc=False,
    cancellation_token=CancellationToken(),
    message_id="msg-1"
)

# 4. Ejecutar flujo multiagente
async def ejecutar():
    print("\n== Predicción de tiempos de entrega ==")
    lista = ListaPedidos(pedidos=pedidos)
    pred = await delivery.predict(lista, ctx)

    print("\n== Asignación por estado ==")
    asignados = await planner.plan(pred, ctx)

    print("\n== Optimización de rutas ==")
    rutas = await optimizer.optimize(asignados, ctx)

    print("\n== Resultado final ==")
    await logger.log(rutas, ctx)

asyncio.run(ejecutar())
