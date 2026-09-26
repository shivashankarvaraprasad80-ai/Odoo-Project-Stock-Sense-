from odoo import models, fields, api

class Warehouse(models.Model):
    _name = 'stock_sense.warehouse'
    _description = 'Warehouse'

    name = fields.Char(string='Warehouse Name', required=True)
    code = fields.Char(string='Short Code', required=True)
    location_ids = fields.One2many('stock_sense.location', 'warehouse_id', string='Locations')

class Location(models.Model):
    _name = 'stock_sense.location'
    _description = 'Location'
    _parent_store = True

    name = fields.Char(string='Location Name', required=True)
    warehouse_id = fields.Many2one('stock_sense.warehouse', string='Warehouse', required=True)
    parent_id = fields.Many2one('stock_sense.location', string='Parent Location', index=True)
    parent_path = fields.Char(index=True, unaccent=False)
    type = fields.Selection([
        ('view', 'View'),
        ('internal', 'Internal'),
        ('customer', 'Customer Location'),
        ('supplier', 'Vendor Location'),
        ('inventory', 'Inventory Loss'),
        ('transit', 'Transit Location')
    ], string='Location Type', default='internal')
