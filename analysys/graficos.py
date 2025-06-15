import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import os

# Crear carpeta para guardar los gráficos
os.makedirs("graphics", exist_ok=True)

# Configurar estilo y tamaño
sns.set_theme(style="whitegrid")
sns.set_context("notebook", font_scale=1.3)
sns.set(rc={"figure.figsize": (16, 8)})

# Cargar los datos
df = pd.read_csv("logs/predicciones.csv")

# Añadir columna de error
df["error"] = df["predicted_days"] - df["delivery_time_days"]

# Agrupación de distancia total por estado
df_agg = df.groupby("estado")["distancia_recorrida_km"].sum().reset_index()

# ---------- Gráfico 1: Dispersión predicción vs real ----------
sns.scatterplot(data=df, x="delivery_time_days", y="predicted_days", hue="estado", palette="deep")
plt.title("Gráfico de dispersión: Predicción vs Entrega real")
plt.savefig("graphics/grafico_dispersion_pred_vs_real.png")
plt.clf()

# ---------- Gráfico 2: Boxplot del error por estado ----------
sns.boxplot(data=df, x="estado", y="error", hue="estado", palette="pastel", legend=False)
plt.title("Boxplot del error de predicción por estado")
plt.savefig("graphics/boxplot_error_prediccion.png")
plt.clf()

# ---------- Gráfico 3: Barras de distancia total por estado ----------
sns.barplot(data=df_agg, x="estado", y="distancia_recorrida_km", hue="estado", palette="muted", legend=False)
plt.title("Distancia total recorrida por estado")
plt.savefig("graphics/barras_distancia_total.png")
plt.clf()

# ---------- Gráfico 4: Histograma de tiempos estimados ----------
sns.histplot(data=df, x="predicted_days", hue="estado", multiple="stack", kde=True)
plt.title("Histograma de días estimados por estado")
plt.savefig("graphics/histograma_tiempos_estimados.png")
plt.clf()

# ---------- Gráfico 5: Violín de tiempo real por estado ----------
sns.violinplot(data=df, x="estado", y="delivery_time_days", hue="estado", palette="Set2", legend=False)
plt.title("Distribución real de días de entrega por estado")
plt.savefig("graphics/violin_tiempo_real.png")
plt.clf()

# ---------- Gráfico 6: Histograma del tiempo real de entrega ----------
sns.histplot(data=df, x="delivery_time_days", bins=20, kde=True)
plt.title("Histograma del tiempo real de entrega")
plt.savefig("graphics/histograma_tiempo_real.png")
plt.clf()

# ---------- Gráfico 7: Histograma del número de ítems por pedido ----------
df_items = df.groupby("order_id").size().reset_index(name="num_items")
sns.histplot(data=df_items, x="num_items", discrete=True)
plt.title("Distribución del número de ítems por pedido")
plt.savefig("graphics/histograma_num_items.png")
plt.clf()

# ---------- Gráfico 8: Mapa de calor de correlaciones ----------
corr = df.select_dtypes(include="number").corr()
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Mapa de calor de correlaciones numéricas")
plt.savefig("graphics/mapa_calor_correlaciones.png")
plt.clf()

# ---------- Gráfico 9: Boxplot del precio por estado ----------
sns.boxplot(data=df, x="estado", y="price", palette="Spectral", hue="estado", legend=False)
plt.title("Distribución del precio de los pedidos por estado")
plt.savefig("graphics/boxplot_precio_estado.png")
plt.clf()