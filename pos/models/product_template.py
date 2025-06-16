# -*- coding: utf-8 -*-
from odoo import models, fields


class ProductTemplate(models.Model):
    """Adding rating field to the pos product """
    _inherit = ['product.template']
    _description = 'product form'

    rating = fields.Selection(
        selection=[('0', 'No rating'),
                   ('1', '1 star'),
                   ('2', '2 star'),
                   ('3', '3 star'),
                   ('4', '4 star'),
                   ('5', '5 star')
                   ], string='Rating')
