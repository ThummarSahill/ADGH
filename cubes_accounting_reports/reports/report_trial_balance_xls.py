# -*- coding: utf-8 -*-

import time
from odoo import api, models, _
from odoo.exceptions import UserError


class ReportTrialBalanceXls(models.AbstractModel):
    _name = "report.smt_accounting_reports.xlsx_trialbalance"
    _inherit = "report.report_xlsx.abstract"

    def generate_xlsx_report(self, workbook, data, lines):
        result = self.env["report.smt_accounting_reports.report_trialbalance"]._get_report_values(self, data=data)
        account_res = result["Accounts"]
        data = result["data"]
        format1 = workbook.add_format(
            {
                "font_size": 14,
                "align": "center",
                "bold": True,
                "bg_color": "#d3dde3",
                "color": "black",
                "bottom": True,
                "text_wrap": True,
                "valign": "vcenter",
            }
        )
        format2 = workbook.add_format(
            {
                "font_size": 11,
                "align": "center",
                "bold": True,
                "bg_color": "#edf4f7",
                "valign": "vcenter",
                "color": "black",
                "num_format": "#,##0.00",
                "text_wrap": True,
                "border": 1,
            }
        )
        format2_num = workbook.add_format(
            {
                "font_size": 11,
                "align": "right",
                "bold": True,
                "bg_color": "#edf4f7",
                "color": "black",
                "num_format": "#,##0.00",
                "text_wrap": True,
                "border": 1,
            }
        )
        format3 = workbook.add_format(
            {
                "font_size": 11,
                "align": "center",
                "bold": False,
                "num_format": "#,##0.00",
                "text_wrap": True,
                "border": 1,
            }
        )
        format3_num = workbook.add_format(
            {
                "font_size": 11,
                "align": "right",
                "bold": False,
                "num_format": "#,##0.00",
                "text_wrap": True,
                "border": 1,
            }
        )

        format5 = workbook.add_format(
            {
                "font_size": 12,
                "align": "vcenter",
                "bold": False,
                "text_wrap": True,
            }
        )

        sheet = workbook.add_worksheet(_("Trial Balance Report"))
        lang = data["used_context"].get("lang", False)
        if lang == "ar_001":
            sheet.right_to_left()
        sheet.set_column("B:B", 12)
        sheet.set_column("C:C", 25)
        sheet.set_column("D:K", 18)
        sheet.set_column("L:L", 13)
        sheet.set_default_row(25)

        company_name = self.env.company.name

        sheet.merge_range(1, 1, 3, 5, _("Trial Balance For Accounts"), format1)
        # Filters
        sheet.write(5, 1, _("Date From"), format5)
        sheet.write(5, 2, data["date_from"], format5)
        sheet.write(5, 4, _("Date To"), format5)
        sheet.write(5, 5, data["date_to"], format5)

        header_col = [
            _("Account No."),
            _("Account Name"),
            _("Initial Balance Debit Side"),
            _("Initial Balance Credit side"),
            _("Initial Balance"),
            _("Movement of Debit Side"),
            _("Movement of Credit Side"),
            _("Ending Balance Debit Side"),
            _("Ending Balance Credit Side"),
            _("Ending Balance"),
            _("Balances Difference"),
        ]
        # write data table
        row = 7
        col = 1
        for h in header_col:
            sheet.write(row, col, h, format2)
            col += 1
        row = 8
        col = 1
        col_1 = col_2 = col_3 = col_4 = col_5 = col_6 = col_7 = col_8 = col_9 = 0
        for account in account_res:
            col = 1
            sheet.write(row, col, account["code"], format3)
            col += 1
            sheet.write(row, col, account["name"], format3)
            col += 1
            sheet.write(row, col, account["debit"], format3_num)
            col += 1
            sheet.write(row, col, account["credit"], format3_num)
            col += 1
            sheet.write(row, col, account["balance"], format3_num)
            col += 1
            sheet.write(row, col, account["debit"], format3_num)
            col += 1
            sheet.write(row, col, account["credit"], format3_num)
            col += 1
            first = account["debit"] - account["credit"]
            sheet.write(row, col, first, format3_num)
            col += 1
            second = account["credit"] - account["debit"]
            sheet.write(row, col, second, format3_num)
            col += 1
            sheet.write(row, col, second, format3_num)
            col += 1
            different = account["balance"] + (account["credit"] - account["debit"])
            sheet.write(row, col, different, format3_num)
            col += 1
            row += 1
            # summation
            col_1 = col_1 + (account["debit"] and account["debit"] or 0)
            col_2 = col_2 + (account["credit"] and account["credit"] or 0)
            col_3 = col_3 + (account["balance"] and account["balance"] or 0)
            col_4 = col_4 + (account["debit"] and account["debit"] or 0)
            col_5 = col_5 + (account["credit"] and account["credit"] or 0)
            col_6 = col_6 + (first and first or 0)
            col_7 = col_7 + (second and second or 0)
            col_8 = col_8 + (second and second or 0)
            col_9 = col_9 + (different and different or 0)

        col = 1
        # write totals
        sheet.write(row, col, "-", format2)
        col += 1
        sheet.write(row, col, _("Total"), format2)
        col += 1
        sheet.write(row, col, col_1, format2_num)
        col += 1
        sheet.write(row, col, col_2, format2_num)
        col += 1
        sheet.write(row, col, col_3, format2_num)
        col += 1
        sheet.write(row, col, col_4, format2_num)
        col += 1
        sheet.write(row, col, col_5, format2_num)
        col += 1
        sheet.write(row, col, col_6, format2_num)
        col += 1
        sheet.write(row, col, col_7, format2_num)
        col += 1
        sheet.write(row, col, col_8, format2_num)
        col += 1
        sheet.write(row, col, col_9, format2_num)
        col += 1
