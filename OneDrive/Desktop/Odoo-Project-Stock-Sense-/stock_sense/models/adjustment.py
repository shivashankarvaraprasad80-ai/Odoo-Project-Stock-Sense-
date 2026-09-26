from odoo import models, fields, api

class InventoryAdjustment(models.Model):
    _name = 'stock_sense.adjustment'
    _description = 'Inventory Adjustment'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    location_id = fields.Many2one('stock_sense.location', string='Location', required=True)
    date = fields.Datetime(string='Date', default=fields.Datetime.now)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Validated')
    ], string='Status', default='draft')
    line_ids = fields.One2many('stock_sense.adjustment.line', 'adjustment_id', string='Adjustment Lines')

    def action_validate(self):
        self.write({'state': 'done'})
        # Create corresponding stock moves to reflect adjustment
        inventory_loss_location = self.env['stock_sense.location'].search([('type', '=', 'inventory')], limit=1)
        for line in self.line_ids:
            diff = line.counted_qty - line.theoretical_qty
            if diff != 0:
                loc_from = self.location_id.id if diff < 0 else inventory_loss_location.id
                loc_to = inventory_loss_location.id if diff < 0 else self.location_id.id
                self.env['stock_sense.move'].create({
                    'product_id': line.product_id.id,
                    'qty': abs(diff),
                    'location_id': loc_from,
                    'location_dest_id': loc_to,
                    'state': 'done'
                })

class InventoryAdjustmentLine(models.Model):
    _name = 'stock_sense.adjustment.line'
    _description = 'Inventory Adjustment Line'

    adjustment_id = fields.Many2one('stock_sense.adjustment', string='Adjustment')
    product_id = fields.Many2one('stock_sense.product', string='Product', required=True)
    theoretical_qty = fields.Float(string='Theoretical Quantity', readonly=True)
    counted_qty = fields.Float(string='Counted Quantity', required=True)
