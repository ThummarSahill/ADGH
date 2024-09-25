from odoo import models, fields


class StockQuantInherit(models.Model):
    _inherit = "stock.quant"

    ah_product_category = fields.Many2one("product.category", related="product_id.categ_id", string="Product Category2", store=True)
