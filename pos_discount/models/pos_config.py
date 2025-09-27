from odoo import fields, models

class PosConfig(models.Model):
    _inherit = 'pos.config'

    session_discount_limit = fields.Float(string="Session Discount Limit",
                                          default=0.0,
                                          help="Maximum total discount allowed in a POS session (0 for no limit).")