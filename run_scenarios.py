import asyncio
from autogen_core import SingleThreadedAgentRuntime, AgentId
from messages.message_types import Pedido
from agents.delivery_predictor import DeliveryPredictorAgent
from agents.order_planner import OrderPlannerAgent
from agents.route_optimizer import RouteOptimizerAgent
from agents.logger_agent import LoggerAgent
from pedido_generator import generar_lista_pedidos
from pathlib import Path
import shutil

async def ejecutar_escenario(nombre: str, **filtros):
    print(f"\n🚀 Ejecutando escenario: {nombre}")
    
    runtime = SingleThreadedAgentRuntime()

    await DeliveryPredictorAgent.register(runtime, "predictor", lambda: DeliveryPredictorAgent())
    await OrderPlannerAgent.register(runtime, "planner", lambda: OrderPlannerAgent())
    await RouteOptimizerAgent.register(runtime, "optimizer", lambda: RouteOptimizerAgent())
    await LoggerAgent.register(runtime, "logger", lambda: LoggerAgent())

    runtime.start()

    pedidos = generar_lista_pedidos(num_pedidos=1000, **filtros)

    await runtime.send_message(pedidos, AgentId("predictor", "default"))

    await runtime.stop_when_idle()

    # Guardar los resultados
    ruta_csv = Path("logs/predicciones.csv")
    ruta_destino = Path(f"logs/predicciones_{nombre}.csv")

    if ruta_csv.exists():
        shutil.copyfile(ruta_csv, ruta_destino)  # sobreescribe si ya existe
        print(f"✅ Guardado: {ruta_destino}")
    else:
        print(f"⚠️ No se encontró el archivo {ruta_csv}")
async def main():
    await ejecutar_escenario("urbano_SP", zona="SP")
    await ejecutar_escenario("rural_MG", zona="MG")
    await ejecutar_escenario("mezcla_total")  # sin filtros

if __name__ == "__main__":
    asyncio.run(main())
