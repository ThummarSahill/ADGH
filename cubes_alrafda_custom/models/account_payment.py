from odoo import fields
from odoo import models


class NewModule(models.Model):
    _inherit = "account.payment"

    balance = fields.Monetary(related="partner_id.balance")
