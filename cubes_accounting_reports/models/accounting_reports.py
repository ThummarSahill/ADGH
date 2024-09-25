# -*- coding: utf-8 -*-
# -**-----------------**
import re

from num2words import num2words

from odoo import api, fields, models


class AccountPayment(models.Model):
    _inherit = "account.payment"
    cash_amount_in_words = fields.Char(
        string="Amount in Words",
        store=True,
        compute="_compute_cash_amount_in_words",
    )
    cheque_number = fields.Char(string="Cheque Number", required=False)
    halla_amount = fields.Integer(string="Halla", compute="amount_word_riyal_halla", required=False)
    riyal_amount = fields.Integer(string="Halla", compute="amount_word_riyal_halla", required=False)
    bank_or_cash = fields.Selection(
        string="Payment Method",
        selection=[
            ("cash", "Cash"),
            ("bank", "Bank"),
            ("cheque", "Cheque"),
        ],
        required=False,
    )
    bank_or_cash_arabic = fields.Selection(
        string="Payment Method",
        selection=[
            ("cash", "كاش"),
            ("bank", "بنــك"),
            ("cheque", "شيــك"),
        ],
        required=False,
        compute="get_selection_in_arabic",
    )
    is_out = fields.Boolean(string="Out Flag", required=False, compute="get_report_name_print", readonly=True)
    is_in = fields.Boolean(string="In Flag", required=False, compute="get_report_name_print", readonly=True)
    is_cheque = fields.Boolean(string="Cheque Flag", required=False, compute="get_report_name_print", readonly=True)
    partner_without_no = fields.Char(string="Partner", compute="get_first_name_index", required=False)

    @api.depends("payment_method_line_id", "currency_id", "amount")
    def _compute_cash_amount_in_words(self):
        for pay in self:
            if pay.currency_id:
                pay.cash_amount_in_words = pay.currency_id.amount_to_text(pay.amount)
            else:
                pay.cash_amount_in_words = False

    @api.depends("bank_or_cash")
    def get_selection_in_arabic(self):
        for arabic in self:
            if arabic.bank_or_cash == "cash":
                arabic.bank_or_cash_arabic = "cash"
            if arabic.bank_or_cash == "bank":
                arabic.bank_or_cash_arabic = "bank"
            if arabic.bank_or_cash == "cheque":
                arabic.bank_or_cash_arabic = "cheque"
            else:
                arabic.bank_or_cash_arabic = "cash"

    @api.depends("payment_type", "bank_or_cash")
    def get_report_name_print(self):
        for selection in self:
            selection.is_out = False
            selection.is_in = False
            selection.is_cheque = False
            if selection.payment_type == "outbound":
                selection.write({"is_out": True})
                selection.write({"is_in": False})
            if selection.payment_type == "inbound":
                selection.write({"is_in": True})
                selection.write({"is_out": False})
            if selection.payment_type == "outbound" and selection.bank_or_cash == "cheque":
                selection.write({"is_out": False})
                selection.is_cheque = True
            if selection.payment_type == "inbound" and selection.bank_or_cash == "cheque":
                selection.write({"is_in": False})
                selection.is_cheque = True

    def amount_word(self, amount):
        language = self.partner_id.lang or "en"
        language_id = self.env["res.lang"].search([("code", "=", "ar_001")])
        if language_id:
            language = language_id.iso_code
        amount_str = str("{:2f}".format(amount))
        amount_str_splt = amount_str.split(".")
        before_point_value = amount_str_splt[0]
        after_point_value = amount_str_splt[1][:2]
        before_amount_words = num2words(int(before_point_value), lang=language)
        after_amount_words = num2words(int(after_point_value), lang=language)
        self.halla_amount = int(after_point_value)
        self.riyal_amount = int(before_point_value)
        if num2words(int(after_point_value), lang=language) == "صفر":
            amount = before_amount_words + " "
            return amount
        else:
            amount = before_amount_words + " " + "و " + " " + after_amount_words
            return amount

    @api.depends("amount")
    def amount_word_riyal_halla(self):
        language = self.partner_id.lang or "en"
        language_id = self.env["res.lang"].search([("code", "=", "ar_001")])
        if language_id:
            language = language_id.iso_code
        amount_str = str("{:2f}".format(self.amount))
        amount_str_splt = amount_str.split(".")
        before_point_value = amount_str_splt[0]
        after_point_value = amount_str_splt[1][:2]
        self.halla_amount = int(after_point_value)
        self.riyal_amount = int(before_point_value)

    @api.depends("partner_id")
    def get_first_name_index(self):
        for name in self:
            partner = name.partner_id.name
            pattern_order = r"[0-9]"
            char_str = re.sub(pattern_order, "", partner)
            name.partner_without_no = char_str
