# -*- coding: utf-8 -*-
import json
from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    """class for website sale """
    _inherit = ['res.config.settings']
    _description = 'Pos module settings'

    is_discount_limit = fields.Boolean(
        string='Enable Discount Limit',
        help="If checked, a maximum discount percentage can be set for POS sessions.",
        config_parameter='pos_discount_limit.is_discount_limit',
    )
    discount = fields.Float(
        string='Maximum Discount (%)',
        help="The maximum percentage discount allowed per order line in POS sessions (0 means no limit).",
        default=0.0,config_parameter='pos_discount_limit.discount'
    )

    # def set_values(self):
    #     super().set_values()
    #     config = self.env['ir.config_parameter'].sudo()
    #     config.set_param('pos_discount_limit.is_discount_limit', self.is_discount_limit)
    #     config.set_param('pos_discount_limit.discount', self.discount)
    #
    # @api.model
    # def get_values(self):
    #     res = super().get_values()
    #     session = self.env['pos.session'].sudo().search([])
    #     config = self.env['ir.config_parameter'].sudo()
    #     is_limit = config.get_param('pos_discount_limit.is_discount_limit', default='False')
    #     discount_limit = config.get_param('pos_discount_limit.discount', default='0')
    #     session.discount_limit = discount_limit
    #     res.update({
    #         'is_discount_limit': is_limit == 'True',
    #         'discount': float(discount_limit),
    #     })
    #     return res

