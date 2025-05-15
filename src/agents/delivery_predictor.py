from autogen_core import RoutedAgent, message_handler, MessageContext
from messages.message_types import ListaPedidos, Pedido
import joblib
import pandas as pd

class DeliveryPredictorAgent(RoutedAgent):
    def __init__(self, name="DeliveryPredictor"):
        super().__init__("DeliveryPredictor")
        self.model = joblib.load("models/delivery_time_predictor.pkl")
        self.features = [
            "price", "freight_value", "product_weight_g",
            "product_length_cm", "product_height_cm", "product_width_cm",
            "payment_value", "payment_installments"
        ]

    @message_handler
    async def predict(self, message: ListaPedidos, ctx: MessageContext) -> ListaPedidos:
        print(f"\n[{self.__class__.__name__}] Recibidos {len(message.pedidos)} pedidos.")
        df = pd.DataFrame([p.__dict__ for p in message.pedidos])
        df.fillna(0, inplace=True)
        predictions = self.model.predict(df[self.features])
        for i, p in enumerate(message.pedidos):
            p.predicted_days = round(predictions[i], 2)
        print(f"[{self.__class__.__name__}] Predicciones asignadas a cada pedido.")
        return message

