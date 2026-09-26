from odoo import models, fields, api

class Picking(models.Model):
    _name = 'stock_sense.picking'
    _description = 'Transfer / Picking'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    partner_id = fields.Many2one('stock_sense.partner', string='Contact')
    picking_type = fields.Selection([
        ('incoming', 'Receipt'),
        ('outgoing', 'Delivery Order'),
        ('internal', 'Internal Transfer')
    ], string='Operation Type', required=True)
    location_id = fields.Many2one('stock_sense.location', string='Source Location', required=True)
    location_dest_id = fields.Many2one('stock_sense.location', string='Destination Location', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('ready', 'Ready'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ], string='Status', default='draft')
    line_ids = fields.One2many('stock_sense.picking.line', 'picking_id', string='Operations')

    def action_confirm(self):
        self.write({'state': 'ready'})

    def action_validate(self):
        self.write({'state': 'done'})
        # Auto-create moves
        for line in self.line_ids:
            self.env['stock_sense.move'].create({
                'product_id': line.product_id.id,
                'qty': line.qty,
                'location_id': self.location_id.id,
                'location_dest_id': self.location_dest_id.id,
                'picking_id': self.id,
                'state': 'done'
            })

class PickingLine(models.Model):
    _name = 'stock_sense.picking.line'
    _description = 'Transfer Line'

    picking_id = fields.Many2one('stock_sense.picking', string='Transfer')
    product_id = fields.Many2one('stock_sense.product', string='Product', required=True)
    qty = fields.Float(string='Quantity', required=True, default=1.0)
