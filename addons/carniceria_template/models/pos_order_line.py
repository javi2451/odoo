# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PosOrderLine(models.Model):
    """Extensión de pos.order.line para agregar el campo translated_product_name.

    El widget 'product_label_section_and_note_field' utilizado en la vista de
    formulario de pos.order (heredado de account) solicita este campo al hacer
    web_read sobre pos.order.line. Sin esta definición, Odoo lanza:
        ValueError: Invalid field 'translated_product_name' on 'pos.order.line'
    """
    _inherit = 'pos.order.line'

    translated_product_name = fields.Text(
        string='Translated Product Name',
        compute='_compute_translated_product_name',
    )

    @api.depends('product_id')
    def _compute_translated_product_name(self):
        for line in self:
            if line.product_id:
                line.translated_product_name = line.product_id.with_context(
                    lang=line.order_id.partner_id.lang or self.env.lang
                ).display_name
            else:
                line.translated_product_name = False
