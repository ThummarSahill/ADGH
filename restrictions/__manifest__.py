# -*- coding: utf-8 -*-
{
    "name": "Restrictions",
    "category": "Uncategorized",
    "version": "17.0",
    # any module necessary for this one to work correctly
    "depends": [
        "base",
        "sale_stock",
        "account_accountant",
        "analytic",
        "sale_management",
    ],
    # always loaded
    "data": [
        "security/security.xml",
        "views/sale_order_view.xml",
        "views/user_views.xml",
    ],
    "license": "LGPL-3",
}
