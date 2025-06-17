from odoo import models, fields

class PosCategory(models.Model):
    _inherit = ['pos.category']

    discount = fields.Integer(string='Discount', config_parameter='pos_discount.discount')
    #category_id = fields.Many2one('pos.category')

    def load_pos_data_fields(self, config_id):
        fields = super().load_pos_data_fields(config_id)
        if 'discount' not in fields:
            fields.append('discount')  # Send discount field to JS
        return fields
