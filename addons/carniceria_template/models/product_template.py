# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    es_corte_carne = fields.Boolean(
        string='Es corte de carne',
        help='Indica si este producto es un corte específico de carnicería.'
    )
    
    dias_maduracion = fields.Integer(
        string='Días de Maduración (Añejamiento)',
        help='Tiempo óptimo de maduración antes de venta (Dry Aged o Wet Aged).'
    )
    
    tipo_corte = fields.Selection([
        ('primario', 'Primario (Mayorista/Desposte)'),
        ('secundario', 'Secundario (Mostrador)'),
        ('subproducto', 'Subproducto (Grasa, Hueso)'),
        ('procesado', 'Procesado (Embutidos, Preparados)')
    ], string='Tipo de Corte Carnicería')
