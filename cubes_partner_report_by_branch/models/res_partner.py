from odoo import models, fields, api


class ResPartnerInherit(models.Model):
    _inherit = "res.partner"

    branch_id = fields.Many2one("sale.order.branch", string="الفرع")

    # unreconciled_aml_ids
