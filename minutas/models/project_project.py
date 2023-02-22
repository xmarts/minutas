#-*- coding: utf-8 -*-
from odoo import api, models, fields, _
from .project_update import STATUS_COLOR
import json
class hrProjectMinutas(models.Model):
    _inherit = 'project.project'

    last_update_status = fields.Selection(
        selection=[
            ('on_track', 'On Track'),
            ('at_risk', 'At Risk'),
            ('off_track', 'Off Track'),
            ('on_hold', 'On Hold'),
            ('to_define', 'Set Status'),
            ('minute', 'Minuta')
        ], 
        default='on_track', 
        compute='_compute_last_update_status', 
        store=True
    )
    last_update_color = fields.Integer(compute='_compute_last_update_color')
    project_minutas_count = fields.Integer(
        string="", 
        default=0, 
        compute="count_minutas_project"
    )

    def action_minutas_tasks(self):
        minutas = self.env['minutas.xmarts'].search([
            ('proyecto', '=', self.id)
        ])
        action = {
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form,kanban,pivot,calendar',
            'name': _('Minutas del proyecto'),
            'res_model': 'minutas.xmarts',
            'domain': [('id', 'in', minutas.ids)],
            'context': {'default_proyecto': self.id}
        }
        return action
    def minutas_get_action(self):
        action = self.env["ir.actions.actions"]._for_xml_id("minutas.action_minutas_xmarts")
        action.update({
            'display_name': _('Tickets'),
            'context': {'active_id': self.id},
        })
        return action

    def _get_stat_buttons(self):
        buttons = super(hrProjectMinutas, self)._get_stat_buttons()
        buttons.append({
                'icon': 'clock-o',
                'text': 'Minutas',
                'number': self.project_minutas_count,
                'action_type': 'object',
                'action': 'action_minutas_tasks',
                'show': True,
                'sequence': 99,
            })
        return buttons
    @api.depends('last_update_id.status')
    def _compute_last_update_status(self):
        for project in self:
            project.last_update_status = project.last_update_id.status or 'on_track'

    def count_minutas_project(self):
        minutas = self.env['minutas.xmarts'].search([
            ('proyecto', '=', self.id)
        ])
        self.project_minutas_count = len(minutas)
        print(self.project_minutas_count)

    def mis_minutas_search(self):
        cr = self.env.cr
        sql = "select * from minutas_xmarts mx inner join minutas_xmarts_asistenciain mxa on mxa.minuta_id=mx.id where mxa.name='"+str(self.env.uid)+"';"
        cr.execute(sql)
        minutas = cr.fetchall()
        lista=[]
        for l in minutas:
            lista.append(l[0])
        action = {
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form,kanban,pivot,calendar',
            'name': _('Minutas del proyecto'),
            'res_model': 'minutas.xmarts',
            'domain': [('id', 'in', lista)],
            'context': {'default_proyecto': self.id}
        }
        return action
