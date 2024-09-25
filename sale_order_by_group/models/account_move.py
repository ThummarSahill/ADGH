from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    branch_id = fields.Many2one("sale.order.branch", compute="get_branch_id", store=True, string="الفرع")
    compute_branch = fields.Boolean(compute="get_compute_branch", store=False)

    def get_compute_branch(self):
        for elem in self:
            if not elem.branch_id:
                elem.sudo().get_branch_id()
            elem.compute_branch = False

    def get_branch_id(self):
        sale_orders = self.env["sale.order"].search([("invoice_ids", "!=", False)])
        so_invo_dict = {}
        for ele in sale_orders:
            if ele.invoice_ids[0].id:
                so_invo_dict.setdefault(ele.invoice_ids[0].id, ele.branch_id.id)

        for elem in self:
            elem.branch_id = False
            try:
                if elem.id in so_invo_dict.keys() and so_invo_dict[elem.id]:
                    elem.branch_id = self.env["sale.order.branch"].search([("id", "=", so_invo_dict[elem.id])])
            except:
                elem.branch_id = False
