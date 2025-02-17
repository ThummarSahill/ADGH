# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, fields, models
from odoo.osv import expression


class ShResUsers(models.Model):
    _inherit = "res.users"

    @api.model
    def default_get(self, fields_list):
        rec = super(ShResUsers, self).default_get(fields_list)

        journals = self.env.company.journal_ids.ids
        rec.update({"journal_ids": [(6, 0, journals)]})
        return rec

    journal_ids = fields.Many2many("account.journal", string="Journals", copy=False)


class ShAccountJournalRestrict(models.Model):
    _inherit = "account.journal"

    @api.model
    def default_get(self, fields_list):
        rec = super(ShAccountJournalRestrict, self).default_get(fields_list)

        users = self.env.company.sh_user_ids.ids
        rec.update({"user_ids": [(6, 0, users)]})
        return rec

    user_ids = fields.Many2many("res.users", string="Users", copy=False)

    # To apply domain to action_________ 2
    @api.model
    def _name_search(self, name, domain=None, operator='ilike', limit=None, order=None):
        super(ShAccountJournalRestrict, self)._name_search(name, domain, operator, limit, order)

        if self.env.user.has_group("sh_journal_restrict.group_journal_restrict_feature") and not (self.env.user.has_group("base.group_erp_manager")):
            domain = [("user_ids", "in", self.env.user.id), ("name", "ilike", name)]
        else:
            domain = [("name", "ilike", name)]
        return self._search(expression.AND([domain]), limit=limit)

    # To apply domain to load menu_________ 1
    @api.model
    def search(self, args, offset=0, limit=None, order=None):
        _ = self._context or {}
        if self.env.user.has_group("sh_journal_restrict.group_journal_restrict_feature") and not (self.env.user.has_group("base.group_erp_manager")):
            args += [
                ("user_ids", "in", self.env.user.id),
            ]
        return super(ShAccountJournalRestrict, self).search(args, offset=offset, limit=limit, order=order)
