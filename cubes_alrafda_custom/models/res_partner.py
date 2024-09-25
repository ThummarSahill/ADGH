from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"
    balance = fields.Monetary(compute="_calc_balance")

    @api.depends("debit", "credit")
    def _calc_balance(self):
        for rec in self:
            rec.balance = rec.credit - rec.debit
