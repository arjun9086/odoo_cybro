# -*- coding: utf-8 -*-
"""sale res config settings"""
from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    """class for ecommerce discount """
    _inherit = ['res.config.settings']
    _description = 'discount for ecommerce orders'

    is_discount = fields.Boolean(config_parameter='ecommerce_discount.is_discount')
    discount = fields.Integer('Discount', config_parameter='ecommerce_discount.discount')
