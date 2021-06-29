#-*- coding: utf-8 -*-
from odoo import models, fields


class MinutasXmartsAsistencia(models.Model):
    _name = 'minutas.xmarts.asistencia'

    minuta_id = fields.Many2one('minutas.xmarts', string='Minuta',ondelete='cascade', index=True,copy=False)
    name = fields.Many2one('res.partner',string='Nombre',ondelete='restrict', domain="[('is_company','=',False)]")
    empresa = fields.Char('Empresa',related='name.parent_id.name', readonly=True)
    puesto = fields.Char('Puesto',related='name.function', readonly=True)
    email = fields.Char('E-mail', related='name.email', readonly=True)
    minuta = fields.Boolean('Envio de minuta', default=True)
