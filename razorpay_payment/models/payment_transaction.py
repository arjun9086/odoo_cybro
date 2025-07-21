# -*- coding: utf-8 -*-
"""payment transaction  model"""
from datetime import datetime
import logging
from dateutil.relativedelta import relativedelta
from odoo import models
from odoo.addons.payment import utils as payment_utils
from odoo.addons.razorpay_payment import const
_logger = logging.getLogger(__name__)

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
        order_id = self._razorpay_create_order(customer_id)['id']
        return {
            'razorpay_key_id': self.provider_id.razorpay_new_key_id,
            'razorpay_public_token': self.provider_id._razorpay_get_public_token(),
            'razorpay_customer_id': customer_id,
            'razorpay_order_id': order_id,
            'reference': self.reference,
        }

    def _razorpay_create_customer(self):
        payload = {
            'name': self.partner_name,
            'email': self.partner_email or '',
            'contact': self.partner_phone and self._validate_phone_number(self.partner_phone) or '',
            'fail_existing': '0',
        }
        customer_data = self.provider_id._razorpay_make_request('customers', payload=payload)
        return customer_data

    def _razorpay_create_order(self, customer_id=None):
        payload = self._razorpay_prepare_order_payload(customer_id=customer_id)
        return self.provider_id._razorpay_make_request('orders', payload)

    def _razorpay_prepare_order_payload(self, customer_id=None):
        converted_amount = payment_utils.to_minor_currency_units(self.amount, self.currency_id)
        payload = {
            'amount': converted_amount,
            'currency': self.currency_id.name,
        }
        if self.operation in ['online_direct', 'validation']: #used for emi,card saving
            payload['customer_id'] = customer_id
            if self.tokenize:
                payload['token'] = {
                    'max_amount': payment_utils.to_minor_currency_units(
                        self._razorpay_get_mandate_max_amount(), self.currency_id
                    ),
                    'expire_at': int((datetime.now() + relativedelta(years=10)).timestamp()),
                    'frequency': 'as_presented',
                }
        if self.provider_id.capture_manually:
            payload['payment'] = {
                'capture': 'manual',
                'capture_options': {
                    'manual_expiry_period': 7200,
                    'refund_speed': 'normal',
                }
            }
        return payload
