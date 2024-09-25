from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    partner_credit = fields.Monetary(related="partner_id.credit")
    balance = fields.Monetary(related="partner_id.balance")

    @api.returns("self", lambda value: value.id)
    def copy(self, default=None):
        default = dict(default or {})
        default["warehouse_id"] = self.warehouse_id.id if self.warehouse_id else False
        return super(SaleOrder, self).copy(default=default)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    readonly_group_sale = fields.Boolean(readonly=True, store=False)

    @api.model
    def default_get(self, fields):
        res = super(SaleOrderLine, self).default_get(fields)
        readonly = self.env.user.has_group("cubes_alrafda_custom.group_sale_price_readonly")
        if readonly:
            res.update({"readonly_group_sale": True})
        else:
            res.update({"readonly_group_sale": False})
        return res
