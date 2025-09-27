# -*- coding: utf-8 -*-
"""sale order model"""
from odoo import models, api ,_


class SaleOrder(models.Model):
    """class for Invoice in property """
    _inherit = 'sale.order'
    _description = 'Sale order'

    def _cart_update(self, product_id=None, line_id=None, add_qty=0, set_qty=0, **kwargs):
        """Apply global discount from settings if enabled"""
        res = super()._cart_update(product_id=product_id, line_id=line_id, add_qty=add_qty, set_qty=set_qty, **kwargs)

        if not self.env.context.get('website_id'):
            return res

        config = self.env['ir.config_parameter'].sudo()
        is_discount_enabled = config.get_param('ecommerce_discount.is_discount') == 'True'
        discount_percent = float(config.get_param('ecommerce_discount.discount') or 0.0)

        # Remove existing discount lines
        discount_lines = self.order_line.filtered(
            lambda l: l.product_id and l.product_id.default_code == 'DISCOUNT_LINE')
        discount_lines.unlink()

        if is_discount_enabled and discount_percent > 0:
            discount_product = self.env['product.product'].sudo().search([('default_code', '=', 'DISCOUNT_LINE')],
                                                                         limit=1)
            if not discount_product:
                # Auto-create if not present
                discount_product = self.env['product.product'].create({
                    'name': 'Discount',
                    'default_code': 'DISCOUNT_LINE',
                    'type': 'service',
                    'list_price': 0.0,
                    'sale_ok': True,
                    'invoice_policy': 'order',
                })

            # Compute discount amount from current lines (excluding discount lines)
            subtotal = sum(self.order_line.filtered(lambda l: l.product_id.default_code != 'DISCOUNT_LINE').mapped(
                'price_subtotal'))
            discount_amt = -(subtotal * discount_percent / 100.0)

            # Add negative discount line
            if discount_amt != 0:
                self.order_line.create({
                    'order_id': self.id,
                    'product_id': discount_product.id,
                    'name': _("Discount\n%0.2f%%") % discount_percent,
                    'product_uom_qty': 1,
                    'price_unit': discount_amt,
                })
        return res

# def _cart_update(self, product_id=None, line_id=None, add_qty=0, set_qty=0, **kwargs):
    #     """Override to apply ecommerce discount when product is added to cart."""
    #     res = super()._cart_update(product_id=product_id, line_id=line_id, add_qty=add_qty, set_qty=set_qty, **kwargs)
    #     # Only apply for website orders
    #     if self.env.context.get('website_id'):
    #         is_discount_enabled = self.env['ir.config_parameter'].sudo().get_param(
    #             'ecommerce_discount.is_discount') == 'True'
    #         discount_percent = int(self.env['ir.config_parameter'].sudo().get_param('ecommerce_discount.discount') or 0)
    #         if is_discount_enabled and discount_percent > 0:
    #             for line in self.order_line:
    #                 # Only discount product lines (not delivery, coupon, etc.)
    #                 if line.product_id and not line.is_delivery:
    #                     line.discount = discount_percent
    #     return res
