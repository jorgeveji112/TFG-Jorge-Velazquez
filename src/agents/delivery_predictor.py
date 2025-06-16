from autogen_core import AgentId, RoutedAgent, MessageContext, message_handler
from messages.message_types import ListaPedidos
import joblib
import pandas as pd

class DeliveryPredictorAgent(RoutedAgent):
    def __init__(self):
        super().__init__("Predice el tiempo de entrega")
        self.model = joblib.load("models/delivery_time_predictor.pkl")
        self.features = [
            "price", "freight_value", "product_weight_g",
            "product_length_cm", "product_height_cm", "product_width_cm",
            "payment_value", "payment_installments"
        ]

    @message_handler
    async def predict(self, message: ListaPedidos, ctx: MessageContext) -> None:
        try:
            print("[DeliveryPredictorAgent] Handler ACTIVADO")
            df = pd.DataFrame([p.__dict__ for p in message.pedidos])
            df = df.infer_objects(copy=False)
            preds = self.model.predict(df[self.features])
            for i, p in enumerate(message.pedidos):
                p.predicted_days = round(preds[i], 2)

            print(f"[DeliveryPredictorAgent] Enviando predicciones a planner...")
            await self.send_message(message, AgentId("planner", "default"))
        except Exception as e:
            print("[ERROR en predict()]:", e)
