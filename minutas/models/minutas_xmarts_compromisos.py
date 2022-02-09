#-*- coding: utf-8 -*-
from odoo import api, models, fields


class MinutasXmartsCompromisos(models.Model):
    _name = 'minutas.xmarts.compromisos'

    minuta_id = fields.Many2one(
        'minutas.xmarts', 
        string="Minuta", 
        ondelete="cascade", 
        index=True, 
        copy=False
    )
    name = fields.Many2one(
        'project.task', 
        string="Tarea", 
        ondelete="restrict"
    )
    asignado = fields.Char(
        string="Asignado a", 
    #   related='name.user_ids.name', 
        compute="_compute_get_asignado"
    )
    limite = fields.Date(
        string="Fecha límite", 
        related='name.date_deadline', 
        readonly=True
    )
    etapa = fields.Char(
        string="Etapa", 
        related='name.stage_id.name', 
        readonly=True
    )
    observaciones =  fields.Text(string="Descripción")

    @api.depends('name.user_ids')
    def _compute_get_asignado(self):
        for record in self:
            record.asignado = ""
            if record.name.user_ids:
                record.asignado = ",".join(record.name.user_ids.mapped('name'))
