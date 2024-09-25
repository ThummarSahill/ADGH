from odoo import fields, models


class Branches(models.Model):
    _name = "sale.order.branch"

    name = fields.Char(string="الفرع")

    location = fields.Char("العنوان")
    phone = fields.Char("الهاتف")
