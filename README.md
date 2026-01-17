# MiniERP - Sistema de Gestión Empresarial

![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.1-092E20?style=for-the-badge&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

Este proyecto implementa un sistema ERP completo utilizando Django. El modelo de datos ha sido diseñado siguiendo estándares profesionales para asegurar la integridad contable y la trazabilidad.

## 1. Características Avanzadas del Modelo

Para garantizar la robustez del sistema, se han implementado patrones de diseño avanzados:

* **Integridad de Históricos (Snapshot):** Las líneas de pedido guardan una copia ("foto fija") del precio, IVA y nombre del producto en el momento de la compra. Si el producto cambia de precio en el futuro, los pedidos antiguos no se ven afectados.
* **Trazabilidad (Auditoría):** Todas las entidades registran automáticamente la fecha de creación (`created_at`) y última modificación (`updated_at`).
* **Denormalización Controlada:** El modelo `Pedido` almacena los totales (Bruto, IVA, Neto) calculados para evitar recálculos costosos en cada consulta.
* **Optimización:** Uso de `indexes` en campos clave (NIF, SKU, Fechas) para acelerar las búsquedas.

## 2. Clasificación de Entidades

### 2.1. Entidades Maestras (App `core`)
* **Cliente:** Información fiscal y de contacto. Incluye validaciones de unicidad en NIF y Email.
* **Producto:** Catálogo de artículos con gestión de precios base y tipos de IVA parametrizables.

### 2.2. Entidades Transaccionales (App `ventas`)
* **EstadoPedido:** Tabla maestra para gestionar los estados del flujo de venta (Borrador, Confirmado, Facturado, Cobrado).
* **Pedido:** Cabecera de la venta. Vincula al cliente con el estado actual y los totales económicos.
* **Línea de Pedido:** Detalle de la venta.

## 3. Estructura de Datos (Esquema ER)

### Tabla: CLIENTE
| Campo | Tipo | Notas |
| :--- | :--- | :--- |
| **id** | Integer | **PK** |
| nif | String | **Unique Index** (Clave natural) |
| nombre | String | |
| email | String | **Unique** |
| created_at | DateTime | Auditoría |

### Tabla: PRODUCTO
| Campo | Tipo | Notas |
| :--- | :--- | :--- |
| **id** | Integer | **PK** |
| sku | String | **Unique Index** (Referencia) |
| nombre | String | **Index** (Búsqueda) |
| precio_base | Decimal | Precio sin IVA |
| tipo_iva | Decimal | Ej: 0.21 (21%) |

### Tabla: ESTADO_PEDIDO
| Campo | Tipo | Notas |
| :--- | :--- | :--- |
| **id** | Integer | **PK** |
| nombre | String | **Unique** (Borrador, Confirmado...) |

### Tabla: PEDIDO
| Campo | Tipo | Notas |
| :--- | :--- | :--- |
| **id** | Integer | **PK** |
| fecha | DateTime | Auto-generada |
| total_neto | Decimal | Campo calculado (Denormalizado) |
| **cliente_id** | Integer | **FK** -> Cliente (Indexado) |
| **estado_id** | Integer | **FK** -> EstadoPedido |

### Tabla: LINEA_PEDIDO
| Campo | Tipo | Notas |
| :--- | :--- | :--- |
| **id** | Integer | **PK** |
| cantidad | Decimal | |
| precio_unitario| Decimal | **Snapshot** (Copia del producto) |
| tipo_iva | Decimal | **Snapshot** (Copia del producto) |
| **pedido_id** | Integer | **FK** -> Pedido (OnDelete: Cascade) |
| **producto_id** | Integer | **FK** -> Producto |