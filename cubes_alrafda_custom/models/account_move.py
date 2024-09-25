from odoo import models, fields, api


class Invoice(models.Model):
    _inherit = "account.move"

    partner_credit_x = fields.Monetary(related="partner_id.credit")


class InvoiceLine(models.Model):
    _inherit = "account.move.line"

    readonly_group_invoice = fields.Boolean(readonly=True, store=False)

    @api.model
    def default_get(self, fields):
        res = super(InvoiceLine, self).default_get(fields)
        readonly = self.env.user.has_group("cubes_alrafda_custom.group_invoice_price_readonly")
        if readonly:
            res.update({"readonly_group_invoice": True})
        else:
            res.update({"readonly_group_invoice": False})
        return res
