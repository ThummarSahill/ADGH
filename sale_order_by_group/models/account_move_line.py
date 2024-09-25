from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    branch_id = fields.Many2one("sale.order.branch", related="move_id.branch_id", store=True, string="الفرع")
