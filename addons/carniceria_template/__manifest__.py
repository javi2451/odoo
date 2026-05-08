# -*- coding: utf-8 -*-
{
    'name': 'Plantilla para Carnicería',
    'version': '1.2',
    'summary': 'Módulo pre-configurado para negocios de carnicería.',
    'description': """
Plantilla para Carnicería
=========================
Este módulo configura Odoo para operaciones típicas de una carnicería.

⚠️ CONFIGURACIÓN CRÍTICA: UNIDADES DE MEDIDA
=============================================================
ANTES de registrar operaciones, es obligatorio habilitar el soporte para kilos:
1. Ve a Ajustes (Configuración) > Inventario > Productos.
2. Activa la casilla "Unidades de Medida" y guarda.
3. Regla de Oro al crear/editar productos en el Inventario:
   ► Animales vivos (Ganado en pie): Unidad de Medida = "Unidades"
   ► Cortes de Carne (Canal, Molida, Lomo, etc): Unidad de Medida = "kg"
Si omites esto, Odoo asumirá "Unidades" y multiplicará los kilos x1000 al despostar o recibir faenas.

Flujo completo implementado:
=============================================================
⑴  🐄  Compra de Ganado en Pie
        → Órdenes de compra por kg
        → Registro de cabezas y peso vivo estimado

⑵  ⚖️  Faena / Camal
        → Registro de peso real beneficiado (kg)
        → Costo servicio camal + costo traslado
        → Cálculo automático de Costo Real por Kg
        → Validación actualiza AVCO automáticamente
        → Crea recepción en frigorífico al validar

⑶  📦  Ingreso a Inventario (Frigorífico Central)
        → Canal beneficiada ingresa con costo real
        → Valoración AVCO actualizada

⑷  🚚  Distribución a Puntos de Venta
        → Traslados internos: Frigorífico → Local 1 / Local 2
        → Registro de movimientos de inventario

⑸  🔪  Desposte en cada PV
        → Desmontaje (Unbuild) usando BOM tipo "normal"
        → 13 cortes: Ribeye, Lomo, Churrasco, Costilla,
          Asado, Bife, Bistec, Osobuco, Tapa, Marucha,
          Carne con Hueso, Carne Molida, Hueso/Subprod.
        → Merma del 10% registrada en carniceria.merma

⑹  📊  Costeo Automático
        → Costo real por corte (AVCO: ganado + camal + traslado)

⑺  🏪  Venta en TPV (POS)
        → Venta por kg en cada local
        → Descuento automático de stock

⑻  📈  Reportes
        → Ventas por mostrador y análisis de ventas
        → Historial de faenas con costos
        → Reporte de mermas consolidado
        → Stock en tiempo real por local
=============================================================
    """,
    'category': 'Industries',
    'author': 'VYNX',
    'website': 'https://vynx.group/',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'point_of_sale',
        'stock',
        'stock_account',
        'mrp',
        'sale_management',
        'purchase',
        'account',
        'mail',
    ],
    'data': [
        'security/ir.model.access.csv',
        # Configuración base: secuencias, empresa
        'data/company_config_data.xml',
        # Categorías de productos cárnicos
        'data/product_category_data.xml',
        # 5 Puntos de Venta (Removido temporalmente por falta de plan contable en BD actual)
        # 'data/pos_config_data.xml',
        # Almacenes: Frigorífico Central + Local 1 + Local 2
        'data/stock_warehouse_data.xml',
        # Vistas: ficha de producto con datos de carnicería
        'views/product_views.xml',
        # Vistas: registro de faena / camal
        'views/carniceria_faena_views.xml',
        # Vistas: control de mermas
        'views/carniceria_merma_views.xml',
        # Menú principal "🥩 Carnicería"
        'views/carniceria_main_menu.xml',
    ],
    'demo': [
        'demo/product_demo.xml',
        # BOM de desposte - cargado después de los productos demo
        'data/mrp_bom_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
