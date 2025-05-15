import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib

# Cargar datos
df = pd.read_csv("data/processed/orders_filtered_with_delivery_time.csv")

# Eliminar filas con delivery_time_days nulo o negativo
df = df[df['delivery_time_days'].notnull() & (df['delivery_time_days'] > 0)]

# Variables a usar
features = [
    'price', 'freight_value', 'product_weight_g',
    'product_length_cm', 'product_height_cm', 'product_width_cm',
    'payment_value', 'payment_installments'
]

X = df[features]
y = df['delivery_time_days']

# Dividir en train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar modelo
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluar
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f"MAE del modelo: {mae:.2f} días")

# Guardar modelo
joblib.dump(model, "models/delivery_time_predictor.pkl")
print("Modelo guardado en models/delivery_time_predictor.pkl")
