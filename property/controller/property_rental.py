# -*- coding: utf-8 -*-
"""Website creation and displaying of rental records"""
from odoo import http
from odoo.http import request
import json


class PropertyRental(http.Controller):
    """Property Rental"""

    @http.route('/my/rental_orders', type='http', auth='user', website=True)
    def portal_my_rental_orders(self):
        """Rental orders"""
        rentals = request.env['property.rental'].sudo().search([])
        return request.render('property.portal_my_rental_orders', {
            'rental_orders': rentals,
        })

    @http.route(['/rentals'], type='http', auth="public", website=True)
    def rental_form(self):
        """Rental record form"""
        # owners = request.env['res.partner'].sudo().search([])
        tenants = request.env['res.partner'].sudo().search([])
        properties = request.env['property.property'].sudo().search([])
        return request.render("property.property_rental_form",
                              {'tenants': tenants,
                               'properties': properties,
                               })

    @http.route(['/rental/submit'], type='http', auth="public", website=True, csrf=False)
    def rental_submit(self, **post):
        """Form Submit button"""
        print('Form submitted')
        property_lines = []
        i = 0
        has_property = False  # Track if at least one valid property is added
        while True:
            prop_id = post.get(f'property_id_{i}')
            if not prop_id:
                break  # No more lines
            if prop_id:
                try:
                    property_lines.append((0, 0, {
                        'property_id': int(prop_id),
                    }))
                    has_property = True
                except Exception as e:
                    print(f"Skipping line {i}: {e}")
            i += 1
        if not has_property:
            # Re-render the form with an error message
            tenants = request.env['res.partner'].sudo().search([])
            properties = request.env['property.property'].sudo().search([])
            return request.render("property.property_rental_form", {
                'tenants': tenants,
                'properties': properties,
                'error_message': 'Please select at least one property before submitting.',
            })
        request.env['property.rental'].sudo().create({
            'start_date': post.get('start_date'),
            'end_date': post.get('end_date'),
            'type': post.get('type'),
            'tenant_id': int(post.get('tenant_id')),
            'property_ids': property_lines,
            'name': 'New',
        })
        print('Rental record created successfully')
        return request.redirect('/rental-thank-you')

    @http.route(['/rental/<int:rental_id>/edit'], type='http', auth="public", website=True)
    def rental_edit(self, rental_id):
        """For display Rental records"""
        rental = request.env['property.rental'].sudo().browse(rental_id)
        tenants = request.env['res.partner'].sudo().search([])
        properties = request.env['property.property'].sudo().search([])
        return request.render("property.property_rental_form", {
            'rental': rental,
            'tenants': tenants,
            'properties': properties,
        })

    @http.route('/property/rent/<int:property_id>', type='http', auth='public', website=True)
    def get_property_rent(self, property_id):
        """To get Lease and Rent Amount"""
        prop = request.env['property.property'].sudo().browse(property_id)
        print('prop')
        return http.Response(json.dumps({'rent_amount': prop.rent, 'lease_amount': prop.legal_amount}),
                             content_type='application/json')

    @http.route('/my/rental_orders/<int:rental_id>', type='http', auth='user', website=True)
    def portal_view_rental(self, rental_id):
        """TO view portal rental"""
        rental = request.env['property.rental'].sudo().browse(rental_id)
        if not rental:
            return request.not_found()
        return request.render('property.portal_rental_order_detail', {
            'rental': rental,
        })