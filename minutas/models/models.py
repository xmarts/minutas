#-*- coding: utf-8 -*-
from openerp import models, fields, api, _, tools, time

class MinutasXmarts(models.Model):
    _name = 'minutas.xmarts'

    @api.one
    @api.depends('reunion', 'referencia')
    def _referencia(self):
        if self.reunion:
            self.referencia = 'calle {}, {}, {}, {}, CP: {}'.format(self.reunion.street,
                                                                    self.reunion.city,
                                                                    self.reunion.state_id.name,
                                                                    self.reunion.country_id.name,
                                                                    self.reunion.zip)

    @api.one
    @api.depends('proxima_reunion', 'referencia2')
    def _referencia2(self):
        if self.proxima_reunion:
            self.referencia2 = 'calle {}, {}, {}, {}, CP: {}'.format(self.proxima_reunion.street,
                                                                    self.proxima_reunion.city,
                                                                    self.proxima_reunion.state_id.name,
                                                                    self.proxima_reunion.country_id.name,
                                                                    self.proxima_reunion.zip)

    def _get_default_name(self):
        cr = self.env.cr
        cr.execute('select "id" from "minutas_xmarts" order by "id" desc limit 1')
        id_returned = cr.fetchone()
        if id_returned == None:
            id_returned = (0,)
        return "MINUTA{}-{}".format(time.strftime("%x"),max(id_returned)+1)

    status = fields.Selection([('borrador', 'Borrador'),('recordatorio', 'Recordatorio de reunión'),('minuta', 'Minuta enviada')],default='borrador')
    objetivo = fields.Char('Objetivo', required=True)
    fecha_hora = fields.Datetime('Fecha y Hora', required=True)
    proyecto = fields.Many2one('project.project',string='Proyecto',required = True)
    name = fields.Char(string='Minuta', default=_get_default_name)
    duracion = fields.Float('Duración', required=True)
    hito = fields.Many2many(comodel_name='minutas.xmarts.hitos',string='Hito')
    fecha_proxima_reunion = fields.Datetime('Fecha de proxima reunión')
    fin_proxima_reunion = fields.Datetime('Fin proxima reunión')
    asistencia_lines = fields.One2many('minutas.xmarts.asistencia', 'minuta_id', string='Tabla Asistencia')
    actividades_lines = fields.One2many('minutas.xmarts.actividades', 'minuta_id', string='Tabla Actividades')
    compromisos_lines = fields.One2many('minutas.xmarts.compromisos', 'minuta_id', string='Tabla Compromisos')
    referencia = fields.Char(string='', compute='_referencia')
    referencia2 = fields.Char(string='', compute='_referencia2')
    reunion = fields.Many2one('res.partner', string='Lugar de reunión', required=True)
    proxima_reunion = fields.Many2one('res.partner', string='Lugar de proxima reunión')


    @api.one
    @api.depends('emails')
    def _correos(self):
        cont = 0
        corr = ''
        for line in self.asistencia_lines:
            if line.minuta == True:
                if cont > 0:
                    corr = corr + ','
                corr = corr + line.name.email
                cont = cont + 1
        self.emails = corr

    emails = fields.Char(string='Correos', compute="_correos")



    @api.onchange('reunion')
    def onchange_reun(self):
        if self.reunion:
            self.referencia = 'calle {}, {}, {}, {}, CP: {}'.format(self.reunion.street,
                                                                    self.reunion.city,
                                                                    self.reunion.state_id.name,
                                                                    self.reunion.country_id.name,
                                                                    self.reunion.zip)

    @api.onchange('proxima_reunion')
    def onchange_preun(self):
        if self.proxima_reunion:
            self.referencia2 = 'calle {}, {}, {}, {}, CP: {}'.format(self.proxima_reunion.street,
                                                                    self.proxima_reunion.city,
                                                                    self.proxima_reunion.state_id.name,
                                                                    self.proxima_reunion.country_id.name,
                                                                    self.proxima_reunion.zip)

    #@api.onchange('proyecto')
    #def onchange_categ(self):
    #    selected_categ = []
    #    res = {}
    #    if self.proyecto:
    #        selected_categ.append(self.proyecto.partner_id.id)
    #        for line in self.proyecto.partner_id.child_ids:
    #            selected_categ.append(line.id)
    #    res.update({
    #        'domain': {
    #            'reunion': [('id', '=', list(set(selected_categ)))],
    #            'proxima_reunion': [('id', '=', list(set(selected_categ)))],
    #        }
    #    })
    #    return res

    def action_orden_sent(self):
        """ Open a window to compose an email, with the edi invoice template
            message loaded by default
        """
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
        """ Open a window to compose an email, with the edi invoice template
            message loaded by default
        """
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







class MinutasXmartsAsistencia(models.Model):
    _name = 'minutas.xmarts.asistencia'

    @api.onchange('name')
    def onchange_name(self):
        if self.name:
            self.puesto = self.name.function
            self.empresa = self.name.company_id.name


    @api.one
    @api.depends('name','empresa')
    def _empresa(self):
        self.empresa = self.name.company_id.name

    @api.one
    @api.depends('name', 'puesto')
    def _puesto(self):
        self.puesto = self.name.function


    minuta_id = fields.Many2one('minutas.xmarts', string='Minuta',ondelete='cascade', index=True,copy=False)
    name = fields.Many2one('res.partner',string='Nombre',ondelete='restrict', domain="[('is_company','=',False)]")
    empresa = fields.Char('Empresa',compute='_empresa')
    puesto = fields.Char('Puesto',compute='_puesto')
    minuta = fields.Boolean('Envio de minuta')

class MinutasXmartsActividades(models.Model):
    _name = 'minutas.xmarts.actividades'
    minuta_id = fields.Many2one('minutas.xmarts', string='Minuta', ondelete='cascade', index=True, copy=False)
    name = fields.Char(string='Actividad',ondelete='restrict')
    status = fields.Many2one('minutas.xmarts.estatus', string='Estatus de actividades')

class MinutasXmartsCompromisos(models.Model):
    _name = 'minutas.xmarts.compromisos'

    @api.onchange('name')
    def onchange_name(self):
        if self.name:
            self.asignado = self.name.user_id.name
            self.limite = self.name.date_deadline
            self.etapa = self.name.stage_id.name

    @api.one
    @api.depends('name', 'asignado')
    def _asignado(self):
        self.asignado = self.name.user_id.name

    @api.one
    @api.depends('name', 'limite')
    def _limite(self):
        self.limite = self.name.date_deadline

    @api.one
    @api.depends('name', 'etapa')
    def _etapa(self):
        self.etapa = self.name.stage_id.name


    minuta_id = fields.Many2one('minutas.xmarts', string='Minuta', ondelete='cascade', index=True, copy=False)
    name = fields.Many2one('project.task',string='Tarea',ondelete='restrict')
    asignado = fields.Char(string='Asignado a', compute='_asignado')
    limite = fields.Date(string='Fecha limite', compute='_limite')
    etapa = fields.Char(string='Etapa', compute='_etapa')

class MinutasXmartsHitos(models.Model):
    _name = 'minutas.xmarts.hitos'
    name = fields.Char('Hito')

class MinutasXmartsEstatus(models.Model):
    _name = 'minutas.xmarts.estatus'
    name = fields.Char('Estatus de actividad')
