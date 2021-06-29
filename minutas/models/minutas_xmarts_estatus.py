#-*- coding: utf-8 -*-
from odoo import models, fields


class MinutasXmartsEstatus(models.Model):
    _name = 'minutas.xmarts.estatus'

    name = fields.Char('Estatus de actividad')
