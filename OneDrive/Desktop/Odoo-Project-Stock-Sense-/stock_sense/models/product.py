# pyrefly: ignore [missing-import]
from odoo import models, fields

class Product(models.Model):
    _name = 'stock_sense.product'
    _description = 'Product'

    name = fields.Char(string='Product Name', required=True)
    sku = fields.Char(string='SKU / Reference', required=True, copy=False)
    category_id = fields.Many2one('stock_sense.product.category', string='Category')
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure', required=True, default=lambda self: self.env.ref('uom.product_uom_unit').id)
    reordering_min_qty = fields.Float(string='Minimum Reorder Quantity', default=0.0)
    qty_available = fields.Float(string='Available Quantity', compute='_compute_qty_available')

    def _compute_qty_available(self):
        for record in self:
            # Placeholder for compute logic based on moves
            record.qty_available = 0.0

class ProductCategory(models.Model):
    _name = 'stock_sense.product.category'
    _description = 'Product Category'

    name = fields.Char(string='Category Name', required=True)
    parent_id = fields.Many2one('stock_sense.product.category', string='Parent Category')
