#-*- coding: utf-8 -*-
from odoo import models, fields


class MinutasXmartsHitos(models.Model):
    _name = 'minutas.xmarts.hitos'

    name = fields.Char(string="Hito")
