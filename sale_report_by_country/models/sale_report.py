# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class SaleReportEdited(models.Model):
    _inherit = "sale.report"

    product_country_id = fields.Many2one("res.country", string="بلد المنشاء", readonly=True)
    brand_id = fields.Many2one("product.brand", string="الشركة المصنعة", readonly=True)

    def _select_sale(self):
        res = super(SaleReportEdited, self)._select_sale()
        res += "t.country_id as product_country_id,"
        res += "t.brand_id as brand_id,"
        return res

    def _group_by_sale(self):
        res = super(SaleReportEdited, self)._group_by_sale()
        res += "t.country_id,"
        res += "t.brand_id,"
        return res
