# MiniERP - Sistema de Gestión Empresarial

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.0-092E20?style=for-the-badge&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

Este proyecto implementa la base de un sistema ERP sencillo utilizando Django, enfocado en la gestión de clientes, productos y pedidos de venta.

## 1. Justificación del Modelo de Datos

### 1.1. Clasificación de Entidades
* **Entidades Maestras (App `core`):**
    * **Cliente:** Dato maestro independiente. Contiene la información fiscal y de contacto.
    * **Producto:** Dato maestro estable. Representa el catálogo vendible.
* **Entidades Transaccionales (App `ventas`):**
    * **Pedido:** Cabecera de la venta. Depende del Cliente y del tiempo.
    * **Línea de Pedido:** Detalle de la venta. Depende del Pedido (composición fuerte).

### 1.2. Relaciones y Cardinalidades
* **Cliente - Pedido (1:N):** Un cliente tiene muchos pedidos. (On Delete: RESTRICT).
* **Pedido - Línea (1:N):** Un pedido tiene muchas líneas. (On Delete: CASCADE).
* **Producto - Línea (1:N):** Un producto aparece en muchas líneas. (On Delete: RESTRICT).

## 2. Estructura de Datos (Esquema ER)

A continuación se detallan las tablas, sus campos principales y las claves (PK/FK).

### Tabla: CLIENTE
| Campo | Tipo | Notas |
| :--- | :--- | :--- |
| **id** | Integer | **PK** (Automática) |
| nif | String | **Unique** (DNI/CIF) |
| nombre | String | |
| email | String | |
| direccion | Text | |

### Tabla: PRODUCTO
| Campo | Tipo | Notas |
| :--- | :--- | :--- |
| **id** | Integer | **PK** (Automática) |
| sku | String | **Unique** (Referencia) |
| nombre | String | |
| precio | Decimal | |

### Tabla: PEDIDO
| Campo | Tipo | Notas |
| :--- | :--- | :--- |
| **id** | Integer | **PK** (Automática) |
| fecha | DateTime | Auto-generada |
| estado | String | Enum (Borrador, Confirmado...) |
| **cliente_id** | Integer | **FK** -> Cliente |

### Tabla: LINEA_PEDIDO
| Campo | Tipo | Notas |
| :--- | :--- | :--- |
| **id** | Integer | **PK** (Automática) |
| cantidad | Integer | Constraint: > 0 |
| precio_unitario | Decimal | Precio congelado |
| **pedido_id** | Integer | **FK** -> Pedido |
| **producto_id** | Integer | **FK** -> Producto |