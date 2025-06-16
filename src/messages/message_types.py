from dataclasses import dataclass
from typing import List, Dict, Literal

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
    seller_zip_code_prefix: int
    customer_zip_code_prefix: int
    customer_lat: float
    customer_lng: float
    seller_lat: float
    seller_lng: float
    delivery_time_days: float | None = None
    predicted_days: float | None = None
    order_purchase_timestamp: str = ""
    shipping_limit_date: str = "" 
    
@dataclass
class ListaPedidos:
    pedidos: List[Pedido]

@dataclass
class Asignaciones:
    asignados: Dict[str, List[Pedido]]

@dataclass
class Rutas:
    rutas: Dict[str, List[Pedido]]

@dataclass
class Nodo:
    id: str
    lat: float
    lng: float
    tipo: Literal["pickup", "dropoff"]
    pedido_id: List[str]

@dataclass
class GrafoAsignaciones:
    nodos: List[Nodo]                            # Nodos de recogida y entrega
    distancias: Dict[str, Dict[str, float]]      # Mapa de distancias
    pedidos: Dict[str, Pedido]                   # Info completa de cada pedido

@dataclass
class RutasNodos:
    ruta_nodos: List[Nodo]
    pedidos: Dict[str, Pedido]
