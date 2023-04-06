# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Yummy Inventory Master API',
    'version': '13.0.1.0.0',
    'category': 'Inventory',
    'summary': 'Yummy Inventory Master API',
    'description': """
        This module IS API For Master Inventory
    """,
    'website': 'https://www.yummycorp.com',
    'author':'Yummy Corp.',
    'depends': ['base','stock','stock_account','web','product_activation','product_brand'],
    'data': [
        'views/yummy_api_config_server.xml',
        'views/yummy_api_productflag.xml',
        'views/yummy_api_config_client.xml',
        'views/yummy_invmaster_template.xml',
        'data/yummy_master_product_cron.xml',
    ],
    'qweb': [],
    'installable': True,
    'auto_install': True,
    'license': 'OEEL-1',
    'external_dependencies': {
        'python': ['pypeg2', 'requests']
    }
}
