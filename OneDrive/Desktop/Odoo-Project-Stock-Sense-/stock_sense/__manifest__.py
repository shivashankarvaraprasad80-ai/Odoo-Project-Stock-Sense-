# -*- coding: utf-8 -*-
{
    'name': 'StockSense Inventory Management',
    'version': '1.0',
    'category': 'Inventory/Inventory',
    'summary': 'Advanced modular Inventory Management System',
    'description': """
        StockSense Inventory Management System
        - User Roles (Manager, Staff)
        - Multi-Warehouse & Locations
        - Product Management (SKU, Category, UoM)
        - Receipts, Delivery Orders, Internal Transfers
        - Inventory Adjustments
        - Move History (Ledger)
        - Low Stock Alerts & Dashboard
    """,
    'author': 'StockSense',
    'depends': ['base', 'mail'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/menu_view.xml',
        'views/product_view.xml',
        'views/warehouse_view.xml',
        'views/picking_view.xml',
        'views/dashboard_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
