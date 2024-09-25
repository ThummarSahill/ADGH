from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    branch_id = fields.Many2one(related="sale_id.branch_id", store=True, string="الفرع", readonly=True)
