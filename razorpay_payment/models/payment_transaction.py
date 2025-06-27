# -*- coding: utf-8 -*-
"""product product model"""
from odoo import models,fields


class PaymentTransaction(models.Model):
    """Payment Transaction class"""
    _inherit = 'payment.transaction'

    def _get_specific_processing_values(self, processing_values):

        res = super()._get_specific_processing_values(processing_values)
        if self.provider_code != 'new_razorpay':
            return res

        if self.operation in ('online_token', 'offline'):
            return {}

        customer_id = self._razorpay_create_customer()['id']
        print(customer_id)
        order_id = self._razorpay_create_order(customer_id)['id']
        return {
            'razorpay_key_id': self.provider_id.razorpay_key_id,
            'razorpay_public_token': self.provider_id._razorpay_get_public_token(),
            'razorpay_customer_id': customer_id,
            'is_tokenize_request': self.tokenize,
            'razorpay_order_id': order_id,
        }

    # def _get_specific_rendering_values(self, processing_values):
    #     res = super()._get_specific_rendering_values(processing_values)
    #     if self.provider_code != 'aps':
    #         return res
    #
    #     converted_amount = payment_utils.to_minor_currency_units(self.amount, self.currency_id)
    #     base_url = self.provider_id.get_base_url()
    #     payment_option = aps_utils.get_payment_option(self.payment_method_id.code)
    #     rendering_values = {
    #         'command': 'PURCHASE',
    #         'access_code': self.provider_id.aps_access_code,
    #         'merchant_identifier': self.provider_id.aps_merchant_identifier,
    #         'merchant_reference': self.reference,
    #         'amount': str(converted_amount),
    #         'currency': self.currency_id.name,
    #         'language': self.partner_lang[:2],
    #         'customer_email': self.partner_id.email_normalized,
    #         'return_url': urls.url_join(base_url, APSController._return_url),
    #     }
    #     if payment_option:  # Not included if the payment method is 'card'.
    #         rendering_values['payment_option'] = payment_option
    #     rendering_values.update({
    #         'signature': self.provider_id._aps_calculate_signature(
    #             rendering_values, incoming=False
    #         ),
    #         'api_url': self.provider_id._aps_get_api_url(),
    #     })
    #     return rendering_values
