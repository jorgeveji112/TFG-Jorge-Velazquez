import pandas as pd
import asyncio
from autogen_core import SingleThreadedAgentRuntime, AgentId
from messages.message_types import Pedido, ListaPedidos
from agents.delivery_predictor import DeliveryPredictorAgent
from agents.order_planner import OrderPlannerAgent
from agents.route_optimizer import RouteOptimizerAgent
from agents.logger_agent import LoggerAgent
from pedido_generator import generar_lista_pedidos

async def main():
    runtime = SingleThreadedAgentRuntime()

    pedidos = generar_lista_pedidos(num_pedidos=100)
    

    await DeliveryPredictorAgent.register(runtime, "predictor", lambda: DeliveryPredictorAgent())
    await OrderPlannerAgent.register(runtime, "planner", lambda: OrderPlannerAgent())
    await RouteOptimizerAgent.register(runtime, "optimizer", lambda: RouteOptimizerAgent())
    await LoggerAgent.register(runtime, "logger", lambda: LoggerAgent())

    runtime.start()
    await runtime.send_message(pedidos, AgentId("predictor", "default"))
    await runtime.stop_when_idle()

if __name__ == "__main__":
    asyncio.run(main())
