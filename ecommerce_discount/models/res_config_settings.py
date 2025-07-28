# -*- coding: utf-8 -*-
"""sale res config settings"""
from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    """class for ecommerce discount """
    _inherit = 'res.config.settings'
    _description = 'discount for ecommerce orders'

    is_discount = fields.Boolean(config_parameter='ecommerce_discount.is_discount')
    discount_type = fields.Selection([('percentage', 'Percentage'), ('amount', 'Amount')],
                                     string='Discount Type',
                                     config_parameter='ecommerce_discount.discount_type',
                                     default='percentage')
    discount = fields.Integer('Discount', config_parameter='ecommerce_discount.discount')
    discount_amount = fields.Float('Discount Amount', config_parameter='ecommerce_discount.discount_amount')
