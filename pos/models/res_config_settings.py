# -*- coding: utf-8 -*-
"""res config settings"""
from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    """class for adding pos settings/settings """
    _inherit = ['res.config.settings']
    _description = 'Pos module settings'

    is_discount_limit = fields.Boolean(string='Discount limit', config_parameter='pos_discount_limit.is_discount_limit')
    discount = fields.Float('Limit', config_parameter='pos_discount_limit.discount')


