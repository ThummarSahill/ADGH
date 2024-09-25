# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo.tools.misc import get_lang


class AccountBalanceReport(models.TransientModel):
    _name = "account.balance.report"
    _inherit = "account.common.report"
    _description = "Trial Balance Report"

    journal_ids = fields.Many2many(
        "account.journal",
        "account_balance_report_journal_rel",
        "account_id",
        "journal_id",
        string="Journals",
        required=True,
        default=[],
    )
    display_account = fields.Selection(
        [
            ("all", "All"),
            ("movement", "With movements"),
            ("not_zero", "With balance is not equal to 0"),
        ],
        string="Display Accounts",
        required=True,
        default="movement",
    )
    is_final_balance = fields.Boolean(string="Show Final Balance in report ?", required=False)

    def pre_print_report(self, data):
        data["form"].update(self.read(["display_account"])[0])
        return data

    def _print_report(self, data):
        data = self.pre_print_report(data)
        records = self.env[data["model"]].browse(data.get("ids", []))
        return self.env.ref("smt_accounting_reports.action_report_trial_balance").report_action(records, data=data)

    def button_export_xlsx(self):
        data = {}
        data["ids"] = self.env.context.get("active_ids", [])
        data["model"] = self.env.context.get("active_model", "ir.ui.menu")
        data["form"] = self.read(["date_from", "date_to", "journal_ids", "target_move", "company_id"])[0]
        used_context = self._build_contexts(data)
        data["form"]["used_context"] = dict(used_context, lang=get_lang(self.env).code)

        data = self.pre_print_report(data)
        records = self.env[data["model"]].browse(data.get("ids", []))
        print("-----data")
        return self.env.ref("smt_accounting_reports.action_report_trial_balance_xls").report_action(records, data=data)
