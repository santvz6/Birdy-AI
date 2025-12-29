# 🐦 Birdy AI: Evolución del Cerebro Neuroevolutivo
Este documento detalla la progresión de la arquitectura de la red neuronal aplicada a nuestro proyecto Birdy, un sistema de aprendizaje por refuerzo donde una población de pájaros evoluciona para dominar un entorno dinámico.

## 📑 LOG DE EVOLUCIÓN: BIRDY NEURAL NETWORK

| FASE | ARQUITECTURA | PESOS | DESCRIPCIÓN TÉCNICA |
| :--- | :--- | :--- | :--- |
| **01. Prototipo** | **3 - 5 - 1** | ~20 | **Reflejo Básico:** Solo esquiva tuberías. Entradas: Distancia X, Distancia Y, y Velocidad. |
| **02. Expansión** | **11 - 16 - 1** | ~192 | **Percepción Total:** Añadimos Espadas, Monedas y PowerUps con sensores individuales para cada uno. |
| **03. Actual (Deep)**| **9 - 10 - 6 - 1**| 156 | **Estratega:** Dos capas ocultas. Capacidad de priorizar: "Esquivar espada > Recoger moneda". El PowerUp solo otorga fitness. |

---

### 🧠 Cambios Clave en la Lógica de Entrenamiento

* **De Destrucción a Persistencia:** Los objetos ya no mueren al ser tocados (`dokill=False`). Usamos un `set()` de `hit_items` por pájaro para que la horda compita en igualdad de condiciones.
* **Normalización $[0, 1]$:** Todos los inputs (distancias y velocidades) se escalan según el tamaño de la pantalla para estabilizar los gradientes de la red.
* **Jerarquía de Fitness:**
    * **Vivir:** +1 (Supervivencia)
    * **Moneda:** +100 (Incentivo)
    * **PowerUp:** +500 (Prioridad)
    * **Espada:** -300 (Castigo por daño) 
    > **Nota:** Castigos bajos provocan saltos constantes en el pájaro ya que esta es la mejor estrategia si solo nos importa sobrevivir.

---

### 🛠️ Configuración de Capas Actual (9-10-6-1)
1. **Input (9):** [PipeX, PipeY, CoinX, CoinY, PwX, PwY, SwX, SwY, SpeedY]
2. **Hidden 1 (10):** Extracción de patrones de proximidad.
3. **Hidden 2 (6):** Toma de decisiones lógica y estratégica.
4. **Output (1):** Decisión binaria de salto (Función Sigmoide > 0.5).