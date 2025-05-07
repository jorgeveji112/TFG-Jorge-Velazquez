import pandas as pd
import os

# Rutas
RAW_PATH = 'data/raw'
PROCESSED_PATH = 'data/processed'
os.makedirs(PROCESSED_PATH, exist_ok=True)

# Cargar datasets
customers = pd.read_csv(os.path.join(RAW_PATH, 'olist_customers_dataset.csv'))
order_items = pd.read_csv(os.path.join(RAW_PATH, 'olist_order_items_dataset.csv'))
order_payments = pd.read_csv(os.path.join(RAW_PATH, 'olist_order_payments_dataset.csv'))
orders = pd.read_csv(os.path.join(RAW_PATH, 'olist_orders_dataset.csv'))
products = pd.read_csv(os.path.join(RAW_PATH, 'olist_products_dataset.csv'))
sellers = pd.read_csv(os.path.join(RAW_PATH, 'olist_sellers_dataset.csv'))
category_translation = pd.read_csv(os.path.join(RAW_PATH, 'product_category_name_translation.csv'))

# Traducir categorías
products = products.merge(category_translation, on='product_category_name', how='left')

# Unir productos con sellers y order_items
order_items_merged = order_items.merge(products, on='product_id', how='left') \
                                 .merge(sellers, on='seller_id', how='left')

# Unir con pedidos, clientes y pagos
full_df = orders.merge(customers, on='customer_id', how='left') \
                .merge(order_items_merged, on='order_id', how='left') \
                .merge(order_payments, on='order_id', how='left')

# Seleccionar columnas clave
columns_needed = [
    'order_id',
    'order_purchase_timestamp',
    'shipping_limit_date',
    'order_estimated_delivery_date',
    'customer_zip_code_prefix',
    'customer_state',
    'seller_zip_code_prefix',
    'seller_state',
    'price',
    'freight_value',
    'product_weight_g',
    'product_length_cm',
    'product_height_cm',
    'product_width_cm',
    'product_category_name_english',
    'payment_type',
    'payment_installments',
    'payment_value',
    'order_delivered_customer_date'  # necesaria para calcular el target
]

filtered_df = full_df[columns_needed]

# Convertir a datetime y calcular delivery_time_days
filtered_df['order_purchase_timestamp'] = pd.to_datetime(filtered_df['order_purchase_timestamp'], errors='coerce')
filtered_df['order_delivered_customer_date'] = pd.to_datetime(filtered_df['order_delivered_customer_date'], errors='coerce')
filtered_df['delivery_time_days'] = (filtered_df['order_delivered_customer_date'] - filtered_df['order_purchase_timestamp']).dt.days

# Guardar resultado
output_path = os.path.join(PROCESSED_PATH, 'orders_filtered_with_delivery_time.csv')
filtered_df.to_csv(output_path, index=False)

print(f"Archivo procesado guardado en: {output_path}")
