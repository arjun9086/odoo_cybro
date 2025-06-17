# -*- coding: utf-8 -*-
"""utf8"""
from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    """class for website sale """
    _inherit = ['res.config.settings']
    _description = 'Pos module settings'

    is_discount_limit = fields.Boolean(string='Discount limit')
    pos_category_ids = fields.Many2many('pos.category', 'pos_product_category_ids')
    discount = fields.Integer(string='Discount', config_parameter='pos_discount.discount')

    def set_values(self):
        super().set_values()
        config = self.env['ir.config_parameter'].sudo()

        # Save the boolean flag
        config.set_param('pos_discount_limit_enabled', self.is_discount_limit)

        # Save selected POS categories as comma-separated string
        category_ids = ','.join(str(cat.id) for cat in self.pos_category_ids)
        config.set_param('pos_discount.category_ids', category_ids)

    @api.model
    def get_values(self):
        res = super().get_values()
        config = self.env['ir.config_parameter'].sudo()

        # Read saved values
        discount = config.get_param('pos_discount.discount', default='0')
        category_ids_str = config.get_param('pos_discount.category_ids', default='')
        category_ids = [int(x) for x in category_ids_str.split(',') if x]

        res.update({
            'is_discount_limit': config.get_param('pos_discount_limit_enabled', default=False) == 'True',
            'discount': int(discount),
            'pos_category_ids': [(6, 0, category_ids)],
        })
        return res
    # def set_values(self):
    #     super().set_values()
    #     config = self.env['ir.config_parameter'].sudo()
    #     config.set_param('pos_discount_limit_enabled', self.is_discount_limit)
    #
    # @api.model
    # def get_values(self):
    #     res = super().get_values()
    #     config = self.env['ir.config_parameter'].sudo()
    #     discount = config.get_param('pos_discount.discount', default='0')
    #     category_ids_str = config.get_param('pos_discount.category_ids', default='')
    #     category_ids = [int(x) for x in category_ids_str.split(',') if x]
    #     res.update({
    #         'is_discount_limit': config.get_param('pos_discount_limit_enabled', default=False),
    #         'discount': int(discount),
    #         'pos_category_ids': [(6, 0, category_ids)],
    #     })
    #     print(res)
    #     return res
