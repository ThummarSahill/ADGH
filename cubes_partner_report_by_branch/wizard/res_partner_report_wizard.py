from odoo import models, fields


class ResPartnerByBranch(models.TransientModel):
    _name = "partner.account.report"

    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)
    branch_ids = fields.Many2many("sale.order.branch", string="Branches")

    def action_print(self):
        data = self.read()[0]
        datas = {"ids": [], "model": "partner.account.report", "form": data}
        return {
            "type": "ir.actions.report",
            "data": data,
            "report_name": "cubes_partner_report_by_branch.report_branch_xlsx",
            "report_type": "xlsx",
            "report_file": "Excel Partners Report By Branches Sheet.xlsx",
        }


class ResPartnerByBranchesXlsx(models.AbstractModel):
    _name = "report.cubes_partner_report_by_branch.report_branch_xlsx"
    _inherit = "report.report_xlsx.abstract"

    def generate_xlsx_report(self, workbook, data, wizard):
        report_name = "Partners Report By Branches"
        worksheet = workbook.add_worksheet(report_name[:31])

        worksheet.set_column("A:A", 25)
        worksheet.set_column("B:B", 20)
        worksheet.set_column("C:C", 20)
        worksheet.set_column("D:D", 25)
        worksheet.set_column("E:E", 20)
        worksheet.set_column("F:F", 30)
        worksheet.set_column("G:G", 20)
        worksheet.set_column("H:H", 20)
        worksheet.set_column("I:I", 20)
        worksheet.set_column("J:J", 20)
        worksheet.set_column("K:K", 20)
        worksheet.set_column("L:L", 20)
        worksheet.set_column("M:M", 20)
        worksheet.set_column("N:N", 20)
        worksheet.set_column("O:O", 20)
        worksheet.set_column("P:P", 20)
        worksheet.set_column("Q:Q", 20)
        worksheet.set_column("R:R", 20)
        worksheet.set_column("S:S", 20)

        head = workbook.add_format({"align": "center", "bold": True, "border": 1})
        table_head = workbook.add_format({"align": "left", "bold": True, "border": 1})
        table_line = workbook.add_format({"align": "center", "border": 1})

        start_date = wizard.start_date
        end_date = wizard.end_date
        branch_ids = wizard.branch_ids

        worksheet.merge_range(0, 3, 0, 4, "Partner Report By Branches", head)
        worksheet.write(1, 3, "From : %s" % start_date, head)
        worksheet.write(1, 4, "To : %s" % end_date, head)
        worksheet.write(4, 0, "Branch Name", head)
        worksheet.write(4, 1, "Partner Name", head)
        worksheet.write(4, 2, "Total Due", head)

        row = 5
        if not branch_ids:
            branch_ids = self.env["sale.order.branch"].search([])
        for branch in branch_ids:
            partners = self.env["res.partner"].search([("branch_id", "=", branch.id)])
            if partners:
                worksheet.write(row, 0, branch.name, table_line)
            for partner in partners:
                total_due = partner.unreconciled_aml_ids.filtered(lambda aml: start_date <= aml.date <= end_date).mapped("balance")
                if total_due:
                    total_due_formatted = sum(total_due)
                    worksheet.write(row, 1, partner.name, table_line)
                    worksheet.write(row, 2, "{:,.2f}".format(total_due_formatted), table_line)
                    row += 1
