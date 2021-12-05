#-*- coding: utf-8 -*-
from odoo import models, fields, api, _, time 


class MinutasXmarts(models.Model):
    _name = 'minutas.xmarts'
    _inherit = ['mail.thread']

    def _get_default_name(self):
        cr = self.env.cr
        cr.execute('select "id" from "minutas_xmarts" order by "id" desc limit 1')
        id_returned = cr.fetchone()
        if id_returned == None:
            id_returned = (0,)
        return "MINUTA{}-{}".format(time.strftime("%x"),max(id_returned) + 1)

    status = fields.Selection(
        [
            ('borrador', 'Borrador'), 
            ('recordatorio', 'Recordatorio de reunión'), 
            ('minuta', 'Minuta enviada')
        ], 
        default='borrador'
    )
    objetivo = fields.Char(
        string="Objetivo", 
        required=True
    )
    fecha_hora = fields.Datetime(
        string="Fecha y Hora", 
        required=True
    )
    proyecto = fields.Many2one(
        'project.project', 
        string="Proyecto", 
        required=True
    )
    name = fields.Char(
        string="Minuta", 
        default=_get_default_name
    )
    duracion = fields.Float(
        string="Duración (HH:MM)", 
        required=True, 
        default=1
    )
    hito = fields.Many2many(
        comodel_name='minutas.xmarts.hitos', 
        string="Hito"
    )
    fecha_proxima_reunion = fields.Datetime(string="Fecha de próxima reunión")
    fin_proxima_reunion = fields.Datetime(string="Fin próxima reunión")
    asistencia_lines = fields.One2many(
        'minutas.xmarts.asistencia', 
        'minuta_id', 
        string="Tabla Asistencia Externa"
    )
    asistenciain_lines = fields.One2many(
        'minutas.xmarts.asistenciain', 
        'minuta_id', 
        string="Tabla Asistencia Interna"
    )
    actividades_lines = fields.One2many(
        'minutas.xmarts.actividades', 
        'minuta_id', 
        string="Tabla Actividades Extra"
    )
    activids_lines = fields.One2many(
        'minutas.xmarts.activids', 
        'minuta_id', 
        string="Tabla Actividades"
    )
    compromisos_lines = fields.One2many(
        'minutas.xmarts.compromisos', 
        'minuta_id', 
        string="Tabla Compromisos"
    )
    referencia = fields.Char(
        string="", 
        compute="_referencia"
    )
    referencia2 = fields.Char(
        string="", 
        compute="_referencia2"
    )
    reunion = fields.Many2one(
        'res.partner', 
        string="Lugar de reunión"
    )
    proxima_reunion = fields.Many2one(
        'res.partner', 
        string="Lugar de próxima reunión"
    )
    client=fields.Binary(string="Cliente")
    consul=fields.Binary(string="Consultor")
    company_id = fields.Many2one(
        'res.company', 
        default=lambda self: self.env.user.company_id
    )
    emails = fields.Char(
        string="Correos", 
        compute="_correos"
    )
    virtual = fields.Boolean(string="Es virtual")
    liga_de_reunion = fields.Char(string="Link de la reunión")
    ubicaciones_virtuales = fields.Many2one('ubicaciones.virtuales')
    link_reunion = fields.Text(string="Link de la reunión")

    @api.depends('reunion', 'referencia')
    def _referencia(self):
        for rec in self:
            if rec.reunion:
                calle = 'calle {}, {}, {}, {}, CP: {}'.format(
                    rec.reunion.street,
                    rec.reunion.city,
                    rec.reunion.state_id.name,
                    rec.reunion.country_id.name,
                    rec.reunion.zip
                )
                rec.referencia = calle
            else: 
                rec.referencia = ""

    @api.depends('proxima_reunion', 'referencia2')
    def _referencia2(self):
        for rec in self:
            if rec.proxima_reunion:
                calle2 = 'calle {}, {}, {}, {}, CP: {}'.format(
                    rec.proxima_reunion.street,
                    rec.proxima_reunion.city,
                    rec.proxima_reunion.state_id.name,
                    rec.proxima_reunion.country_id.name,
                    rec.proxima_reunion.zip
                )
                rec.referencia2 = calle2
            else: 
                rec.referencia2 = ""

    @api.depends('emails')
    def _correos(self):
        cont = 0
        corr = ''
        for line in self.asistencia_lines:
            if line.minuta == True:
                if cont > 0:
                    corr = corr + ','

                if(line.email):
                    corr = corr + line.email
                    
                cont = cont + 1
        for line in self.asistenciain_lines:
            if line.minuta == True:
                if cont > 0:
                    corr = corr + ','

                if(line.email):
                    corr = corr + line.email
                    
                cont = cont + 1
        self.emails = corr

    @api.onchange('reunion')
    def onchange_reun(self):
        if self.reunion:
            self.referencia = 'calle {}, {}, {}, {}, CP: {}'.format(
                self.reunion.street,
                self.reunion.city,
                self.reunion.state_id.name,
                self.reunion.country_id.name,
                self.reunion.zip
            )

    @api.onchange('proxima_reunion')
    def onchange_preun(self):
        if self.proxima_reunion:
            self.referencia2 = 'calle {}, {}, {}, {}, CP: {}'.format(
                self.proxima_reunion.street,
                self.proxima_reunion.city,
                self.proxima_reunion.state_id.name,
                self.proxima_reunion.country_id.name,
                self.proxima_reunion.zip
            )

    def action_orden_sent(self):
        self.ensure_one()
        template = self.env.ref('minutas.minuta_email_orden', False)
        compose_form = self.env.ref('mail.email_compose_message_wizard_form', False)
        ctx = dict(
            default_model='minutas.xmarts',
            default_res_id=self.id,
            default_use_template=bool(template),
            default_template_id=template and template.id or False,
            force_email=True
        )
        if self.status == 'borrador':
            self.status = 'recordatorio'
        body = "Orden del día envíada" + "\n" + "Proyecto: " + str(self.proyecto.name)
        self.message_post(body=body, message_type='comment', subtype_xmlid='mail.mt_comment')
        return {
            'name': _('Orden Email'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form.id, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }

    def action_minuta_sent(self):
        self.ensure_one()
        template = self.env.ref('minutas.minuta_email_minuta', False)
        compose_form = self.env.ref('mail.email_compose_message_wizard_form', False)
        ctx = dict(
            default_model='minutas.xmarts',
            default_res_id=self.id,
            default_use_template=bool(template),
            default_template_id=template and template.id or False,
            default_composition_mode='comment',
            force_email=True
        )
        self.status = 'minuta'
        body = "Minuta envíada" + "\n" + "Proyecto: " + str(self.proyecto.name)
        self.message_post(body=body, message_type='comment', subtype_xmlid='mail.mt_comment')
        return {
            'name': _('Minuta Email'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form.id, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }
