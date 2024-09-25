from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def _default_warehouse_id(self):
        # !!! Any change to the default value may have to be repercuted
        # on _init_column() below.
        return self.env.user._get_default_warehouse_id()

    warehouse_id = fields.Many2one(
        "stock.warehouse",
        "Warehouse",
        copy=False,
        default=_default_warehouse_id,
        # domain=lambda self: [('id', 'in', self.env.user.warehouse_ids.ids)],
        readonly=False,
    )

    @api.onchange("company_id")
    def _onchange_company_id(self):
        return False

    @api.onchange("user_id")
    def onchange_user_id(self):
        return False

    analytic_account_id = fields.Many2one(
        "account.analytic.account",
        "Analytic Account",
        readonly=True,
        copy=False,
        check_company=True,  # Unrequired company
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        help="The analytic account related to a sales order.",
        default=lambda self: self.env.user.analytic_account_ids.id,
    )


class Warehouse(models.Model):
    _inherit = "stock.warehouse"

    @api.model
    def create(self, vals):
        self.env.registry.clear_all_caches()
        return super(Warehouse, self).create(vals)

    def write(self, vals):
        self.env.registry.clear_all_caches()
        return super(Warehouse, self).write(vals)


class PickingType(models.Model):
    _inherit = "stock.picking.type"

    @api.model
    def create(self, vals):
        self.env.registry.clear_all_caches()
        return super(PickingType, self).create(vals)

    def write(self, vals):
        self.env.registry.clear_all_caches()
        return super(PickingType, self).write(vals)


class Picking(models.Model):
    _inherit = "stock.picking"

    @api.model
    def create(self, vals):
        self.env.registry.clear_all_caches()
        return super(Picking, self).create(vals)

    def write(self, vals):
        self.env.registry.clear_all_caches()
        return super(Picking, self).write(vals)
