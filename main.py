import pandas as pd
from autogen import Message
from agents import (
    DeliveryPredictorAgent,
    OrderPlannerAgent,
    RouteOptimizerAgent,
    LoggerAgent
)

# 1. Cargar datos (una muestra pequeña para pruebas)
df = pd.read_csv("data/processed/orders_filtered_with_delivery_time.csv")
sample_orders = df.sample(10, random_state=42).to_dict(orient="records")

# 2. Inicializar agentes
delivery_predictor = DeliveryPredictorAgent()
order_planner = OrderPlannerAgent()
route_optimizer = RouteOptimizerAgent()
logger_agent = LoggerAgent()

# 3. Enviar pedidos al predictor
print("\n== Paso 1: Predicción de tiempos de entrega ==")
msg1 = Message(sender="main", recipient="DeliveryPredictor", data={"orders": sample_orders})
msg2 = delivery_predictor.receive(msg1)

# 4. Planificar pedidos según estado
print("\n== Paso 2: Asignación de pedidos por estado ==")
msg3 = order_planner.receive(msg2)

# 5. Optimizar rutas
print("\n== Paso 3: Optimización de rutas de entrega ==")
msg4 = route_optimizer.receive(msg3)

# 6. Registrar rutas finales
print("\n== Paso 4: Log de resultados ==")
logger_agent.receive(msg4)
