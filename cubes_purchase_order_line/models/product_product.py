from odoo import models, fields, api


class ProductProductInherit(models.Model):
    _inherit = "product.product"

    last_price = fields.Float(string="Last Price", readonly=True, compute="_compute_last_price", default=0.0)

    @api.depends("seller_ids")
    def _compute_last_price(self):
        for line in self:
            if line.seller_ids:
                seller_ids = line.seller_ids.sorted(reverse=True)
                line.last_price = float(seller_ids[0].price)
            else:
                line.last_price = 0.0
