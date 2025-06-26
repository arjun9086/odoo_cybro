# -*- coding: utf-8 -*-
"""product product model"""
from odoo import models


class PaymentProvider(models.Model):
    """Product data fields loading"""
    _inherit = 'payment.provider'