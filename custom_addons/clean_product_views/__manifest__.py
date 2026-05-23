# -*- coding: utf-8 -*-
{
    'name': "Clean Product Views",
    'summary': "Hides the 'Product Variants' menus to reduce clutter.",
    'description': """
        This module hides the 'Product Variants' menus across various apps (Inventory, POS, etc.)
        so that users only see the main 'Products' (product.template) menu, reducing clutter
        while still allowing 'Dynamic' variants to be created and tracked.
    """,
    'author': "Agent",
    'category': 'Customizations',
    'version': '1.0',
    'depends': ['base', 'product', 'stock', 'point_of_sale'],
    'data': [
        'views/menu_overrides.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
