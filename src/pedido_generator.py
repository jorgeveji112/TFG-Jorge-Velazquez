import pandas as pd
from messages.message_types import Pedido, ListaPedidos

def generar_lista_pedidos(
    num_pedidos: int = 20,
    path_csv: str = "data/processed/orders_filtered_with_delivery_time.csv",
    zona: str = None,
    fecha_inicio: str = None,
    fecha_fin: str = None
) -> ListaPedidos:
    df = pd.read_csv(path_csv).dropna()

    # Filtrar por zona (state o ciudad si tienes esa columna)
    if zona:
        if "customer_state" in df.columns:
            df = df[df["customer_state"] == zona]
        elif "customer_city" in df.columns:
            df = df[df["customer_city"] == zona]

    # Filtrar por fechas
    if fecha_inicio:
        df = df[df["order_purchase_timestamp"] >= fecha_inicio]
    if fecha_fin:
        df = df[df["order_purchase_timestamp"] <= fecha_fin]

    # Muestreo aleatorio
    sample = df.sample(min(num_pedidos, len(df)), random_state=42)

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
            customer_zip_code_prefix=row["customer_zip_code_prefix"],
            seller_zip_code_prefix=row["seller_zip_code_prefix"],
            delivery_time_days=row.get("delivery_time_days", None),
            customer_lat=row["customer_lat"],
            customer_lng=row["customer_lng"],
            seller_lat=row["seller_lat"],
            seller_lng=row["seller_lng"],
            order_purchase_timestamp=row["order_purchase_timestamp"],
            shipping_limit_date=row["shipping_limit_date"]            
        )
        for _, row in sample.iterrows()
    ]

    return ListaPedidos(pedidos=pedidos)
