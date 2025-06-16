# -*- coding: utf-8 -*-
"""utf8"""
from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    """class for website sale """
    _inherit = ['res.config.settings']
    _description = 'Pos module settings'

    # product_id = fields.Many2many('product.product')
    discount_limit_id = fields.Many2one('product.product')
