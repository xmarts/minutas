from odoo import models, fields


class WzAccountAnalyticLine(models.Model):

    _name = 'account.analytic.line.wizard'

    account_analytic_line_ids = fields.One2many('account.analytic.line', 'account_analytic_line_wizard_id')

    def save_wizard(self):
        print('evento wizard')
