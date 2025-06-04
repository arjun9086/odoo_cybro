# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class PropertyRental(http.Controller):

    @http.route('/rentals', auth='public', website=True)
    def rental(self):
        rentals = request.env['property.rental'].sudo().search([])
        # print(rentals)
        return request.render('property.property_rental_template', {'rentals': rentals})

    @http.route(['/rental/new'], type='http', auth="public", website=True)
    def rental_form(self):
        owners = request.env['res.partner'].sudo().search([])
        tenants = request.env['res.partner'].sudo().search([])
        types = request.env['property.rental'].sudo().search([])
        properties = request.env['property.property'].sudo().search([])
        return request.render("property.property_rental_form",
                              {'owners': owners,
                               'tenants': tenants,
                               'types': types,
                               'properties': properties,
                               })

    @http.route(['/rental/submit'], type='http', auth="user", website=True, csrf=True)
    def rental_submit(self, **post):
        # property_ids = [int(x) for x in request.httprequest.form.getlist('property_ids')]
        request.env['property.rental'].sudo().create({
            'name': post.get('name'),
            'start_date': post.get('start_date'),
            'end_date': post.get('end_date'),
            # 'type_id': int(post.get('type_id')),
            'tenant_id': int(post.get('tenant_id')),
            'owner_id': int(post.get('owner_id')),
            # 'property_ids': [(6, 0, property_ids)],
        })
        return request.redirect('/rentals')
