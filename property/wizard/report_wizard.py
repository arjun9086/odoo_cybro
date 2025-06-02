# -*- coding: utf-8 -*-
"""wizard form to print the pdf report """
import base64
import io
import json
import xlsxwriter
from odoo import models, fields
from odoo.exceptions import ValidationError
from odoo.tools import json_default


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

    # def query_result_from_data(self, data):
    #     query = """
    #         SELECT
    #             prop_rent.name AS rental_name,
    #             prop.name AS property_name,
    #             owner.name AS owner_name,
    #             prop_rent.type,
    #             tenant.name AS tenant_name,
    #             prop_rent.start_date,
    #             prop_rent.end_date,
    #             prop.rent AS rent_amount,
    #             prop_rent.status
    #         FROM property_rental prop_rent
    #         JOIN property_line prop_line ON prop_line.property_inverse_id = prop_rent.id
    #         JOIN property_property prop ON prop_line.property_id = prop.id
    #         LEFT JOIN res_partner owner ON prop.owner_id = owner.id
    #         LEFT JOIN res_partner tenant ON prop_rent.tenant_id = tenant.id
    #         WHERE TRUE
    #     """
    #     params = []
    #     if data.get('start_date'):
    #         query += " AND prop_rent.start_date >= %s"
    #         params.append(data['start_date'])
    #     if data.get('end_date'):
    #         query += " AND prop_rent.end_date <= %s"
    #         params.append(data['end_date'])
    #     if data.get('type'):
    #         query += " AND prop_rent.type = %s"
    #         params.append(data['type'])
    #     if data.get('tenant'):
    #         query += " AND tenant.name = %s"
    #         params.append(data['tenant'])
    #     if data.get('owner'):
    #         query += " AND owner.name = %s"
    #         params.append(data['owner'])
    #     if data.get('property'):
    #         query += " AND prop.name = %s"
    #         params.append(data['property'])
    #     self.env.cr.execute(query, params)
    #     return self.env.cr.dictfetchall()

    def action_print_report(self, return_data_only=False):
        """Print PDF report"""
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError("Start date should be should less than End date")
        # result = self.query_result()
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
        print('hi')
        if self.start_date and self.end_date:
            query += " AND prop_rent.start_date >= %s AND prop_rent.end_date <= %s"
            params.extend([self.start_date, self.end_date])
            print(self.start_date)
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
            print('hello')
            query += " AND prop_line.property_id = %s"
            params.append(self.property_id.id)
            print(self.property_id)
        self.env.cr.execute(query, params)
        result = self.env.cr.dictfetchall()
        status_dict = dict(self.env['property.rental']._fields['status'].selection)
        type_dict = dict(self.env['property.rental']._fields['type'].selection)
        for line in result:
            line['status_label'] = status_dict.get(line['status'], line['status'])
            line['type_label'] = type_dict.get(line['type'], line['type'])
        if not result:
            raise ValidationError("No data found for the selected filters.")
        if return_data_only:
            return result
        # print(result)
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
        """to print excell sheet"""
        data = ({
            'start_date': self.start_date or '',
            'end_date': self.end_date or '',
            'property': self.property_id.name if self.property_id else '',
            'tenant': self.tenant_id.name if self.tenant_id else '',
            'owner': self.owner_id.name if self.owner_id else '',
            'type': self.type if self.type else ''
        })
        return {
            'type': 'ir.actions.report',
            'data': {
                'model': 'report.wizard',
                'id': self.id,
                'options': json.dumps(data, default=json_default),
                'output_format': 'xlsx',
                'report_name': 'Rent Report',
            },
            'report_type': 'xlsx',
            'start_date': self.start_date or '',
            'end_date': self.end_date or '',
            'property': self.property_id.name if self.property_id else '',
            'tenant': self.tenant_id.name if self.tenant_id else '',
            'owner': self.owner_id.name if self.owner_id else '',
        }

    def get_xlsx_report(self, data, response):
        """Excel report"""
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet("Rent Report")
        header_format = workbook.add_format({'bold': True})
        text_format = workbook.add_format({'font_size': 10})
        # Header
        buf_image = io.BytesIO(base64.b64decode())
        sheet.insert_image('B3', "any_name.png", {'image_data': buf_image})
        sheet.merge_range('A1:I1', 'Rent/Lease Report',
                          workbook.add_format({'bold': True, 'align': 'center', 'font_size': 14}))
        # row = 2
        sheet.merge_range('A2:H2', self.env.company.name or '',
                          workbook.add_format({'align': 'left', 'font_size': 12}))
        row = 3
        # sheet.write(row, 0, "Filters", header_format)
        row += 1
        for key in ['start_date', 'end_date', 'property', 'tenant', 'owner', 'type']:
            sheet.write(row, 0, key.capitalize(), header_format)
            sheet.write(row, 1, str(data.get(key, '')), text_format)
            row += 1
        row += 1
        headers = ['Rental order', 'Property', 'Owner', 'Type', 'Tenant', 'Start Date', 'End Date', 'Rent', 'Status']
        for col, h in enumerate(headers):
            sheet.write(row, col, h, header_format)
        row += 1
        # result = self.query_result_from_data(data)
        result = self.action_print_report(return_data_only=True)
        for rec in result:
            sheet.write(row, 0, rec['rental_name'], text_format)
            sheet.write(row, 1, rec['property_name'], text_format)
            sheet.write(row, 2, rec['owner_name'], text_format)
            sheet.write(row, 3, rec['type'], text_format)
            sheet.write(row, 4, rec['tenant_name'], text_format)
            sheet.write(row, 5, str(rec['start_date']), text_format)
            sheet.write(row, 6, str(rec['end_date']), text_format)
            sheet.write(row, 7, rec['rent_amount'], text_format)
            sheet.write(row, 8, rec['status'], text_format)
            row += 1
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
