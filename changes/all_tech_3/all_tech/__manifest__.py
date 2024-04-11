{
    'name': 'All Tech',
    'version': '1.0',
    'summary': 'All Tech Shop',
    'author': 'all_tech',
    'sequence': -100,
    'description': """All Tech Module""",
    'category': 'SHOP',
    'depends': ['base', 'mail'],
    'data': [
        'wizard/report.xml',
        'wizard/xslx_report.xml',
        'security/security.xml',
        'security/security_rule.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/customer_view.xml',
        'views/supplier_view.xml',
        'views/invoice_view.xml',
        'views/product_view.xml',
        'views/category_view.xml',
        'views/department_view.xml',
        'views/employee_view.xml',
        'views/menu.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'assets': {},
    'license': 'LGPL-3',
}
