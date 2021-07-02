#-*- coding: utf-8 -*-
from odoo import models, fields


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    wizard_id = fields.Many2one('account.analytic.line.wizard', string='rel', ondelete='cascade', index=True, copy=False)
