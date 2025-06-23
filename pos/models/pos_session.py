# -*- coding: utf-8 -*-
"""pos session"""
from odoo import models, fields


class PosSession(models.Model):
    """Class for pos session field"""
    _inherit = ['pos.session']

    discount_limit = fields.Float('Discount limit')

    def _load_pos_data_fields(self, config_id):
        fields = super()._load_pos_data_fields(config_id)
        fields.append('discount_limit')
        return fields
