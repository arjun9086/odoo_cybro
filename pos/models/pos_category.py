from odoo import models, fields

class PosCategory(models.Model):
    _inherit = ['pos.session']

    def load_pos_data_fields(self, config_id):
        print('discount')
        fields = super().load_pos_data_fields(config_id)
        # if 'discount' not in fields:
        fields.append('discount')
        print(fields)
        return fields
