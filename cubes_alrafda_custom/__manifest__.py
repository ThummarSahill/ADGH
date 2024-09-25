{
    "name": "Cubes Alrafda Custom",
    "author": "Cubes Alrafda Custom",
    "category": "Category",
    "description": """Cubes Alrafda Custom Module""",
    # data files always loaded at installation
    "version": "17.0",
    "depends": [
        "base",
        "stock",
        "sale",
        "purchase",
        "account",
    ],
    "data": [
        "security/security.xml",
        "view/sale_order_edited_view.xml",
        "view/account_move_edited_view.xml",
        "view/product_edited_view.xml",
        "view/account_payment_edited_view.xml",
        "reports/report_payment_edited.xml",
        "reports/report_sale_order_edited.xml",
    ],
    "installable": True,
    "auto_install": False,
    "license": "AGPL-3",
}
