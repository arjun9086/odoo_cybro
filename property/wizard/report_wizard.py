# -*- coding: utf-8 -*-
from odoo import models, fields
from odoo.exceptions import ValidationError


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

    def action_print_report(self):
        """Print PDF report"""
        # if not self.start_date or not self.end_date:
        #     raise ValidationError("From Date and To Date are required.")
        query = """
                   SELECT
                       prop_rent.name AS rental_name,
                       rp.name AS property_name,
                       owner.name AS owner_name,
                       prop_rent.type,
                       tenant.name AS tenant_name,
                       prop_rent.start_date,
                       prop_rent.end_date,
                       rp.rent AS rent_amount,
                       prop_rent.status
                   FROM property_rental prop_rent                   
                   JOIN property_line prop_line ON prop_line.property_inverse_id = prop_rent.id
                   JOIN property_property rp ON prop_line.property_id = rp.id
                   LEFT JOIN res_partner owner ON rp.owner_id = owner.id
                   LEFT JOIN res_partner tenant ON prop_rent.tenant_id = tenant.id
                   WHERE prop_rent.start_date >= %s AND prop_rent.end_date <= %s
               """
        params = [self.start_date, self.end_date]
        self.env.cr.execute(query, params)
        result = self.env.cr.dictfetchall()
        if not result:
            raise ValidationError("No data found for the selected filters.")
        return self.env.ref('property.action_rent_report').report_action(
            self, data={'report_data': {'rental_data': result}}
        )
