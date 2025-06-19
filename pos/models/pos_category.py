from odoo import models, fields


class PosSession(models.Model):
    _inherit = ['pos.session']

    discount_limit = fields.Float('Discount limit')

    # print(discount_limit)

    def _load_pos_data_fields(self, config_id):
        fields = super()._load_pos_data_fields(config_id)
        fields.append('discount_limit')
        print(fields)
        return fields

