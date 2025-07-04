import base64

from odoo import models, fields, api
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta


class IrConfigParameter(models.Model):
    _inherit = 'ir.config_parameter'

    @api.model
    def _cron_send_sales_reports(self):
        # Fetch saved config values
        config_param = self.env['ir.config_parameter'].sudo()
        is_active = config_param.get_param('sale_report.is_sale_report') == 'True'
        if not is_active:
            return

        today = fields.Date.today()

        method = config_param.get_param('sale_report.method')
        print(method)
        start_date = config_param.get_param('sale_report.start_date')
        print(start_date)
        end_date = config_param.get_param('sale_report.end_date')
        team_id = config_param.get_param('sale_report.sales_team_id')
        customer_ids_str = config_param.get_param('sale_report.customer_ids')

        if not start_date or not end_date:
            return

        # Validate trigger date
        if fields.Date.from_string(end_date) > today:
            return
        # if method == 'weekly' and today.weekday() != 6:
        #     print('returned weekday')
        #     return
        # elif method == 'monthly' and str(today) != end_date:
        #     print('returned monthly')
        #     return
        domain = [('date_order', '>=', start_date),
                  ('date_order', '<=', end_date)]
        if team_id:
            domain.append(('team_id', '=', int(team_id)))

        orders = self.env['sale.order'].sudo().search(domain)
        if not orders:
            print('no orders')
            return
        print('before report')
        # Generate PDF report for each order (or combined)
        report = self.env.ref('sale.action_report_saleorder') # Default Odoo Sale Order Report
        print(report)
        pdf_content, _ = report._render_qweb_pdf(orders.ids)
        attachment = self.env['ir.attachment'].create({
            'name': 'Sales_Report.pdf',
            'type': 'binary',
            'datas': base64.b64encode(pdf_content),
            'res_model': 'mail.mail',
        })

        # Email to selected customers
        # customer_ids = list(map(int, customer_ids_str.split(','))) if customer_ids_str else []
        if isinstance(customer_ids_str, str):
            customer_ids = list(map(int, customer_ids_str.split(','))) if customer_ids_str else []
        elif isinstance(customer_ids_str, list):
            customer_ids = customer_ids_str
        else:
            customer_ids = []
        customers = self.env['res.partner'].sudo().browse(customer_ids)

        for customer in customers:
            if not customer.email:
                continue
            mail_values = {
                'subject': 'Sales Report',
                'body_html': '<p>Dear %s,<br/><br/>Please find the attached sales report.</p>' % customer.name,
                'email_to': customer.email,
                'email_from': self.env.user.email or 'noreply@example.com',
                'attachment_ids': [(4, attachment.id)],
            }
            self.env['mail.mail'].sudo().create(mail_values).send()
