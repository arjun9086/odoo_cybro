# -*- coding: utf-8 -*-
"""utf8"""
from odoo import models, fields


class PropertyFacility(models.Model):
    """class for facilities in property """
    _name = "property.facility"
    _description = 'Property Management'

    name = fields.Char(string="Facility")
    color = fields.Integer()
