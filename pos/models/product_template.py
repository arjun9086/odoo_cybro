# -*- coding: utf-8 -*-
from odoo import models, fields


class ProductTemplate(models.Model):
    """Adding rating field to the pos product """
    # _name = 'product.product'
    _inherit = ['product.template']
    _description = 'product form'

    rating = fields.Selection(
        selection=[('0', 'No rating'),
                   ('1', 'One star'),
                   ('2', 'Two star'),
                   ('3', 'Three star'),
                   ('4', 'Four star'),
                   ('5', 'Five star')
                   ], string='Rating')

