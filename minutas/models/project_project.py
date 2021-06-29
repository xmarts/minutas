#-*- coding: utf-8 -*-
from odoo import models, fields, _


class hrProjectMinutas(models.Model):
    _name='project.project'
    _inherit='project.project'

    project_minutas_count = fields.Integer(string="", default=0, compute='count_minutas_project')

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
