# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models


class ShResUsers(models.Model):
    _inherit = "res.users"

    branch_id = fields.Many2many("sale.order.branch", string="فرع المبيعات")
