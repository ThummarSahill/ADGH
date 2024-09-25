from odoo import models, fields, api


class PurchaseOrderLineInherit(models.Model):
    _inherit = "purchase.order.line"

    last_purchase_price = fields.Float(string="Last Purchase Price", compute="_compute_last_purchase_price")

    @api.onchange("product_id", "product_qty", "price_unit", "taxes_id")
    def _compute_last_purchase_price(self):
        for line in self:
            line.last_purchase_price = 0
            if line.product_id:
                seller_ids = line.product_id.seller_ids.sorted(reverse=True)
                if seller_ids:
                    line.last_purchase_price = seller_ids[0].price
