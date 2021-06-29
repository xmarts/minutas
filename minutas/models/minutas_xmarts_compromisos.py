#-*- coding: utf-8 -*-
from odoo import models, fields


class MinutasXmartsCompromisos(models.Model):
    _name = 'minutas.xmarts.compromisos'

    minuta_id = fields.Many2one('minutas.xmarts', string='Minuta', ondelete='cascade', index=True, copy=False)
    name = fields.Many2one('project.task',string='Tarea',ondelete='restrict')
    asignado = fields.Char(string='Asignado a', related='name.user_id.name', readonly=True)
    limite = fields.Date(string='Fecha limite', related='name.date_deadline', readonly=True)
    etapa = fields.Char(string='Etapa', related='name.stage_id.name', readonly=True)
    observaciones =  fields.Text(string='Descripcion')
