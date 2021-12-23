#-*- coding: utf-8 -*-
from odoo import models, fields


class MinutasXmartsAsistenciaInterna(models.Model):
    _name = 'minutas.xmarts.asistenciain'

    minuta_id = fields.Many2one(
        'minutas.xmarts', 
        string="Minuta", 
        ondelete="cascade", 
        index=True, 
        copy=False
    )
    name = fields.Many2one(
        'hr.employee', 
        string="Nombre", 
        ondelete="restrict"
    )
    puesto = fields.Char(
        string="Puesto", 
        related='name.job_id.name', 
        readonly=True
    )
    email = fields.Char(
        string="E-mail", 
        related='name.work_email', 
        readonly=True
    )
    minuta = fields.Boolean(
        string="Envío de minuta", 
        default=True
    )
