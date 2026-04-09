# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CarniceriaMerma(models.Model):
    _name = 'carniceria.merma'
    _description = 'Registro de Merma en Carnicería'
    _order = 'fecha desc'

    name = fields.Char(
        string='Referencia',
        required=True,
        readonly=True,
        default='/',
        copy=False
    )
    fecha = fields.Date(
        string='Fecha',
        required=True,
        default=fields.Date.context_today
    )
    product_id = fields.Many2one(
        'product.product',
        string='Producto',
        required=True,
        domain=[('es_corte_carne', '=', True)]
    )
    cantidad_kg = fields.Float(
        string='Cantidad Merma (kg)',
        required=True,
        digits=(10, 3)
    )
    tipo_merma = fields.Selection([
        ('desposte', 'Desposte / Transformación'),
        ('vencimiento', 'Vencimiento / Caducidad'),
        ('dano', 'Daño / Accidente'),
        ('devolucion', 'Devolución de Cliente'),
    ], string='Tipo de Merma', required=True, default='desposte')

    location_id = fields.Many2one(
        'stock.location',
        string='Almacén / Local',
        domain=[('usage', '=', 'internal')],
        required=True
    )
    costo_unitario = fields.Float(
        string='Costo Unitario (S/.)',
        related='product_id.standard_price',
        store=True,
        readonly=True
    )
    costo_total = fields.Float(
        string='Costo Total Merma (S/.)',
        compute='_compute_costo_total',
        store=True
    )
    observacion = fields.Text(string='Observaciones')
    scrap_id = fields.Many2one(
        'stock.scrap',
        string='Orden de Desecho',
        readonly=True
    )
    state = fields.Selection([
        ('borrador', 'Borrador'),
        ('confirmado', 'Confirmado'),
        ('procesado', 'Procesado en Inventario'),
    ], string='Estado', default='borrador', readonly=True)

    @api.depends('cantidad_kg', 'costo_unitario')
    def _compute_costo_total(self):
        for rec in self:
            rec.costo_total = rec.cantidad_kg * rec.costo_unitario

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', '/') == '/':
                vals['name'] = self.env['ir.sequence'].next_by_code('carniceria.merma') or 'MERMA/0001'
        return super().create(vals_list)

    def action_confirmar(self):
        for rec in self:
            if rec.cantidad_kg <= 0:
                raise ValidationError('La cantidad de merma debe ser mayor a 0 kg.')
            rec.state = 'confirmado'

    def action_procesar_inventario(self):
        """Crea una orden de desecho en el sistema de inventario de Odoo."""
        for rec in self:
            if rec.state != 'confirmado':
                raise ValidationError('Debes confirmar la merma antes de procesarla.')
            scrap = self.env['stock.scrap'].create({
                'product_id': rec.product_id.id,
                'scrap_qty': rec.cantidad_kg,
                'product_uom_id': self.env.ref('uom.product_uom_kgm').id,
                'location_id': rec.location_id.id,
                'origin': rec.name,
            })
            scrap.action_validate()
            rec.scrap_id = scrap.id
            rec.state = 'procesado'

    def action_ver_desecho(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Orden de Desecho',
            'res_model': 'stock.scrap',
            'view_mode': 'form',
            'res_id': self.scrap_id.id,
        }
