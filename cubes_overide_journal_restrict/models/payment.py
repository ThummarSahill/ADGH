# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, fields, models


class AccountPayment(models.Model):
    _inherit = "account.payment"

    destination_journal_id = fields.Many2one(
        comodel_name="account.journal",
        string="Destination Journal",
        # domain="[('type', 'in', ('bank','cash')), ('company_id', '=', company_id), ('id', '!=', journal_id)]",
        check_company=True,
    )

    select_dst_journal = fields.Selection(selection=lambda self: self.sudo().get_journals(), string="Select Destination Journals")

    def get_journals(self):
        return [(str(elem.id), str(elem.name)) for elem in self.env["account.journal"].search([("type", "in", ("bank", "cash"))])]

    @api.onchange("select_dst_journal")
    def change_destination_account_id(self):
        get_journal = self.sudo().env["account.journal"].search([("id", "=", int(self.select_dst_journal))])
        self.destination_journal_id = get_journal
