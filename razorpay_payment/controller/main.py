import logging
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)

class RazorpayController(http.Controller):

    @http.route('/payment/razorpay_plus/verify_payment', type='json', auth='public')
    def razorpay_verify_payment(self, reference, razorpay_payment_id):

        payment = request.env['payment.transaction'].sudo().search(
            [('reference', '=', reference)], limit=1)
        if payment:
            provider = payment.provider_id
            payment_data = provider._razorpay_make_request(f'payments/{razorpay_payment_id}', method='GET')

            if payment_data.get('status') == 'captured':
                payment.provider_reference = razorpay_payment_id
                payment._set_done()
                _logger.info(f"Payment {razorpay_payment_id} for transaction {reference} successfully processed")

                if payment.sale_order_ids:
                    for order in payment.sale_order_ids:
                        if order.state == 'draft':
                            order.action_confirm()
                            _logger.info(f"Sale order {order.name} confirmed for transaction {reference}")

                return {'success': True}
            else:
                _logger.warning(
                    f"Payment {razorpay_payment_id} status is {payment_data.get('status')}, not captured"
                )
                return {'warning': f"Payment status: {payment_data.get('status')}"}
        return {'error': f"No transaction found with reference: {reference}"}