#-*- coding: utf-8 -*-
from odoo import models, fields


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    account_analytic_line_wizard_id = fields.Many2one('account.analytic.line.wizard', string='rel', copy=False)
    minutas_xmarts_id = fields.Many2one('minutas.xmarts', string='rel', copy=False)
