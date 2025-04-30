# -*- coding: utf-8 -*-
from odoo import models, fields


class PropertyProperty(models.Model):
    """class Property_Property """
    _name = "property.property"
    _description = 'Property Management'
    _inherit = ['mail.thread']

    name = fields.Char(required=True)
    street1 = fields.Char()
    street2 = fields.Char()
    state = fields.Char()
    country = fields.Char()
    built_date = fields.Date(string="Built Date", default=fields.Date.context_today)
    description = fields.Html()
    owner_id = fields.Many2one('res.partner', string='Owner')
    can_be_sold = fields.Boolean()
    legal_amount = fields.Integer()
    image = fields.Binary()
    rent = fields.Integer()
    status = fields.Selection(
        selection=[('rented', 'Rented'), ('leased', 'Leased'), ('sold', 'Sold'), ('draft', 'Draft')],
        string='Status',
        default='rented',
        tracking=True
    )
