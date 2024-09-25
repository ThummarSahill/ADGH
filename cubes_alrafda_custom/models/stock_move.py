from odoo import models, fields


class StockMoveInherit(models.Model):
    _inherit = "stock.move"

    _order = "default_code"

    default_code = fields.Char(related="product_id.default_code", store=True)

    # default_name = fields.Char(related='product_id.name', store=True)


class StockMoveLineInherit(models.Model):
    _inherit = "stock.move.line"

    _order = "default_code"

    default_code = fields.Char(related="product_id.default_code", store=True)

    # default_name = fields.Char(related='product_id.name', store=True)
