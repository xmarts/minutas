#-*- coding: utf-8 -*-
from odoo import api, models, fields, _
from .project_update import STATUS_COLOR

class hrProjectMinutas(models.Model):
    _inherit = 'project.project'

    last_update_status = fields.Selection(
        selection=[
            ('on_track', 'On Track'),
            ('at_risk', 'At Risk'),
            ('off_track', 'Off Track'),
            ('on_hold', 'On Hold'),
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

    @api.depends('last_update_id.status')
    def _compute_last_update_status(self):
        for project in self:
            project.last_update_status = project.last_update_id.status or 'on_track'

    @api.depends('last_update_status')
    def _compute_last_update_color(self):
        for project in self:
            project.last_update_color = STATUS_COLOR[project.last_update_status]

    def count_minutas_project(self):
        cr = self.env.cr
        sql = "select coalesce(count(distinct mx.id),0) from minutas_xmarts mx inner join minutas_xmarts_asistenciain mxa on mx.id=mxa.minuta_id where mx.proyecto='"+str(self.id)+"';"
        cr.execute(sql)
        minutas = cr.fetchone()
        self.project_minutas_count=minutas[0]

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
            'view_mode': 'tree,form',
            'name': _('Minutas del proyecto'),
            'res_model': 'minutas.xmarts',
            'domain': [('id', 'in', lista)],
        }
        return action
