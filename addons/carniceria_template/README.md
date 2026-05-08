# Plantilla para Carnicería (Odoo)

Módulo pre-configurado para negocios de carnicería en Odoo. 
Diseñado para la gestión y trazabilidad desde la compra de ganado en pie hasta la venta final de cortes al público.

---

## ⚠️ CONFIGURACIÓN CRÍTICA: Unidades de Medida

**¡MUY IMPORTANTE ANTES DE USAR EL MÓDULO!**
Para evitar errores matemáticos e inconsistencias en tu inventario (ej. ver `30,000` en stock cuando deberían ser `30` kilos), es **obligatorio** habilitar el soporte para múltiples unidades de medida y configurar correctamente tus productos.

### Instrucciones de Configuración Inicial:
1. En Odoo, dirígete a la aplicación de **Ajustes** (Configuración) > **Inventario** > **Productos**.
2. Activa la casilla **"Unidades de Medida"** ("Sell and purchase products in different units of measure") y guarda los cambios.
3. Regla de Oro al crear o editar productos en el sistema:
   * 🐄 **Animales vivos (Ganado en pie):** La 'Unidad de Medida' debe ser **"Unidades"**.
   * 🥩 **Carnes y cortes (Canal, Molida, Lomo, etc):** La 'Unidad de Medida' debe ser **"kg"**. ¡Nunca en Unidades!

> **Nota:** Si omites este paso, Odoo asumirá que todos los productos se manejan en la unidad por defecto (Unidades) y al momento de validar operaciones en Kg (como la Faena o el Desposte), multiplicará las cantidades x1000 intentando hacer una conversión errónea al sistema métrico de referencia.

---

## Flujo Completo Implementado

1. **Compra de Ganado en Pie:** Registro de compras y número de cabezas adquiridas.
2. **Faena / Camal:** Proceso de beneficio con ingreso real de canales en (Kg). Costeo exacto que incluye el precio del ganado + servicios del camal + traslados. (Cálculo AVCO).
3. **Ingreso al Frigorífico:** Recepciones automatizadas del producto 'canal' a tu cámara principal.
4. **Distribución Interna:** Traslados entre frigorífico central y locales/puntos de venta.
5. **Desposte (Producción/Mrp):** Conversión de la canal en distintos cortes primarios y secundarios, mediante Listas de Materiales (BoM).
6. **Manejo de Mermas:** Registro para ajustes de inventario debido a la pérdida de peso de la carne (sangrados, mermas de corte).
7. **Punto de Venta (POS):** Ventas por kg directas en mostrador descontando stock en tiempo real. 

---
---

## ☁ Despliegue y Arquitectura en la Nube (Hosting)

Para llevar este sistema a producción con un cliente real y que esté accesible por internet para todas las áreas de la carnicería, sigue estas recomendaciones de infraestructura:

### Opciones de Arquitectura
1. **VPS "Todo en Uno" (Recomendado para PYMES):** 
   - Alquila un servidor Linux (ej. Ubuntu 22.04 o 24.04) en un proveedor cloud como **Google Cloud Platform (Compute Engine)**, **DigitalOcean**, o **AWS**.
   - **Requisito mínimo:** 2 GB de RAM (Recomendado 4 GB o instancia `e2-medium` en GCP) para soportar Odoo y la base de datos sin colapsos de memoria (OOM).
   - Instala PostgreSQL y el código fuente de Odoo en la misma máquina.
2. **Odoo.sh (Oficial de Odoo):** Si el cliente prefiere un enfoque administrado pagando una suscripción mensual, puedes vincular esta plantilla vía GitHub a un proyecto oficial de Odoo.sh.

### Fase de Pruebas (Testeo)
Si quieres simular la instalación paso a paso antes de tocar la nube o aprovechar los créditos gratuitos:
* **Entorno de Prueba Local:** Usa **WSL (Windows Subsystem for Linux)** o **VirtualBox** en tu computadora instalando Ubuntu Server. Esto te permite tener una consola en negro exacta a la de Google Cloud para practicar los comandos de instalación de Python, Postgres y Odoo con riesgo cero.
* **Bono Google Cloud:** GCP ofrece $300 USD de crédito gratuito por 90 días. Úsalo para crear tu máquina potente (`e2-medium`) y ensayar el despliegue pagando $0. No se recomienda usar su capa permanente de 1GB de RAM dado que Odoo require más capacidad al inicio.

---
_Módulo desarrollado por VYNX._
