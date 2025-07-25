# -*- coding: utf-8 -*-
"""sale order model"""
from odoo import models, api


class SaleOrder(models.Model):
    """class for Invoice in property """
    _inherit = 'sale.order'
    _description = 'Sale order'

    def _cart_update(self, product_id=None, line_id=None, add_qty=0, set_qty=0, **kwargs):
        """Override to apply ecommerce discount when product is added to cart."""
        res = super()._cart_update(product_id=product_id, line_id=line_id, add_qty=add_qty, set_qty=set_qty, **kwargs)
        # Only apply for website orders
        if self.env.context.get('website_id'):
            is_discount_enabled = self.env['ir.config_parameter'].sudo().get_param(
                'ecommerce_discount.is_discount') == 'True'
            discount_percent = int(self.env['ir.config_parameter'].sudo().get_param('ecommerce_discount.discount') or 0)
            if is_discount_enabled and discount_percent > 0:
                for line in self.order_line:
                    # Only discount product lines (not delivery, coupon, etc.)
                    if line.product_id and not line.is_delivery:
                        line.discount = discount_percent
        return res
