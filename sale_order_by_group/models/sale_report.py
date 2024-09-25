# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class SaleReportEdited(models.Model):
    _inherit = "sale.report"

    branch_id = fields.Many2one("sale.order.branch", string="الفرع", readonly=True)

    def _select_sale(self):
        res = super(SaleReportEdited, self)._select_sale()
        res += ", s.branch_id as branch_id"
        return res

    def _group_by_sale(self):
        res = super(SaleReportEdited, self)._group_by_sale()
        res += ", s.branch_id"
        return res
