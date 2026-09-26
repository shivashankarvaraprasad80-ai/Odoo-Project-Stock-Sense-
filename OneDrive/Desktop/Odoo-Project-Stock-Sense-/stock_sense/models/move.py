from odoo import models, fields

class StockMove(models.Model):
    _name = 'stock_sense.move'
    _description = 'Stock Move Ledger'

    name = fields.Char(string='Description')
    product_id = fields.Many2one('stock_sense.product', string='Product', required=True)
    qty = fields.Float(string='Quantity', required=True)
    location_id = fields.Many2one('stock_sense.location', string='Source Location')
    location_dest_id = fields.Many2one('stock_sense.location', string='Destination Location')
    picking_id = fields.Many2one('stock_sense.picking', string='Transfer Reference')
    date = fields.Datetime(string='Date', default=fields.Datetime.now)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ], string='Status', default='draft')
