
# TFG — Optimización Inteligente del Reparto de Mercancías mediante un Sistema Multiagente


Este proyecto implementa un sistema inteligente basado en agentes, desarrollado para el Trabajo de Fin de Grado de Jorge Velázquez Jiménez. Utiliza datos reales del dataset de e-commerce brasileño (`Olist`) para simular la predicción de tiempos de entrega y la planificación logística mediante agentes autónomos comunicándose entre sí.

---

## 🚀 Estructura del Proyecto

```
TFG-Jorge-Velazquez/
├── data/
│   └── processed/                  # Dataset limpio con delivery_time_days
|   └── raw/                        # Archivos csv del dataset sin limpiar
├── logs/
│   └── predicciones.csv            # Predicciones generadas por el sistema
├── models/
│   └── delivery_time_predictor.pkl # Modelo entrenado con scikit-learn
├── src/
│   ├── agents/                     # Agentes del sistema (predictor, planner...)
│   └── messages/                   # Clases de datos personalizadas
├── main.py                         # Punto de entrada del sistema
└── README.md
```

---

## ⚙️ Instalación

1. Crea un entorno virtual:

```bash
python -m venv .venv
.\.venv\Scripts\activate  # En Windows
```

2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

3. Entrena el modelo:

```bash
python src/train_model.py
```

---

## 🧠 Descripción de los agentes

| Agente                  | Función                                                                 |
|------------------------|-------------------------------------------------------------------------|
| `DeliveryPredictorAgent` | Predice el tiempo de entrega en días usando un modelo entrenado       |
| `OrderPlannerAgent`     | Agrupa los pedidos por estado                                           |
| `RouteOptimizerAgent`   | Ordena los pedidos por código postal (simulación de optimización)       |
| `LoggerAgent`           | Registra el resultado final en consola y guarda `predicciones.csv`      |

---

## ▶️ Ejecución

Desde la raíz del proyecto, ejecuta:

```bash
.\run.bat
```

Esto lanza `main.py` y simula todo el flujo multiagente con predicciones reales.

---

## 📄 Salida esperada

En consola verás algo como:

```
== Predicción de tiempos de entrega ==
[DeliveryPredictorAgent] Recibidos 10 pedidos...
...

[LoggerAgent] Resultado final de rutas:
RJ: 3 pedidos
...
```

Y en `logs/predicciones.csv` tendrás las predicciones para cada pedido.

---

## ✨ Autor

**Jorge Velázquez Jiménez**  
Universidad de Málaga – 2025  
Trabajo de Fin de Grado – Ingeniería del Software
