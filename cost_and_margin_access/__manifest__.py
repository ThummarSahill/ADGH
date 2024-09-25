# -*- coding: utf-8 -*-
{
    "name": "Cost and Margin Access Rights",
    "summary": """ Cost and Margin Access Rights""",
    "description": """create group for cost price and group for margin in sales.""",
    "depends": ["base", "purchase", "sale_margin", "mrp_account"],
    "data": ["security/groups.xml", "views/sale_order.xml"],
    "installable": True,
    "auto_install": False,
    "license": "LGPL-3",
}
