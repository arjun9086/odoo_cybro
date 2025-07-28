# -*- coding: utf-8 -*-
"""sale order model"""
from odoo import models, _


class SaleOrder(models.Model):
    """class for sale order """
    _inherit = 'sale.order'
    _description = 'Sale order'

    def _cart_update(self, product_id=None, line_id=None, add_qty=0, set_qty=0, **kwargs):
        """Apply global discount from settings if enabled and capped by discount amount"""
        res = super()._cart_update(product_id=product_id, line_id=line_id, add_qty=add_qty, set_qty=set_qty, **kwargs)
        if not self.env.context.get('website_id'):
            return res
        config = self.env['ir.config_parameter']
        is_discount_enabled = config.get_param('ecommerce_discount.is_discount') == 'True'
        discount_type = config.get_param('ecommerce_discount.discount_type')
        discount_percent = float(config.get_param('ecommerce_discount.discount') or 0.0)
        discount_amount = float(config.get_param('ecommerce_discount.discount_amount') or 0.0)
        # Remove existing discount lines
        discount_lines = self.order_line.filtered(lambda l: l.product_id.default_code == 'DISCOUNT_LINE')
        discount_lines.unlink()
        real_lines = self.order_line.filtered(
            lambda l: l.product_id and l.product_id.default_code != 'DISCOUNT_LINE')
        if not real_lines or not is_discount_enabled:
            return res
        # Get or create discount product
        discount_product = self.env['product.product'].sudo().search([('default_code', '=', 'DISCOUNT_LINE')], limit=1)
        if not discount_product:
            discount_product = self.env['product.product'].sudo().create({
                'name': 'Discount',
                'default_code': 'DISCOUNT_LINE',
                'type': 'service',
                'list_price': 0.0,
                'sale_ok': True,
                'invoice_policy': 'order',
            })
        # Calculate subtotal (excluding any previous discount lines)
        subtotal = sum(real_lines.mapped('price_subtotal'))
        discount_amt = 0.0
        if discount_type == 'percentage' and discount_percent > 0:
            discount_amt = subtotal * discount_percent / 100.0
        elif discount_type == 'amount' and discount_amount > 0:
            discount_amt = discount_amount
        # Cap the discount to max allowed (discount_amount)
        if discount_amount > 0:
            discount_amt = min(discount_amt, discount_amount)
        if discount_amt > 0:
            self.order_line.create({
                'order_id': self.id,
                'product_id': discount_product.id,
                'name': _("Discount (%s)") % (
                    f"{discount_percent}%" if discount_type == 'percentage' else f"₹{discount_amt}"),
                'product_uom_qty': 1,
                'price_unit': -discount_amt,
            })
        return res
