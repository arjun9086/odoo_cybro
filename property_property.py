# -*- coding: utf-8 -*-
from docutils.nodes import target

from odoo import models, fields


class PropertyProperty(models.Model):
    """class Property_Property """
    _name = "property.property"
    _description = 'Property Management'
    _inherit = ['mail.thread']

    name = fields.Char(string="Name")
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
    property_count = fields.Integer(string="Rental",compute="compute_property_count")


    def compute_property_count(self):
        """smart button"""
        for record in self:
            record.property_count = self.env['property.rental'].search_count([("property_id", "=", self.id)])

    def action_get_rental_record(self):
        """smart button config"""
        self.ensure_one()
        return  {
            'type': 'ir.actions.act_window',
            'name': 'rental',
            'view_mode': 'list,form',
            'res_model': 'property.rental',
            'target':'current',
            'domain': [('property_id', '=', self.id)],
            'context': "{ }"
        }