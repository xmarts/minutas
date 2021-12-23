#-*- coding: utf-8 -*-
from odoo import models, fields


class UbicacionesVirtuales(models.Model):
    _name='ubicaciones.virtuales'

    name = fields.Char(
        string="Ubicación virtual", 
        required=True
    )
