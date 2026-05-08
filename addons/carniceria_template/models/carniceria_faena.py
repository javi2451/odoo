# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CarniceriaFaena(models.Model):
    _name = 'carniceria.faena'
    _description = 'Registro de Faena / Beneficio en Camal'
    _order = 'fecha desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # ──────────────────────────────────────────────────────────
    # IDENTIFICACIÓN
    # ──────────────────────────────────────────────────────────
    name = fields.Char(
        string='Referencia',
        required=True,
        readonly=True,
        default='/',
        copy=False,
        tracking=True,
    )
    fecha = fields.Date(
        string='Fecha de Faena',
        required=True,
        default=fields.Date.context_today,
        tracking=True,
    )
    proveedor_camal_id = fields.Many2one(
        'res.partner',
        string='Camal / Proveedor',
        required=True,
        tracking=True,
        help='Proveedor del servicio de beneficio (camal).',
    )
    purchase_order_id = fields.Many2one(
        'purchase.order',
        string='Orden de Compra (Ganado en Pie)',
        domain=[('state', 'in', ['purchase', 'done'])],
        help='Orden de compra que originó la adquisición del ganado en pie.',
    )

    # ──────────────────────────────────────────────────────────
    # DATOS DEL GANADO
    # ──────────────────────────────────────────────────────────
    cantidad_cabezas = fields.Integer(
        string='Cantidad de Cabezas',
        required=True,
        default=1,
    )
    peso_vivo_total_kg = fields.Float(
        string='Peso Vivo Total (kg)',
        digits=(10, 2),
        help='Peso estimado del ganado en pie antes del sacrificio.',
    )
    costo_ganado_total = fields.Float(
        string='Costo Total Ganado (S/.)',
        digits=(10, 2),
        required=True,
        tracking=True,
    )

    # ──────────────────────────────────────────────────────────
    # DATOS DEL CAMAL
    # ──────────────────────────────────────────────────────────
    peso_beneficiado_kg = fields.Float(
        string='Peso Beneficiado Real (kg)',
        digits=(10, 3),
        required=True,
        tracking=True,
        help='Peso real de la canal limpia según el parte del camal.',
    )
    costo_servicio_camal = fields.Float(
        string='Costo Servicio Camal (S/.)',
        digits=(10, 2),
        help='Monto total cobrado por el camal por el servicio de beneficio.',
    )
    costo_traslado = fields.Float(
        string='Costo Traslado (S/.)',
        digits=(10, 2),
        help='Flete: transporte del campo al camal y del camal al frigorífico.',
    )

    # ──────────────────────────────────────────────────────────
    # CÁLCULOS AUTOMÁTICOS
    # ──────────────────────────────────────────────────────────
    rendimiento_pct = fields.Float(
        string='Rendimiento Camal (%)',
        compute='_compute_costos',
        store=True,
        digits=(5, 2),
        help='% de carne aprovechada sobre el peso vivo.',
    )
    costo_total_real = fields.Float(
        string='Costo Total Real (S/.)',
        compute='_compute_costos',
        store=True,
        digits=(10, 2),
        tracking=True,
    )
    costo_por_kg = fields.Float(
        string='Costo Real por Kg (S/.)',
        compute='_compute_costos',
        store=True,
        digits=(10, 4),
        help='Costo total dividido entre kg beneficiados. Se usa para actualizar AVCO.',
        tracking=True,
    )

    # ──────────────────────────────────────────────────────────
    # INVENTARIO
    # ──────────────────────────────────────────────────────────
    product_id = fields.Many2one(
        'product.product',
        string='Producto Canal (Res)',
        required=True,
        domain=[('es_corte_carne', '=', True), ('tipo_corte', '=', 'primario')],
        help='Producto de inventario que representa la canal beneficiada.',
    )
    warehouse_id = fields.Many2one(
        'stock.warehouse',
        string='Frigorífico Destino',
        required=True,
        help='Almacén donde se recibirá la canal para su posterior desposte.',
    )
    stock_picking_id = fields.Many2one(
        'stock.picking',
        string='Recepción en Inventario',
        readonly=True,
    )

    # ──────────────────────────────────────────────────────────
    # ESTADO Y NOTAS
    # ──────────────────────────────────────────────────────────
    state = fields.Selection([
        ('borrador', 'Borrador'),
        ('confirmado', 'Confirmado'),
        ('validado', 'Validado'),
    ], string='Estado', default='borrador', readonly=True, tracking=True)

    observacion = fields.Text(string='Observaciones')

    # ──────────────────────────────────────────────────────────
    # LÓGICA
    # ──────────────────────────────────────────────────────────
    @api.depends(
        'peso_vivo_total_kg', 'peso_beneficiado_kg',
        'costo_ganado_total', 'costo_servicio_camal', 'costo_traslado',
    )
    def _compute_costos(self):
        for rec in self:
            # Rendimiento camal
            if rec.peso_vivo_total_kg and rec.peso_vivo_total_kg > 0:
                rec.rendimiento_pct = (rec.peso_beneficiado_kg / rec.peso_vivo_total_kg) * 100.0
            else:
                rec.rendimiento_pct = 0.0

            # Costo total real
            rec.costo_total_real = (
                rec.costo_ganado_total
                + rec.costo_servicio_camal
                + rec.costo_traslado
            )

            # Costo real por kg (clave para AVCO)
            if rec.peso_beneficiado_kg and rec.peso_beneficiado_kg > 0:
                rec.costo_por_kg = rec.costo_total_real / rec.peso_beneficiado_kg
            else:
                rec.costo_por_kg = 0.0

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', '/') == '/':
                vals['name'] = (
                    self.env['ir.sequence'].next_by_code('carniceria.faena')
                    or 'FAENA/0001'
                )
        return super().create(vals_list)

    def action_confirmar(self):
        """Confirma la faena: valida datos mínimos."""
        for rec in self:
            if rec.peso_beneficiado_kg <= 0:
                raise ValidationError('El peso beneficiado debe ser mayor a 0 kg.')
            if rec.costo_ganado_total <= 0:
                raise ValidationError('El costo del ganado debe ser mayor a 0.')
            rec.state = 'confirmado'

    def action_validar(self):
        """
        Valida la faena. Al hacerlo:
          1. Actualiza el standard_price del producto canal con el costo real/kg
             → Odoo recalcula AVCO automáticamente en el siguiente movimiento.
          2. Crea un picking de recepción (entrada) al frigorífico destino.
        """
        for rec in self:
            if rec.state != 'confirmado':
                raise ValidationError('Confirma la faena antes de validarla.')
            if rec.costo_por_kg <= 0:
                raise ValidationError(
                    'El costo por kg calculado no es válido. '
                    'Verifica los costos y el peso beneficiado.'
                )

            # ── 1. Actualizar precio estándar (base AVCO) ─────────────────
            rec.product_id.product_tmpl_id.sudo().write({
                'standard_price': rec.costo_por_kg,
            })

            # ── 2. Crear recepción de inventario en el frigorífico ─────────
            picking_type = self.env['stock.picking.type'].search([
                ('warehouse_id', '=', rec.warehouse_id.id),
                ('code', '=', 'incoming'),
            ], limit=1)

            if not picking_type:
                raise ValidationError(
                    f'No se encontró operación de entrada para el almacén '
                    f'"{rec.warehouse_id.name}". Verifica la configuración.'
                )

            supplier_location = self.env.ref('stock.stock_location_suppliers')
            picking = self.env['stock.picking'].create({
                'picking_type_id': picking_type.id,
                'partner_id': rec.proveedor_camal_id.id,
                'origin': rec.name,
                'note': (
                    f'Faena: {rec.cantidad_cabezas} cabeza(s) — '
                    f'{rec.peso_beneficiado_kg:.2f} kg beneficiados — '
                    f'Costo/kg: S/ {rec.costo_por_kg:.4f}'
                ),
                'move_ids': [(0, 0, {
                    'description_picking': f'Canal de Res — Faena {rec.name}',
                    'product_id': rec.product_id.id,
                    'product_uom_qty': rec.peso_beneficiado_kg,
                    'product_uom': self.env.ref('uom.product_uom_kgm').id,
                    'location_id': supplier_location.id,
                    'location_dest_id': picking_type.default_location_dest_id.id,
                })],
            })
            picking.action_confirm()

            rec.stock_picking_id = picking.id
            rec.state = 'validado'

    def action_ver_recepcion(self):
        """Abre el picking de recepción creado al validar."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Recepción en Frigorífico',
            'res_model': 'stock.picking',
            'view_mode': 'form',
            'res_id': self.stock_picking_id.id,
            'target': 'current',
        }
