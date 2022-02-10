#-*- coding: utf-8 -*-
from odoo import models, fields, api


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    account_analytic_line_wizard_id = fields.Many2one(
        'account.analytic.line.wizard', 
        string="rel", 
        copy=False
    )
    update_id = fields.Many2one(
        'project.update', 
        string="Actualización"
    )

    @api.model_create_multi
    def create(self, vals_list):
        lines = super(AccountAnalyticLine, self).create(vals_list)
        for line in lines:
            model_wizard = self.env['account.analytic.line.wizard'].search(
                [
                    ('task_id', '=', line.task_id.id), 
                    ('project_id', '=', line.task_id.project_id.id)
                ], 
                limit=1
            )
            if len(model_wizard) > 0:
                id_wizard = int(model_wizard.id)
                model = self.search(
                    [
                        ('task_id', '=', model_wizard.task_id.id), 
                        ('project_id', '=', model_wizard.task_id.project_id.id), 
                        ('account_analytic_line_wizard_id', '=', False)
                    ]
                )
                for task in model:
                    task.update({'account_analytic_line_wizard_id': id_wizard})
        return lines
