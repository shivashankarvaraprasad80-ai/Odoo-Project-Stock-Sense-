from odoo import models, fields

class Partner(models.Model):
    _name = 'stock_sense.partner'
    _description = 'Contact / Partner'

    name = fields.Char(string='Name', required=True)
    partner_type = fields.Selection([
        ('customer', 'Customer'),
        ('supplier', 'Supplier')
    ], string='Type', default='customer')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
