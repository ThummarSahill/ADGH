from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _check_has_create(self):
        return self.env.user.has_group("cubes_product_access.product_management_group_create")

    has_create_product = fields.Boolean(compute="check_has_create_product", default=_check_has_create)

    @api.depends_context("uid")
    def check_has_create_product(self):
        for rec in self:
            rec.has_create_product = True if self.env.user.has_group("cubes_product_access.product_management_group_create") else False


class StockMove(models.Model):
    _inherit = "stock.move"

    copy_product_id = fields.Many2one("product.product", string="Product", domain="[('type', 'in', ['product', 'consu'])]", change_default=True, ondelete="restrict", check_company=True)

    @api.onchange("copy_product_id")
    def _onchange_copy_product_id(self):
        for rec in self:
            if rec.copy_product_id:
                rec.product_id = rec.copy_product_id.id
