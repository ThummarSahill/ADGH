# -*- coding: utf-8 -*-
# -**------------ Manifest Start -------------------------------------**
{
    "name": "Cubes Accounting Report Custom",
    "summary": "Print PDF Accounting Reports",
    "version": "17.0",
    "category": "Human Resources/Contracts",
    "author": "Cubes,Ahmed Abdu",
    "depends": ["account", "report_xlsx"],
    "data": [
        "security/ir.model.access.csv",
        # "wizard/trial_balance.xml",
        "reports/reports_details.xml",
        "reports/voucher_report.xml",
        # "reports/report_trial_balance.xml",
        "views/account_payment.xml",
    ],
    "installable": True,
    "auto_install": False,
    "application": False,
    "license": "LGPL-3",
}

# -*------------  End Of Manifest   -----------------------------------*
