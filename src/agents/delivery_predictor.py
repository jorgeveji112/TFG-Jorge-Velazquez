import random
from autogen import Agent, Message

class DeliveryPredictorAgent(Agent):
    def __init__(self, name="DeliveryPredictor"):
        super().__init__(name=name)

    def receive(self, message: Message):
        pedidos = message.data.get("orders", [])
        for pedido in pedidos:
            pedido["predicted_days"] = random.randint(5, 15)
        return Message(sender=self, recipient="OrderPlanner", data={"orders": pedidos})
