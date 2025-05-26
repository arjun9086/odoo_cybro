# -*- coding: utf-8 -*-
from odoo import fields, models


class PropertyReport(models.Model):
    """Property  rental report"""
    _name = 'property.report'
    _description = 'property rental reports'

    property_ids = fields.Many2many('property.line')
