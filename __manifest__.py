# -*- coding: utf-8 -*-
{
    'name' : 'yousentech_sale_reports',
    # 'version' : '1.1.1.0',
    'summary': 'yousentech_sale_reports dynamic',
    'sequence': -1,
    'description': """OWL yousentech_sale_reports dynamic""",
    'category': 'sale',
    'depends' : ['base', 'web','hr','purchase' ,'sale',  'stock','yousentech_accounts','report_xlsx'],
   
    'demo': [
    ],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_backend': [
            'yousentech_sale_reports/static/src/components/sales_dy.js',
            'yousentech_sale_reports/static/src/components/sales_dy.xml',
            'yousentech_sale_reports/static/src/components/sales_profit_margin_dy.js',
            'yousentech_sale_reports/static/src/components/sales_profit_margin_dy.xml',
            'yousentech_sale_reports/static/src/components/daily_sales_dy.js',
            'yousentech_sale_reports/static/src/components/daily_sales_dy.xml',
                      
        ],
    },
    
    'data': [
        'security/ir.model.access.csv',
        'views/sales.xml',
        'views/sales_profit_margin.xml',
        'views/daily_sales.xml',
        'views/menus.xml',
        'pdf_templates/sale_temp.xml',
        'pdf_templates/daily_sale_temp.xml',
        'pdf_templates/profit_margin.xml',
        'pdf_templates/profit_margin.xml',

    ],
}