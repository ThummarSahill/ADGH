from odoo import models, fields, api


class ProductTemplateInherit(models.Model):
    _inherit = "product.template"

    readonly_group = fields.Boolean(readonly=True, store=False)

    @api.model
    def default_get(self, fields):
        res = super(ProductTemplateInherit, self).default_get(fields)
        readonly = self.env.user.has_group("cubes_alrafda_custom.group_sale_price_readonly")
        if readonly:
            res.update({"readonly_group": True})
        else:
            res.update({"readonly_group": False})
        return res


class ProductProductInherit(models.Model):
    _inherit = "product.product"

    readonly_group = fields.Boolean(readonly=True, store=False)

    last_purchase_price = fields.Float(compute="get_last_purchase_price", readonly=True, store=False)
    last_purchase_currency = fields.Many2one("res.currency", compute="get_last_purchase_price", readonly=True, store=False)

    def get_last_purchase_price(self):
        for elem in self:
            elem.last_purchase_currency = False
            elem.last_purchase_price = False
            purchase_line = self.env["purchase.order.line"].search([("product_id", "=", elem.id), ("state", "in", ["done", "purchase"])])

            if purchase_line:
                last_purchase = max([elem.create_date for elem in purchase_line])

                purchase_line = self.env["purchase.order.line"].search([("product_id", "=", elem.id), ("state", "in", ["done", "purchase"]), ("create_date", "=", str(last_purchase))], limit=1)

                elem.last_purchase_currency = purchase_line.currency_id.id
                elem.last_purchase_price = purchase_line.price_unit

    @api.model
    def default_get(self, fields):
        res = super(ProductProductInherit, self).default_get(fields)
        readonly = self.env.user.has_group("cubes_alrafda_custom.group_sale_price_readonly")
        if readonly:
            res.update({"readonly_group": True})
        else:
            res.update({"readonly_group": False})
        return res
