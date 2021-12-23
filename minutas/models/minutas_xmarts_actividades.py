#-*- coding: utf-8 -*-
from odoo import models, fields


class MinutasXmartsActividades(models.Model):
    _name = 'minutas.xmarts.actividades'

    minuta_id = fields.Many2one(
        'minutas.xmarts', 
        string="Minuta", 
        ondelete="cascade", 
        index=True, 
        copy=False
    )
    name = fields.Char(
        string="Actividad", 
        ondelete="restrict"
    )
    status = fields.Many2one(
        'minutas.xmarts.estatus', 
        string="Estatus de actividades"
    )