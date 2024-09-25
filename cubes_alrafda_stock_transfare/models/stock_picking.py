from odoo import models, fields, api


class StockMoveInherit(models.Model):
    _inherit = "stock.move.line"

    ah_available_quantity = fields.Float(string="Current Quantity", compute="get_ah_available_quantity")

    @api.onchange("product_id", "location_id")
    def get_ah_available_quantity(self):
        for elem in self:
            elem.ah_available_quantity = 0.0
            if elem.product_id and elem.location_id:
                quant_product_lines = self.env["stock.quant"].sudo().search([("product_id", "=", elem.product_id.id), ("location_id", "=", elem.location_id.id)])
                if quant_product_lines:
                    elem.ah_available_quantity = quant_product_lines.quantity
                else:
                    elem.ah_available_quantity = 0.0
