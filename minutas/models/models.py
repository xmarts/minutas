#-*- coding: utf-8 -*-
from odoo import models, fields, api, _, tools, time 

class MinutasXmarts(models.Model):
    _name = 'minutas.xmarts'
    _inherit = ['mail.thread']

    @api.depends('reunion', 'referencia')
    def _referencia(self):
        for rec in self:
            if rec.reunion:
                calle = 'calle {}, {}, {}, {}, CP: {}'.format(rec.reunion.street,
                                                                        rec.reunion.city,
                                                                        rec.reunion.state_id.name,
                                                                        rec.reunion.country_id.name,
                                                                        rec.reunion.zip)
                rec.referencia = calle
            else: 
                rec.referencia = ""

    @api.depends('proxima_reunion', 'referencia2')
    def _referencia2(self):
        for rec in self:
            if rec.proxima_reunion:
                calle2 = 'calle {}, {}, {}, {}, CP: {}'.format(rec.proxima_reunion.street,
                                                                        rec.proxima_reunion.city,
                                                                        rec.proxima_reunion.state_id.name,
                                                                        rec.proxima_reunion.country_id.name,
                                                                        rec.proxima_reunion.zip)
                rec.referencia2 = calle2
            else: 
                rec.referencia2 = ""


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
    duracion = fields.Float('Duración (HH:MM)', required=True, default=1)
    hito = fields.Many2many(comodel_name='minutas.xmarts.hitos',string='Hito')
    fecha_proxima_reunion = fields.Datetime('Fecha de proxima reunión')
    fin_proxima_reunion = fields.Datetime('Fin proxima reunión')
    asistencia_lines = fields.One2many('minutas.xmarts.asistencia', 'minuta_id', string='Tabla Asistencia Externa')
    asistenciain_lines = fields.One2many('minutas.xmarts.asistenciain', 'minuta_id', string='Tabla Asistencia Interna')
    actividades_lines = fields.One2many('minutas.xmarts.actividades', 'minuta_id', string='Tabla Actividades Extra')
    activids_lines = fields.One2many('minutas.xmarts.activids', 'minuta_id', string='Tabla Actividades')
    compromisos_lines = fields.One2many('minutas.xmarts.compromisos', 'minuta_id', string='Tabla Compromisos')
    referencia = fields.Char(string='', compute='_referencia')
    referencia2 = fields.Char(string='', compute='_referencia2')
    reunion = fields.Many2one('res.partner', string='Lugar de reunión', required=True)
    proxima_reunion = fields.Many2one('res.partner', string='Lugar de proxima reunión')
    client=fields.Binary(string='Cliente')
    consul=fields.Binary(string='Consultor')
    company_id = fields.Many2one("res.company", default=lambda self: self.env.user.company_id)

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
        body = "Orden del dia enviada"+"\n"+"Proyecto: "+str(self.proyecto.name)
        self.message_post(body=body, subtype='mt_comment', context="")
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
        body = "Minuta enviada"+"\n"+"Proyecto: "+str(self.proyecto.name)
        self.message_post(body=body, subtype='mt_comment', context="")
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

    minuta_id = fields.Many2one('minutas.xmarts', string='Minuta',ondelete='cascade', index=True,copy=False)
    name = fields.Many2one('res.partner',string='Nombre',ondelete='restrict', domain="[('is_company','=',False)]")
    empresa = fields.Char('Empresa',related='name.parent_id.name', readonly=True)
    puesto = fields.Char('Puesto',related='name.function', readonly=True)
    email = fields.Char('E-mail', related='name.email', readonly=True)
    minuta = fields.Boolean('Envio de minuta', default=True)

class MinutasXmartsAsistenciaInterna(models.Model):
    _name = 'minutas.xmarts.asistenciain'

    minuta_id = fields.Many2one('minutas.xmarts', string='Minuta',ondelete='cascade', index=True,copy=False)
    name = fields.Many2one('hr.employee',string='Nombre',ondelete='restrict')
    puesto = fields.Char('Puesto',related='name.job_id.name', readonly=True)
    email = fields.Char('E-mail', related='name.work_email', readonly=True)
    minuta = fields.Boolean('Envio de minuta', default=True)

class MinutasXmartsActividades(models.Model):
    _name = 'minutas.xmarts.actividades'
    minuta_id = fields.Many2one('minutas.xmarts', string='Minuta', ondelete='cascade', index=True, copy=False)
    name = fields.Char(string='Actividad',ondelete='restrict')
    status = fields.Many2one('minutas.xmarts.estatus', string='Estatus de actividades')

class MinutasXmartsActivids(models.Model):
    _name = 'minutas.xmarts.activids'

    minuta_id = fields.Many2one('minutas.xmarts', string='Minuta', ondelete='cascade', index=True, copy=False)
    name = fields.Many2one('project.task',string='Tarea',ondelete='restrict')
    asignado = fields.Char(string='Asignado a', related='name.user_id.name', readonly=True)
    limite = fields.Date(string='Fecha limite', related='name.date_deadline', readonly=True)
    etapa = fields.Char(string='Etapa', related='name.stage_id.name', readonly=True)
    observaciones =  fields.Text(string='Descripcion')

class MinutasXmartsCompromisos(models.Model):
    _name = 'minutas.xmarts.compromisos'

    minuta_id = fields.Many2one('minutas.xmarts', string='Minuta', ondelete='cascade', index=True, copy=False)
    name = fields.Many2one('project.task',string='Tarea',ondelete='restrict')
    asignado = fields.Char(string='Asignado a', related='name.user_id.name', readonly=True)
    limite = fields.Date(string='Fecha limite', related='name.date_deadline', readonly=True)
    etapa = fields.Char(string='Etapa', related='name.stage_id.name', readonly=True)
    observaciones =  fields.Text(string='Descripcion')

class MinutasXmartsHitos(models.Model):
    _name = 'minutas.xmarts.hitos'
    name = fields.Char('Hito')

class MinutasXmartsEstatus(models.Model):
    _name = 'minutas.xmarts.estatus'
    name = fields.Char('Estatus de actividad')


class hrEmployeeMinutas(models.Model):
    _name='hr.employee'
    _inherit='hr.employee'

    employe_minutas_count = fields.Integer(string="", default=0, compute='count_minutas_employee')

    def count_minutas_employee(self):
        cr = self.env.cr
        sql = "select coalesce(count(distinct mx.id),0) from minutas_xmarts mx inner join minutas_xmarts_asistenciain mxa on mx.id=mxa.minuta_id where mxa.name='"+str(self.id)+"';"
        cr.execute(sql)
        minutas = cr.fetchone()
        self.employe_minutas_count=minutas[0]


class hrProjectMinutas(models.Model):
    _name='project.project'
    _inherit='project.project'

    project_minutas_count = fields.Integer(string="", default=0, compute='count_minutas_project')

    def count_minutas_project(self):
        cr = self.env.cr
        sql = "select coalesce(count(distinct mx.id),0) from minutas_xmarts mx inner join minutas_xmarts_asistenciain mxa on mx.id=mxa.minuta_id where mx.proyecto='"+str(self.id)+"';"
        cr.execute(sql)
        minutas = cr.fetchone()
        self.project_minutas_count=minutas[0]


    
    def mis_minutas_search(self):
        cr = self.env.cr
        sql = "select * from minutas_xmarts mx inner join minutas_xmarts_asistenciain mxa on mxa.minuta_id=mx.id where mxa.name='"+str(self.env.uid)+"';"
        cr.execute(sql)
        minutas = cr.fetchall()
        lista=[]
        for l in minutas:
            lista.append(l[0])
        action = {
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'name': _('Minutas del proyecto'),
            'res_model': 'minutas.xmarts',
            'domain': [('id', 'in', lista)],
        }
        return action