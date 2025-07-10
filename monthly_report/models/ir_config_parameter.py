# -*- coding: utf-8 -*-
"""ir_config_parameter"""
import base64
import logging
from odoo import models, fields

class IrConfigParameter(models.Model):
    """ConfigParameter Class"""
    _inherit = 'ir.config_parameter'

    def _cron_send_sales_reports(self):
        """sending sales report"""
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
            return
        if method == 'weekly' and today.weekday() != 3:
            return
        if method == 'monthly' and today.day != 10:
            return
        # customer_ids_str
        customer_ids = []
        if customer_ids_str:
            customer_ids = [int(cid) for cid in customer_ids_str.split(',') if cid]
        if not customer_ids:
            return
        customers = self.env['res.partner'].sudo().browse(customer_ids).filtered(lambda c: c.exists() and c.email)
        if not customers:
            return
        template = self.env.ref('monthly_report.sale_report_mail_template')
        for customer in customers:
            # Search orders
            domain = [('date_order', '>=', start_date), ('date_order', '<=', end_date),
                      ('partner_id', '=', customer.id)]
            if team_id and team_id != 'False':
                domain.append(('team_id', '=', int(team_id)))
            orders = self.env['sale.order'].sudo().search(domain)
            if not orders:
                return
            pdf_content, _ = self.env['ir.actions.report']._render_qweb_pdf('monthly_report.action_sale_report',
                                                                            res_ids=orders.ids,
                                                                            data={
                                                                                'custom_values': {
                                                                                    'method': method,
                                                                                    'team': self.env['crm.team'].browse(
                                                                                        int(team_id)).name if team_id and
                                                                                                              team_id != 'False' else 'All Teams',
                                                                                }
                                                                            })
            # Create attachment
            attachment = self.env['ir.attachment'].sudo().create({
                'name': f'Sales_Report_{customer.name}.pdf',
                'type': 'binary',
                'datas': base64.b64encode(pdf_content),
                'res_model': 'mail.mail',
            })
            recipient_emails = [customer.email]
            if team_id and team_id != 'False':
                team = self.env['crm.team'].sudo().browse(int(team_id))
                team_members = team.member_ids.filtered(lambda u: u.email)
            else:
                all_teams = self.env['crm.team'].sudo().search([])
                team_members = all_teams.mapped('member_ids').filtered(lambda u: u.email)
            recipient_emails += [user.email for user in team_members if user.email]
            recipient_emails = list(set(recipient_emails))
            template.send_mail(customer.id, force_send=True, email_values={
                'subject': f'Sale Report {customer.name}',
                'email_to': ','.join(recipient_emails),
                'attachment_ids': [(4, attachment.id)], })
