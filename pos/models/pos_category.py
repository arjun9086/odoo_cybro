# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PosSession(models.Model):
    _inherit = ['pos.session']

    discount_limit = fields.Float(
        string='Discount Limit',
        help="The maximum percentage discount allowed per order line in this POS session. (Value inherited from System Settings)"
    )
    def _load_pos_data_fields(self, config_id):
            fields = super()._load_pos_data_fields(config_id)
            fields.append('discount_limit')
            print(fields)
            return fields

