from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Pedido:
    order_id: str
    price: float
    freight_value: float
    product_weight_g: float
    product_length_cm: float
    product_height_cm: float
    product_width_cm: float
    payment_value: float
    payment_installments: float
    customer_state: str
    customer_zip_code_prefix: int
    delivery_time_days: float | None = None

@dataclass
class ListaPedidos:
    pedidos: List[Pedido]

@dataclass
class Asignaciones:
    asignados: Dict[str, List[Pedido]]

@dataclass
class Rutas:
    rutas: Dict[str, List[Pedido]]
