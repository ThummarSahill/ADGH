# -*- coding: utf-8 -*-
{
    "name": "Sale Order By Group",
    "summary": """
        Sale Order Visibility By Group
        """,
    "category": "Uncategorized",
    "version": "17.0",
    "depends": ["base", "sale", "sales_team", "sale_stock", "stock"],
    "data": [
        "security/ir.model.access.csv",
        "security/security.xml",
        "views/branch_view.xml",
        "views/res_user.xml",
        "views/sale_order.xml",
        "views/account_move.xml",
        "views/account_move_line_view.xml",
        "views/account_payment.xml",
        "views/stock_picking_view.xml",
        "views/menuitem.xml",
        "reports/external_layout.xml",
    ],
    "license": "LGPL-3",
}
