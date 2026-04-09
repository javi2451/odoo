# -*- coding: utf-8 -*-
{
    'name': 'Plantilla para Carnicería',
    'version': '1.1',
    'summary': 'Módulo pre-configurado para negocios de carnicería.',
    'description': """
Plantilla para Carnicería
=========================
Este módulo configura Odoo para operaciones típicas de una carnicería.

Funcionalidades principales:
- ✅ Configuración en español (Perú) y moneda Sol (PEN).
- ✅ TPV / Mostrador con productos vendidos por peso (kg) y balanza.
- ✅ Proceso de Desposte (BOM) para transformar canales en cortes.
- ✅ Control de Mermas (con registro automático en inventario).
- ✅ Costo real por corte usando valoración AVCO.
- ✅ Inventario multi-almacén (Frigorífico + Locales de venta).
- ✅ Traslados de stock entre locales.
- ✅ Menú propio "🥩 Carnicería" con acceso a todas las funciones.
    """,
    'category': 'Industries',
    'author': 'VYNX',
    'website': 'https://www.vynx.com',
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
    ],
    'data': [
        'security/ir.model.access.csv',
        # Configuración base (empresa, idioma, moneda, secuencias)
        'data/company_config_data.xml',
        # Categorías de productos cárnicos
        'data/product_category_data.xml',
        # Configuración del TPV / Mostrador
        'data/pos_config_data.xml',
        # Almacenes: Frigorífico Central + Local Mostrador 1
        'data/stock_warehouse_data.xml',
        # Vistas: ficha de producto con datos de carnicería
        'views/product_views.xml',
        # Vistas: control de mermas
        'views/carniceria_merma_views.xml',
        # Menú principal "🥩 Carnicería"
        'views/carniceria_main_menu.xml',
    ],
    'demo': [
        'demo/product_demo.xml',
        # Listas de Materiales — Desposte de Canal de Res
        'data/mrp_bom_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
