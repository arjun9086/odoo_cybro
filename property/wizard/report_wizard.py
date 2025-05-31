# -*- coding: utf-8 -*-
"""wizard form to print the pdf report """
from odoo import models, fields
from odoo.exceptions import ValidationError
import io
import xlsxwriter
import json

from odoo.tools import json_default, date_utils


class ReportWizard(models.TransientModel):
    """wizard model"""
    _name = "report.wizard"
    _description = "File wizard"

    owner_id = fields.Many2one('res.partner', string='Owner')
    tenant_id = fields.Many2one("res.partner", string="Tenant")
    start_date = fields.Date(string="Date")
    end_date = fields.Date(string="To date")
    property_id = fields.Many2one('property.property', string="Property")
    type = fields.Selection(selection=[('rent', 'Rent'), ('lease', 'Lease')])
    status = fields.Selection(
        selection=[('draft', 'Draft'), ('to_approve', 'To Approve'), ('confirm', 'Confirmed'),
                   ('closed', 'Closed'), ('returned', 'Returned'), ('expired', 'Expired')]
    )

    def action_print_report(self):
        """Print PDF report"""
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError("Start date should be should less than End date")
        query = """
                   SELECT
                       prop_rent.name AS rental_name,
                       prop.name AS property_name,
                       owner.name AS owner_name,
                       prop_rent.type,
                       tenant.name AS tenant_name,
                       prop_rent.start_date,
                       prop_rent.end_date,
                       prop.rent AS rent_amount,
                       prop_rent.status
                   FROM property_rental prop_rent                   
                   JOIN property_line prop_line ON prop_line.property_inverse_id = prop_rent.id
                   JOIN property_property prop ON prop_line.property_id = prop.id
                   LEFT JOIN res_partner owner ON prop.owner_id = owner.id
                   LEFT JOIN res_partner tenant ON prop_rent.tenant_id = tenant.id
                   WHERE TRUE
               """
        params = []
        if self.start_date and self.end_date:
            query += " AND prop_rent.start_date >= %s AND prop_rent.end_date <= %s"
            params.extend([self.start_date, self.end_date])
        elif self.start_date:
            query += " AND prop_rent.start_date >= %s"
            params.append(self.start_date)
        elif self.end_date:
            query += " AND prop_rent.end_date <= %s"
            params.append(self.end_date)
        if self.status:
            query += " AND prop_rent.status = %s"
            params.append(self.status)
        if self.type:
            query += " AND prop_rent.type = %s"
            params.append(self.type)
        if self.tenant_id:
            query += " AND prop_rent.tenant_id = %s"
            params.append(self.tenant_id.id)
        if self.owner_id:
            query += " AND prop.owner_id = %s"
            params.append(self.owner_id.id)
        if self.property_id:
            query += " AND prop_line.property_id = %s"
            params.append(self.property_id.id)
        self.env.cr.execute(query, params)
        result = self.env.cr.dictfetchall()
        status_dict = dict(self.env['property.rental']._fields['status'].selection)
        type_dict = dict(self.env['property.rental']._fields['type'].selection)
        for line in result:
            line['status_label'] = status_dict.get(line['status'], line['status'])
            line['type_label'] = type_dict.get(line['type'], line['type'])
        if not result:
            raise ValidationError("No data found for the selected filters.")
        return self.env.ref('property.action_rent_report').report_action(
            self, data={'report_data':
                            {'rental_data': result,
                             'filters': {
                                 'start_date': self.start_date,
                                 'end_date': self.end_date,
                                 'property': self.property_id.name if self.property_id else '',
                                 'tenant': self.tenant_id.name if self.tenant_id else '',
                                 'owner': self.owner_id.name if self.owner_id else '',
                                 'type': self.type if self.type else '',
                             }
                             }})

    def action_print_excel(self):
        """to generate xlsx file report"""
        # report_data=action_print_report()
        data = {
            'start_date': self.start_date,
            'end_date': self.end_date,
            'property': self.property_id.name,
            'tenant': self.tenant_id.name,
            'owner': self.owner_id.name,
            'type': self.type
        }
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'sale.order',
                     'options': json.dumps(data,
                                           default=json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Rent Excel Report',
                     },
            'report_type': 'xlsx'
        }

    def get_xlsx_report(self, data, response):
        """Excel report"""
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format(
            {'font_size': '12px', 'align': 'center'})
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format({'font_size': '10px', 'align': 'center'})
        sheet.merge_range('B2:I3', 'Rent/Lease Report', head)
        sheet.merge_range('A4:B4', 'Property:', cell_format)
        sheet.merge_range('C4:D4', data['property'], txt)
        sheet.merge_range('A5:B5', 'property', cell_format)
        # for i, property in enumerate(data['property'],start=5):  # Start at row 6 for products
        #     sheet.merge_range(f'C{i}:D{i}', property, txt)
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()