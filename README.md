# Simulador de Cracking de Contraseñas – Password Lab

## Objetivo
Demostrar, de forma **didáctica y ética**, por qué las contraseñas débiles (cortas o predecibles) son vulnerables a un **ataque de diccionario**.  
**Solo se utilizan datos de prueba sintéticos generados por el programa.**  
Se incluyen visualizaciones con **Matplotlib** y recomendaciones automáticas.

---

## Descripción
- Genera **100 contraseñas de prueba**:
  - 50 débiles (4-7 caracteres, solo minúsculas, 5 predefinidas para garantizar recuperación).
  - 50 fuertes (8-12 caracteres, mezcla de mayúsculas, minúsculas, números y símbolos).
- Las hashea con **SHA-256** y guarda los pares `usuario:hash`.
- Crea un **diccionario de prueba** con 150 palabras comunes.
- Ejecuta un **ataque de diccionario** y mide el tiempo.
- Genera **3 gráficos** y un **CSV** con resultados.
- Ofrece **recomendaciones** específicas para cada contraseña recuperada.

---

## Requisitos
```bash
Python 3.x
pip install matplotlib


Resultados
El programa genera automáticamente:

Gráficos de análisis (*.png)

Reportes detallados (results.txt, cracked_passwords.csv)

Datos de prueba (passwords.txt, hashed_passwords.txt)

Aviso importante
Solo para fines educativos. No utilizar en sistemas reales. Todos los datos son sintéticos.

Estructura
text
password-lab/
├── pass_Lab.py              # Código principal
├── passwords.txt            # Contraseñas de prueba
├── hashed_passwords.txt     # Hashes SHA-256
├── dictionary.txt           # Diccionario de ataque
├── results.txt              # Análisis completo
├── cracked_passwords.csv    # Resultados detallados
└── *.png                    # Gráficos generados


(NATALIA SOFIA GARCIA VAZQUEZ - JOSE ROBERTO AGUILAR CASTRO) CIBERSEGURIDAD
