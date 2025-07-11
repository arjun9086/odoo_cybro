# -*- coding: utf-8 -*-
"""snippets of property list"""
from odoo import http
from odoo.http import request


class PropertyProperty(http.Controller):

    @http.route('/property/json', type='json', auth='public', website=True, csrf=False)
    def index(self, offset=0):
        """Property list"""
        offset = int(offset)
        properties = request.env['property.property'].sudo().search([], offset=offset)
        return properties.read(['id', 'name', 'image'])

    @http.route('/property_details/<int:name>', type='http', auth='public', website=True, csrf=False)
    def get_property_details(self, name):
        """Getting property Details"""
        name = request.env['property.property'].sudo().browse(name)
        return request.render('property.property_information_template', {
            'property': name,
        })
