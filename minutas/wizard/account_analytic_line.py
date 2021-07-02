from odoo import models, fields


class AccountAnalyticLineWizard(models.Model):
    _name = 'account.analytic.line.wizard'

    # account_analytic_line_ids = fields.One2many('account.analytic.line', 'wizard_id', 'Parte de horas')
    minuta = fields.Boolean('Envio de minuta', default=True)
