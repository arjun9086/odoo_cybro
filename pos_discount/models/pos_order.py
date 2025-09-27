from odoo import fields, models

class PosOrder(models.Model):
    _inherit = 'pos.order'

    amount_discount = fields.Float(string="Discount Amount", compute="_compute_amount_discount")

    def _compute_amount_discount(self):
        for order in self:
            discount = 0.0
            for line in order.lines:
                if line.discount:
                    discount += (line.price_unit * line.qty * line.discount) / 100
            order.amount_discount = discount