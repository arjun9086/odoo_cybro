# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json


class PropertyRental(http.Controller):

    @http.route('/rentals', type='http', auth='public', website=True)
    def rental(self):
        rentals = request.env['property.rental'].sudo().search([])
        # print(rentals)
        return request.render('property.property_rental_template', {'rentals': rentals})

    @http.route(['/rental/new'], type='http', auth="public", website=True)
    def rental_form(self):
        # owners = request.env['res.partner'].sudo().search([])
        tenants = request.env['res.partner'].sudo().search([])
        properties = request.env['property.property'].sudo().search([])
        print('hello')
        return request.render("property.property_rental_form",
                              {'tenants': tenants,
                               'properties': properties,
                               })

    @http.route(['/rental/submit'], type='http', auth="public", website=True, csrf=False)
    def rental_submit(self, **post):
        print('Form submitted')
        property_lines = []
        i = 0
        while True:
            prop_id = post.get(f'property_id_{i}')
            print(prop_id)
            qty = post.get(f'quantity_{i}')
            print(qty)
            if not prop_id:
                break  # No more lines
            try:
                property_lines.append((0, 0, {
                    'property_id': int(prop_id),
                    # 'quantity_': float(qty or 1),
                }))
            except Exception as e:
                print(f"Skipping line {i}: {e}")
            i += 1
            print(property_lines)
            print('work')
        request.env['property.rental'].sudo().create({
            'start_date': post.get('start_date'),
            'end_date': post.get('end_date'),
            'type': post.get('type'),
            'tenant_id': int(post.get('tenant_id')),
            'property_ids': property_lines,
            'name': 'New',
        })
        print('Rental record created successfully')
        return request.redirect('/rentals')

    @http.route(['/rental/<int:rental_id>/edit'], type='http', auth="public", website=True)
    def rental_edit(self, rental_id):
        rental = request.env['property.rental'].sudo().browse(rental_id)
        tenants = request.env['res.partner'].sudo().search([])
        properties = request.env['property.property'].sudo().search([])
        # print(amount)
        return request.render("property.property_rental_form", {
            'rental': rental,
            'tenants': tenants,
            'properties': properties,
        })

    @http.route('/property/rent/<int:property_id>', type='http', auth='public', website=True)
    def get_property_rent(self, property_id):
        prop = request.env['property.property'].sudo().browse(property_id)
        print('prop')
        return http.Response(json.dumps({'rent_amount': prop.rent}), content_type='application/json')

