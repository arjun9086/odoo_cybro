from odoo import models, fields

class PosCategory(models.Model):
    _inherit = ['pos.category']

    discount = fields.Integer(string='Discount', config_parameter='pos_discount.discount')
    # category_id = fields.Many2one('pos.category')
    def load_pos_data_fields(self, config_id):
        result = super().load_pos_data_fields(config_id)
        result.append('discount')
        print(result)
        return result
