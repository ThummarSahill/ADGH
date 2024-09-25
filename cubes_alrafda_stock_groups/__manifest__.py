{
    'name': "Cubes Alrafda Stock Access Right Custom",
    'version': '1.0',
    'depends': ['base', 'stock','product'],
    'author': "Cubes",

    'category': 'Category',
    'description': """
    Cubes Alrafda Stock Access Right Custom made by Abdalwahed Freaa at 2023-02-22
    """,
    # data files always loaded at installation
    'data': [
        'security/security.xml',
        'view/stock_view_edited.xml',
    ],

    'installable': True,
    'auto_install': False,
    'license': 'AGPL-3',
}
