from odoo import fields, models, api

class PosSession(models.Model):
    _inherit = 'pos.session'

    max_discount_limit = fields.Float(string="Maximum Discount Limit", default=0.0, help="Maximum total discount allowed in this session.")
    total_discount_applied = fields.Float(string="Total Discount Applied", compute="_compute_total_discount_applied")

    @api.depends('order_ids')
    def _compute_total_discount_applied(self):
        for session in self:
            orders = self.env['pos.order'].search([('session_id', '=', session.id)])
            session.total_discount_applied = sum(order.amount_discount for order in orders)

    def write(self, vals):
        res = super(PosSession, self).write(vals)
        if 'config_id' in vals:
            for session in self:
                session.max_discount_limit = session.config_id.session_discount_limit
        return res