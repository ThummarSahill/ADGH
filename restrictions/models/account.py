from odoo import api, fields, models


class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"

    # def get_domain(self):
    #     sales_user = self.env.user.has_group('sales_team.group_sale_salesman')
    #     domain = [('company_id', '=', self.env.user.company_id.id), ('type', 'in', ('bank', 'cash'))]
    #     if sales_user and self.env.user.has_group('account.group_account_invoice'):
    #         domain = [('id', 'in', self.env.user.journal_id.ids)]
    #     print('----------------=',not self.env.user.has_group('account.group_account_invoice'))
    #     return domain
    journal_id = fields.Many2one("account.journal", store=True, readonly=False, compute="_compute_journal_id")  # , domain=get_domain

    @api.depends("can_edit_wizard", "company_id")
    def _compute_journal_id(self):
        for wizard in self:
            if wizard.can_edit_wizard:
                batch = wizard._get_batches()[0]
                wizard.journal_id = wizard._get_batch_journal(batch)
            else:
                wizard.journal_id = self.env["account.journal"].search(
                    [
                        ("type", "in", ("bank", "cash")),
                        ("company_id", "=", wizard.company_id.id),
                    ],
                    limit=1,
                )
