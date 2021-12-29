#-*- coding: utf-8 -*-
from odoo import api, exceptions, fields, models, _


class MinutasXmartsActivids(models.Model):
    _name = 'minutas.xmarts.activids'

    minuta_id = fields.Many2one(
        'minutas.xmarts', 
        string="Minuta", 
        ondelete="cascade", 
        index=True, 
        copy=False
    )
    name = fields.Many2one(
        'project.task', 
        string="Tarea", 
        ondelete="restrict"
    )
    asignado = fields.Char(
        string="Asignado a", 
    #   related='name.user_ids.name', 
        compute="_compute_get_asignado"
    )
    limite = fields.Date(
        string="Fecha límite", 
        related='name.date_deadline', 
        readonly=True
    )
    etapa = fields.Char(
        string="Etapa", 
        related='name.stage_id.name', 
        readonly=True
    )
    observaciones = fields.Text(string="Descripción")

    @api.depends('name.user_ids')
    def _compute_get_asignado(self):
        for record in self:
            record.asignado = ""
            if record.name.user_ids:
                record.asignado = ",".join(record.name.user_ids.mapped('name'))

    def action_set_horas(self):
        if self.name:
            action = self.env['ir.actions.act_window']._for_xml_id('minutas.account_analytic_line_wizard_act_window')
            model_wizard = self.env['account.analytic.line.wizard'].search(
                [
                    ('task_id', '=', self.name.id), 
                    ('project_id', '=', self.name.project_id.id)
                ], 
                limit=1
            )
            if len(model_wizard) == 0:
                model_wizard = self.env['account.analytic.line.wizard'].create(
                    {'task_id': self.name.id, 'project_id': self.name.project_id.id}
                )
            model_hour = self.env['account.analytic.line'].search(
                [
                    ('task_id', '=', self.name.id), 
                    ('project_id', '=', self.name.project_id.id), 
                    ('account_analytic_line_wizard_id', '=', False)
                ]
            )
            for hour in model_hour:
                hour.update({'account_analytic_line_wizard_id': model_wizard.id})
            action['res_id'] = model_wizard.id
            return action
        else:
            raise exceptions.ValidationError(_("Es necesario tener una tarea seleccionada para poder registrar horas"))
