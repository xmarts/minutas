#-*- coding: utf-8 -*-
from odoo import models, fields, api


class WzAccountAnalyticLine(models.Model):
    _name = 'account.analytic.line.wizard'

    account_analytic_line_ids = fields.One2many(
        'account.analytic.line', 
        'account_analytic_line_wizard_id'
    )
    task_id = fields.Many2one(
        'project.task',
        string="Tarea", 
        readonly=True
    )
    project_id = fields.Many2one(
        'project.project', 
        string="Projecto", 
        readonly=True
    )

    def save_wizard(self):
        print('guardar')
