# -*- coding: utf-8 -*-
##############################################################################

from odoo import api, fields, models


class Users(models.Model):
    _inherit = "res.users"

    @api.model
    def create(self, vals):
        self.env.registry.clear_all_caches()
        return super(Users, self).create(vals)

    def write(self, vals):
        self.env.registry.clear_all_caches()
        return super(Users, self).write(vals)

    analytic_account_ids = fields.Many2one(
        "account.analytic.account",
        string="Analytic Account",
        check_company=True,
    )
    # journal_id = fields.Many2many('account.journal', string='Journal', required=False, check_company=True,)
    warehouse_ids = fields.Many2many("stock.warehouse", string="Warehouse", required=False)

    def _get_default_warehouse_id(self):
        if self.property_warehouse_id:
            return self.property_warehouse_id
        if len(self.warehouse_ids.ids) == 1:
            return self.env["stock.warehouse"].search([("id", "=", self.warehouse_ids.id)])

    restrict_locations = fields.Boolean("Restrict Location")
    restrict_warehouse = fields.Boolean(readonly=True)
    restrict_journal = fields.Boolean(readonly=True)
    restrict_analytic = fields.Boolean(readonly=True)
    default_picking_type_ids = fields.Many2many("stock.picking.type", "stock_picking_type_users_rel", "user_id", "picking_type_id", string="Default Warehouse Operations")

class AccountReconcileModelLine(models.Model):
    _inherit = "account.reconcile.model.line"

    analytic_account_id = fields.Many2one(
        "account.analytic.account", string="Analytic Account", ondelete="set null", check_company=True, default=lambda self: self.env.user.analytic_account_ids.id, readonly=True
    )