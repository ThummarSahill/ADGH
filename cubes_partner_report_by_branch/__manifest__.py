# -*- coding: utf-8 -*-
{
    "name": "Partner Report By Branch",
    "summary": """Partner Report By Branch""",
    "description": """Partner Report By Branch""",
    "category": "Uncategorized",
    "version": "17.0",
    "depends": ["base", "report_xlsx", "sale_order_by_group", "account_accountant", "sale_management", "contacts"],
    "data": ["security/ir.model.access.csv", "views/res_partner_view.xml", "wizard/res_partner_report_wizard_view.xml", "reports/report.xml"],
    "license": "LGPL-3",
}
