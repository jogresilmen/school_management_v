# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class SchoolDashboardController(http.Controller):

    @http.route('/school/powerbi_dashboard', type='http', auth='user', website=False)
    def powerbi_dashboard(self, **kw):
        # Obtenemos el link desde los parámetros del sistema para no tenerlo en el código
        powerbi_url = request.env['ir.config_parameter'].sudo().get_param('school_management_v.powerbi_url')

        if not powerbi_url:
            return "La URL del dashboard de Power BI no está configurada."

        # Renderizamos una vista simple que solo contiene el iframe
        # Esto oculta la URL real del inspector del navegador del cliente
        return request.render('school_management_v.powerbi_iframe_template', {'powerbi_url': powerbi_url})
