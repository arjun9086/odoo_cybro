import base64
import logging

from odoo import models, fields, api
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta


class IrConfigParameter(models.Model):
    _inherit = 'ir.config_parameter'

    def _cron_send_sales_reports(self):
        _logger = logging.getLogger(__name__)
        config_param = self.env['ir.config_parameter'].sudo()

        if config_param.get_param('sale_report.is_sale_report') != 'True':
            _logger.info("Sales report is disabled, skipping report generation.")
            return

        today = fields.Date.today()
        method = config_param.get_param('sale_report.method')
        start_date = config_param.get_param('sale_report.start_date')
        end_date = config_param.get_param('sale_report.end_date')
        team_id = config_param.get_param('sale_report.sales_team_id')
        customer_ids_str = config_param.get_param('sale_report.customer_ids')

        _logger.debug("Parameters: method=%s, start_date=%s, end_date=%s, team_id=%s, customer_ids_str=%r",
                      method, start_date, end_date, team_id, customer_ids_str)

        # Validate parameters
        if not start_date or not end_date:
            _logger.warning("Start date or end date is missing, aborting report generation.")
            return
        try:
            end_date_obj = fields.Date.from_string(end_date)
            if end_date_obj > today:
                _logger.info("End date is in the future, skipping report generation.")
                return
            if method == 'weekly' and today.weekday() != 0:
                _logger.info("Not Monday, skipping weekly report generation.")
                return
            elif method == 'monthly' and today != end_date_obj:
                _logger.info("Today is not the end date, skipping monthly report generation.")
                return
        except ValueError as e:
            _logger.error("Invalid date format: %s", e)
            return

        # Search orders
        domain = [('date_order', '>=', start_date), ('date_order', '<=', end_date)]
        if team_id and team_id != 'False':
            domain.append(('team_id', '=', int(team_id)))
        orders = self.env['sale.order'].sudo().search(domain)
        if not orders:
            _logger.info("No orders found for the given criteria.")
            return

        # Load report
        try:
            # report = self.env.ref('monthly_report.action_custom_sales_report')
            # _logger.debug("Report loaded: %s", report)
            pdf_content, _ = self.env['ir.actions.report']._render_qweb_pdf('monthly_report.action_custom_sales_report',
                                                                            res_ids=orders.ids)

        except Exception as e:
            _logger.error("Failed to render report: %s", e)
            return

        # Create attachment
        attachment = self.env['ir.attachment'].sudo().create({
            'name': f'Sales_Report_{start_date}_to_{end_date}.pdf',
            'type': 'binary',
            'datas': base64.b64encode(pdf_content),
            'res_model': 'mail.mail',
        })

        # Parse customer_ids_str safely
        customer_ids = []
        if customer_ids_str and customer_ids_str != 'False':
            try:
                customer_ids = [int(cid) for cid in customer_ids_str.split(',') if cid]
            except ValueError as e:
                _logger.error("Failed to parse customer_ids: %s", e)
                return

        if not customer_ids:
            _logger.warning("No valid customer IDs found, skipping email sending.")
            return

        customers = self.env['res.partner'].sudo().browse(customer_ids).filtered(lambda c: c.exists() and c.email)
        if not customers:
            _logger.warning("No valid customers with email addresses found.")
            return

        # Load mail template
        try:
            template = self.env.ref('monthly_report.sale_report_template')
        except Exception as e:
            _logger.error("Failed to load mail template: %s", e)
            return

        # Send email to each customer
        for customer in customers:
            try:
                template.with_context({
                    'default_model': 'res.partner',
                    'default_res_id': customer.id,
                    'default_attachment_ids': [(4, attachment.id)],
                }).sudo().send_mail(customer.id, force_send=True)
                _logger.info("Sales report sent to customer: %s", customer.name)
            except Exception as e:
                _logger.error("Failed to send email to customer %s: %s", customer.name, e)