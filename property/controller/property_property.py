# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class PropertyDetails(http.Controller):

    @http.route('/property', auth='public', website=True)
    def index(self):
        name = request.env['property.property'].sudo().search([])
        print(name)
        return request.render('property.property_details', {'property': name})
