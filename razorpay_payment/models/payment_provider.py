# -*- coding: utf-8 -*-
"""payment provider model"""
import logging

import requests

from odoo import models, fields, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class PaymentProvider(models.Model):
    """Payment Provider class"""
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('new_razorpay', "RazorPay")], ondelete={'new_razorpay': 'set default'}
    )
    razorpay_key_id = fields.Char(
        string="Razorpay Key Id",
        help="The key solely used to identify the account with Razorpay.",
    )
    razorpay_key_secret = fields.Char(
        string="Razorpay Key Secret",
    )
    razorpay_webhook_secret = fields.Char(
        string="Razorpay Webhook Secret",
    )

    def _razorpay_make_request(self, endpoint, payload=None, method='POST'):
        self.ensure_one()
        if not self.razorpay_key_id or not self.razorpay_key_secret:
            raise ValidationError(_("Razorpay credentials are missing"))
        url = f"https://api.razorpay.com/v1/{endpoint}"
        auth = (self.razorpay_key_id, self.razorpay_key_secret)
        headers = {'Content-Type': 'application/json'}
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, auth=auth, params=payload, timeout=10)
            else:
                response = requests.request(method, url, headers=headers, auth=auth, json=payload, timeout=10)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            error_data = response.json().get('error', {})
            msg = error_data.get('description', str(e))
            _logger.error("Razorpay API error: %s", msg)
            raise ValidationError(_("Razorpay API error: %s") % msg)
        except requests.exceptions.RequestException as e:
            _logger.error("Razorpay connection error: %s", str(e))
            raise ValidationError(_("Failed to connect to Razorpay: %s") % str(e))
        return response.json()
