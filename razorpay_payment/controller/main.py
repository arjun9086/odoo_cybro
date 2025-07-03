# -*- coding: utf-8 -*-
import logging
from odoo import http
from odoo.http import request
import json

_logger = logging.getLogger(__name__)

class RazorpayController(http.Controller):

    @http.route('/razorpay_payment/verify_payment', type='json', auth='public')
    def razorpay_payment_verification(self):
        """payment verification"""
        data = json.loads(request.httprequest.data)
        reference = data.get('reference')
        payment_id = data.get('razorpay_payment_id')
        _logger.info(f"[Razorpay] Verification data: {data}")

        if not reference or not payment_id:
            return {'success': False, 'error': 'Missing one or more required fields.'}
        tx = request.env['payment.transaction'].sudo().search(
            [('reference', '=', reference)], limit=1)
        if not tx:
            return {'success': False, 'error': f"No transaction found with reference: {reference}"}
        tx._set_done()


