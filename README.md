# 🎬 StreamUCV — Módulo del Diccionario de Datos

Este es el Módulo de Exploración del Diccionario de Datos para el **Proyecto #1 - StreamUCV** de la asignatura **Administración de Bases de Datos** (Semestre 1-2026, Escuela de Computación, UCV).

La aplicación, desarrollada en **Python**, se conecta a una instancia local de **SQL Server** para auditar y consultar de forma automática y visual las metadatos, restricciones físicas, almacenamiento y estimar costos del esquema `streaming` de la base de datos `StreamUCV`.

---

## 🛠️ Requisitos e Instalación

### 1. Requisitos del Sistema
* **Python 3.11 o superior**
* **Microsoft SQL Server** (local o en Docker) con el esquema `streaming` creado y poblado.
* **Driver ODBC de SQL Server** instalado en el sistema operativo (ej. `ODBC Driver 17 for SQL Server` o `ODBC Driver 18 for SQL Server`).

### 2. Instalación de Dependencias
Instale las librerías necesarias con el siguiente comando en su terminal:
```bash
pip install -r requirements.txt
```

---

## 🚀 Instrucciones de Ejecución

Para iniciar la aplicación web con la interfaz gráfica e interactiva de Streamlit, ejecute:

```bash
streamlit run main.py
```
O bien:
```bash
python main.py
```

La aplicación se abrirá de forma automática en su navegador predeterminado (por lo general en `http://localhost:8501`).

---

## ⚙️ Configuración y Portabilidad

El código centraliza los parámetros de conexión requeridos por el enunciado en el archivo [app/config.py](file:///c:/Users/Ronald/Desktop/ABDproys/Fase-1/app/config.py):
* `SERVER`: Dirección del servidor (ej. `localhost` o `localhost\SQLEXPRESS`).
* `DATABASE`: Nombre de la base de datos (`StreamUCV`).
* `USERNAME` / `PASSWORD`: Credenciales del usuario SQL Server.
* `DRIVER`: Nombre del driver instalado en el sistema.

### Autenticación Integrada (Windows Auth)
Si utiliza autenticación de Windows, deje las variables `USERNAME` y `PASSWORD` vacías en `config.py` o cámbielo desde la interfaz de usuario. El sistema utilizará de forma automática `Trusted_Connection=yes`.

### Sobrescritura Dinámica
La interfaz de usuario incluye un panel lateral (Sidebar) que permite modificar y probar todos estos parámetros en caliente, garantizando la **portabilidad absoluta** del software durante la defensa o evaluación del profesor en otra máquina.

---

## 📐 Supuestos de Cómputo Físico de Datos
1. **Tamaño de bloque/página:** 8 KB (8,192 bytes).
2. **Tamaño estimado de un registro:** Suma de los tamaños máximos declarados para sus columnas.
3. **Factor de bloqueo (Tabla):** `ParteEntera(8192 / tamaño_registro_bytes)`.
4. **Factor de bloqueo (Índice):** `ParteEntera(8192 / tamaño_fila_indice_bytes)`, donde el tamaño de fila de índice corresponde a la suma de sus columnas clave.
5. **Costo en Tiempo:** Calculado sobre una tasa de transferencia promedio del disco duro de **17 MB/s**.
