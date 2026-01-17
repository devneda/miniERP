# MiniERP - Sistema de Gestión Empresarial

Este proyecto implementa la base de un sistema ERP sencillo utilizando Django, enfocado en la gestión de clientes, productos y pedidos de venta.

## 1. Justificación del Modelo de Datos

El diseño se ha modularizado en dos aplicaciones para separar responsabilidades: **Core** (datos estáticos) y **Ventas** (datos dinámicos).

### 1.1. Clasificación de Entidades

* **Entidades Maestras (`core`):**
    * **Cliente:** Representa a los actores que realizan las compras. Es un dato maestro porque su existencia es independiente de las transacciones.
    * **Producto:** Representa el catálogo de artículos disponibles. Es información estable que se referencia en múltiples ventas.

* **Entidades Transaccionales (`ventas`):**
    * **Pedido:** Representa el evento de venta ("Cabecera"). Depende del tiempo y de un cliente.
    * **Línea de Pedido:** Representa el detalle desglosado de la venta. Su existencia depende totalmente del Pedido al que pertenece.

### 1.2. Relaciones y Cardinalidades

Las relaciones se han implementado mediante claves foráneas (`ForeignKey`) siguiendo esta lógica:

1.  **Cliente - Pedido (1:N):**
    * *Relación:* Un Cliente puede realizar **N** Pedidos, pero un Pedido pertenece a **1** solo Cliente.
    * *Integridad:* Se usa `ON_DELETE=RESTRICT`. No se permite eliminar un Cliente si tiene pedidos históricos, preservando la integridad contable.

2.  **Pedido - LíneaPedido (1:N):**
    * *Relación:* Un Pedido se compone de **N** Líneas de detalle. Una Línea pertenece a **1** único Pedido.
    * *Integridad:* Se usa `ON_DELETE=CASCADE`. Es una relación de composición fuerte: si se borra la cabecera del pedido, sus líneas (detalles) dejan de tener sentido y se eliminan automáticamente.

3.  **Producto - LíneaPedido (1:N):**
    * *Relación:* Un Producto puede aparecer en **N** Líneas de diferentes pedidos.
    * *Integridad:* Se usa `ON_DELETE=RESTRICT`. No se puede eliminar un Producto del catálogo si ya ha sido vendido (está presente en líneas de pedido).

## 2. Diagrama Entidad-Relación (ER)

A continuación se representa la estructura de las tablas y sus relaciones:

```mermaid
erDiagram
    CLIENTE ||--o{ PEDIDO : realiza
    PEDIDO ||--|{ LINEA_PEDIDO : contiene
    PRODUCTO ||--o{ LINEA_PEDIDO : referencia

    CLIENTE {
        int id PK
        string nif UK "Unique"
        string nombre
        string email
        text direccion
    }

    PRODUCTO {
        int id PK
        string sku UK "Unique"
        string nombre
        decimal precio
    }

    PEDIDO {
        int id PK
        date fecha
        string estado "Enum: Borrador, Confirmado..."
        int cliente_id FK
    }

    LINEA_PEDIDO {
        int id PK
        int cantidad "Check > 0"
        decimal precio_unitario
        int pedido_id FK
        int producto_id FK
    }
    ```
