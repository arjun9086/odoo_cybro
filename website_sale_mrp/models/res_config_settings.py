# -*- coding: utf-8 -*-
"""utf8"""
from odoo import models, fields,api


class ResConfigSettings(models.TransientModel):
    """class for website sale """
    _inherit = ['res.config.settings']
    _description = 'website sale module'

    bom_product_ids = fields.Many2many('product.product')

    def set_values(self):
        super().set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'my_website_bom.bom_product_ids',
            ','.join(map(str, self.bom_product_ids.ids))
        )

    @api.model
    def get_values(self):
        res = super().get_values()
        value = self.env['ir.config_parameter'].sudo().get_param('my_website_bom.bom_product_ids', default='')
        product_ids = [int(product_id) for product_id in value.split(',') if product_id]
        res.update(bom_product_ids=[(6, 0, product_ids)])
        return res