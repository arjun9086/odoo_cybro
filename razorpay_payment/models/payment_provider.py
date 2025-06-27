# -*- coding: utf-8 -*-
"""payment provider model"""
import logging
from odoo import models,fields

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
        required_if_provider='razorpay',
    )
    razorpay_key_secret = fields.Char(
        string="Razorpay Key Secret",
        required_if_provider='razorpay',
    )
    razorpay_webhook_secret = fields.Char(
        string="Razorpay Webhook Secret",
        required_if_provider='razorpay',
    )