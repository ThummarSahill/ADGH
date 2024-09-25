from odoo import fields, models


class AccountPayment(models.Model):
    _inherit = "account.payment"

    branch_id = fields.Many2one("sale.order.branch", compute="get_branch_id", store=True, string="الفرع")
    compute_branch = fields.Boolean(compute="get_compute_branch", store=False)

    def get_compute_branch(self):
        for elem in self:
            if not elem.branch_id:
                elem.sudo().get_branch_id()
            elem.compute_branch = False

    def get_branch_id(self):
        for elem in self:
            elem.branch_id = False
            if elem.reconciled_invoice_ids:
                elem.branch_id = elem.reconciled_invoice_ids[0].branch_id
