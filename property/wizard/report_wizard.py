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

    def query_result(self, data):
        """fetching data from db"""
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
        if data.get('start_date'):
            query += " AND prop_rent.start_date >= %s"
            params.append(data['start_date'])
        if data.get('end_date'):
            query += " AND prop_rent.end_date <= %s"
            params.append(data['end_date'])
        if data.get('type'):
            query += " AND prop_rent.type = %s"
            params.append(data['type'])
        if data.get('status'):
            query += " AND prop_rent.status = %s"
            params.append(data['status'])
        if data.get('tenant_id'):
            query += " AND prop_rent.tenant_id = %s"
            params.append(data['tenant_id'])
        if data.get('owner_id'):
            query += " AND prop.owner_id = %s"
            params.append(data['owner_id'])
        if data.get('property_id'):
            query += " AND prop.id = %s"
            params.append(data['property_id'])
        self.env.cr.execute(query, params)
        return self.env.cr.dictfetchall()

    def action_print_report(self):
        """To print Pdf report"""
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError("Start date should be less than End date")
        data = {
            'start_date': self.start_date,
            'end_date': self.end_date,
            'property_id': self.property_id.id if self.property_id else None,
            'tenant_id': self.tenant_id.id if self.tenant_id else None,
            'owner_id': self.owner_id.id if self.owner_id else None,
            'type': self.type,
            'status': self.status,
        }
        result = self.query_result(data)
        if not result:
            raise ValidationError("No data found for the selected filters.")
        status_dict = dict(self.env['property.rental']._fields['status'].selection)
        type_dict = dict(self.env['property.rental']._fields['type'].selection)
        for line in result:
            line['status_label'] = status_dict.get(line['status'], line['status'])
            line['type_label'] = type_dict.get(line['type'], line['type'])
        display_filters = {
            'start_date': self.start_date,
            'end_date': self.end_date,
            'property': self.property_id.name if self.property_id else '',
            'tenant': self.tenant_id.name if self.tenant_id else '',
            'owner': self.owner_id.name if self.owner_id else '',
            'type': type_dict.get(self.type, '') if self.type else '',
            'status': status_dict.get(self.status, '') if self.status else '',
        }
        return self.env.ref('property.action_rent_report').report_action(
            self, data={'report_data': {
                'rental_data': result,
                'filters': display_filters
            }}
        )

    def action_print_excel(self):
        """To print Excel report"""
        data = {
            'start_date': self.start_date or '',
            'end_date': self.end_date or '',
            'property': self.property_id.name if self.property_id else '',
            'property_id': self.property_id.id if self.property_id else None,
            'tenant': self.tenant_id.name if self.tenant_id else '',
            'tenant_id': self.tenant_id.id if self.tenant_id else None,
            'owner': self.owner_id.name if self.owner_id else '',
            'owner_id': self.owner_id.id if self.owner_id else None,
            'type': self.type or '',
            'status': self.status or '',
        }
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
        }

    def get_xlsx_report(self, data, response):
        """Excel sheet customising"""
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet("Rent Report")
        header_format = workbook.add_format({'bold': True})
        text_format = workbook.add_format({'font_size': 9})
        label_format = workbook.add_format({'bold': True, 'font_size': 10})
        # Header
        logo = self.env.company.logo
        logo_image = io.BytesIO(base64.b64decode(logo))
        sheet.merge_range('Q1:S3', ' ')
        sheet.insert_image('Q1', 'logo.png', {'image_data': logo_image, 'x_scale': 0.4, 'y_scale': 0.4})
        company = self.env.company
        sheet.merge_range('Q4:S4', company.name or '', text_format)
        sheet.merge_range('Q5:S5', company.street or '', text_format)
        sheet.merge_range('Q6:S6', f"{company.city or ''} {company.zip or ''}, {company.state_id.name or ''}",
                          text_format)
        sheet.merge_range('A8:S8', 'Rent/Lease Report',
                          workbook.add_format({'bold': True, 'align': 'center', 'font_size': 14}))
        status_dict = dict(self.env['property.rental']._fields['status'].selection)
        type_dict = dict(self.env['property.rental']._fields['type'].selection)
        filters = []
        if data.get('start_date'):
            filters.append(("Start Date", data['start_date']))
        if data.get('end_date'):
            filters.append(("End Date", data['end_date']))
        if data.get('property'):
            filters.append(("Property", data['property']))
        if data.get('tenant'):
            filters.append(("Tenant", data['tenant']))
        if data.get('owner'):
            filters.append(("Owner", data['owner']))
        if data.get('type'):
            filters.append(("Type", type_dict.get(data['type'], data['type'])))
        if data.get('status'):
            filters.append(("Status", status_dict.get(data['status'], data['status'])))
        row = 9
        for i in range(0, len(filters), 2):
            left = filters[i]
            right = filters[i + 1] if i + 1 < len(filters) else None
            sheet.write(row, 0, f"{left[0]}:", label_format)
            sheet.merge_range(row, 1, row, 2, str(left[1]), text_format)
            if right:
                sheet.write(row, 5, f"{right[0]}:", label_format)
                sheet.merge_range(row, 6, row, 7, str(right[1]), text_format)
            row += 1
        row += 1
        headers = ['Rental order', 'Property', 'Owner', 'Type', 'Tenant', 'Start Date', 'End Date', 'Rent', 'Status']
        col = 0
        for h in headers:
            sheet.merge_range(row, col, row, col + 1, h, header_format)
            col += 2
        row += 1
        result = self.query_result(data)
        for rec in result:
            sheet.merge_range(row, 0, row, 1, rec['rental_name'], text_format)
            sheet.merge_range(row, 2, row, 3, rec['property_name'], text_format)
            sheet.merge_range(row, 4, row, 5, rec['owner_name'], text_format)
            sheet.merge_range(row, 6, row, 7, type_dict.get(rec['type'], rec['type']), text_format)
            sheet.merge_range(row, 8, row, 9, rec['tenant_name'], text_format)
            sheet.merge_range(row, 10, row, 11, str(rec['start_date']), text_format)
            sheet.merge_range(row, 12, row, 13, str(rec['end_date']), text_format)
            sheet.merge_range(row, 14, row, 15, rec['rent_amount'], text_format)
            sheet.merge_range(row, 16, row, 17, status_dict.get(rec['status'], rec['status']), text_format)
            row += 1
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
