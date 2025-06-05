# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


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
        # Extract all lines using array-style input names
        property_ids = post.getlist('property_ids[]')
        quantities = post.getlist('quantity[]')
        rents = post.getlist('rent[]')

        property_lines = []
        for prop_id, qty, rent in zip(property_ids, quantities, rents):
            try:
                property_lines.append((0, 0, {
                    'property_id': int(prop_id),
                    'quantity_': float(qty or 1),
                    'rent': float(rent or 0),
                }))
            except Exception as e:
                print(f"Skipping invalid line: {e}")
        # Create the rental record
        request.env['property.rental'].sudo().create({
            'start_date': post.get('start_date'),
            'end_date': post.get('end_date'),
            'type': post.get('type'),
            'tenant_id': int(post.get('tenant_id')),
            'property_ids': property_lines,
            'name': 'New',
            'rent': float(post.get('rent') or 0),
        })

        print('Rental record created successfully')
        return request.redirect('/rentals')

