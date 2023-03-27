
import binascii

from odoo import fields, http, SUPERUSER_ID, _
from odoo.exceptions import AccessError, MissingError, ValidationError
from odoo.fields import Command
from odoo.http import request

from odoo.addons.payment.controllers import portal as payment_portal
from odoo.addons.payment import utils as payment_utils
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.addons.portal.controllers import portal
from odoo.addons.portal.controllers.portal import pager as portal_pager


class MinutasPortal(portal.CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        partner = request.env.user.partner_id
        project = request.env['project.project'].sudo().search([
            ('partner_id','=', partner.id)
        ])
        print('PROYECTOOOOOO-------- ', project.ids)
        domain = [
            ('proyecto','in', project.ids)
        ]

        MinutasPortal = request.env['minutas.xmarts']
        if 'minutas_count' in counters:
            values['minutas_count'] = MinutasPortal.search_count(domain) \
                if MinutasPortal.check_access_rights('read', raise_exception=False) else 0
        return values

    def _get_minuta_searchbar_sortings(self):
        return {
            'date': {'label': _('Fecha de la Minuta'), 'minuta': 'fecha_hora desc'},
            'name': {'label': _('Referencia'), 'minuta': 'name'},
            'stage': {'label': _('Estado'), 'minuta': 'status'},
        }

    def _prepare_minutas_portal_rendering_values(
            self, page=1, date_begin=None, date_end=None, sortby=None, minuta_page=False, **kwargs
        ):
            print("_prepare_minutas_portal_rendering_values")
            MinutasXmarts = request.env['minutas.xmarts']

            if not sortby:
                sortby = 'date'

            partner = request.env.user.partner_id
            values = self._prepare_portal_layout_values()

            url = "/my/minutas"
            project = request.env['project.project'].sudo().search([
                ('partner_id','=', partner.id)
            ])
            print('PROYECTOOOOOO-------- ', project.ids)
            domain = [
                ('proyecto','in', project.ids)
            ]

            searchbar_sortings = self._get_minuta_searchbar_sortings()

            sort_minuta = searchbar_sortings[sortby]['minuta']

            if date_begin and date_end:
                domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

            pager_values = portal_pager(
                url=url,
                total=MinutasXmarts.search_count(domain),
                page=page,
                step=self._items_per_page,
                url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            )
            minutas = MinutasXmarts.search(domain, order=sort_minuta, limit=self._items_per_page, offset=pager_values['offset'])
            print(minutas, '-------------------')

            values.update({
                'date': date_begin,
                'minutas': minutas.sudo(),
                'page_name': 'minutas',
                'pager': pager_values,
                'default_url': url,
                'searchbar_sortings': searchbar_sortings,
                'sortby': sortby,
            })

            return values

    @http.route(['/my/minutas/<int:minuta_id>'], type='http', auth="public", website=True)
    def portal_minuta_page(self, minuta_id, report_type=None, access_token=None, message=False, download=False, **kw):
        print("HTTP -- portal_minuta_page")
        try:
            minuta_sudo = self._document_check_access('minutas.xmarts', minuta_id, access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        if report_type in ('html', 'pdf', 'text'):
            return self._show_report(model=minuta_sudo, report_type=report_type, report_ref='minutas.reporte_minutas', download=download)

        if request.env.user.share and access_token:
            today = fields.Date.today().isoformat()
            session_obj_date = request.session.get('view_minuta_%s' % minuta_sudo.id)
            if session_obj_date != today:
                request.session['view_minuta_%s' % minuta_sudo.id] = today
                partner = request.env.user.partner_id
                context = {'lang': partner.lang}
                msg = _('Minuta Proyecto %s', minuta_sudo.proyecto.name)
                del context
                _message_post_helper(
                    "minutas.xmarts",
                    minuta_sudo.id,
                    message=msg,
                    token=minuta_sudo.access_token,
                    message_type="notification",
                    subtype_xmlid="mail.mt_note",
                    partner_ids = [partner.id], 
                )

        backend_url = f'/web#model={minuta_sudo._name}'\
                      f'&id={minuta_sudo.id}'\
                      f'&action={minuta_sudo._get_portal_return_action().id}'\
                      f'&view_type=form'
        values = {
            'minuta_xmarts': minuta_sudo,
            'message': message,
            'report_type': 'html',
            'backend_url': backend_url,
            'res_company': minuta_sudo.company_id,  # Used to display correct company logo
        }

        history_session_key = 'my_minuta_history'

        values = self._get_page_view_values(
            minuta_sudo, access_token, values, history_session_key, False)
        print(values, '___________')
        return request.render('minutas.minuta_xmarts_portal_template', values)


    @http.route(['/my/minutas', '/my/minutas/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_minutas(self, **kwargs):
        print("HTTP portal_my_minutas")
        values = self._prepare_minutas_portal_rendering_values(minuta_page=True, **kwargs)
        request.session['my_minuta_history'] = values['minutas'].ids[:100]
        return request.render("minutas.portal_my_minutas", values)
    
    @http.route(['/my/minutas/<int:minuta_id>/accept'], type='json', auth="public", website=True)
    def portal_minuta_accept(self, minuta_id, access_token=None, name=None, signature=None):
        print("FIRMAAAAAAAAA", name, signature )
        # get from query string if not on json param
        access_token = access_token or request.httprequest.args.get('access_token')
        try:
            minuta_sudo = self._document_check_access('minutas.xmarts', minuta_id, access_token=access_token)
        except (AccessError, MissingError):
            return {'error': _('Invalid order.')}

        if minuta_sudo.signature:
            return {'error': _('La Minuta ya ha sido Firmada')}
        if not signature:
            return {'error': _('No hay Firma, favor de firmar primero')}

        try:
            minuta_sudo.write({
                'signature': signature,
                'client_has_sing': True
            })
            request.env.cr.commit()
        except (TypeError, binascii.Error) as e:
            return {'error': _('Invalid signature data.')}

        pdf = request.env['ir.actions.report'].sudo()._render_qweb_pdf('minutas.reporte_minutas', [minuta_sudo.id])[0]

        _message_post_helper(
            'minutas.xmarts',
            minuta_sudo.id,
            _('Minuta firmada por %s', name),
            attachments=[('%s.pdf' % minuta_sudo.name, pdf)],
            token=access_token,
        )

        query_string = '&message=sign_ok'
        return {
            'force_refresh': True,
            'redirect_url': minuta_sudo.get_portal_url(query_string=query_string),
        }