# -*- coding: utf-8 -*-
"""res config settings"""
from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    """class for adding pos settings/settings """
    _inherit = ['res.config.settings']
    _description = 'Pos module settings'

    is_discount_limit = fields.Boolean(string='Discount limit')
    discount = fields.Float('Limit')

    def set_values(self):
        """setting values in the settings"""
        super().set_values()
        config = self.env['ir.config_parameter'].sudo()
        config.set_param('pos_discount_limit.is_discount_limit', self.is_discount_limit)
        config.set_param('pos_discount_limit.discount', self.discount)

    @api.model
    def get_values(self):
        """getting the values in the fields"""
        res = super().get_values()
        session = self.env['pos.session'].sudo().search([])
        config = self.env['ir.config_parameter'].sudo()
        is_limit = config.get_param('pos_discount_limit.is_discount_limit', default='False')
        discount_limit = config.get_param('pos_discount_limit.discount', default='0')
        session.discount_limit = discount_limit
        res.update({
            'is_discount_limit': is_limit == 'True',
            'discount': float(discount_limit),
        })
        return res
