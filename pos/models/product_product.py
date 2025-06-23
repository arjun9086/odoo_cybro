# -*- coding: utf-8 -*-
"""product product model"""
from odoo import models


class ProductProduct(models.Model):
    """Product data fields loading"""
    _inherit = ['product.product']

    def _load_pos_data_fields(self, config_id):
        result = super()._load_pos_data_fields(config_id)
        result.append('rating')
        return result
