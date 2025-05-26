# -*- coding: utf-8 -*-
from odoo import models, fields


class ReportWizard(models.TransientModel):
    """wizard model"""
    _name = "report.wizard"
    _description = "File wizard"

    # property_ids = fields.Many2many('property.line')
    owner_id = fields.Many2one('res.partner', string='Owner')
    tenant_id = fields.Many2one("res.partner", string="Tenant")
    start_date = fields.Date(string="Date")
    end_date = fields.Date(string="To date")
    property_id = fields.Many2one('property.property', string="Property")
    type = fields.Selection(selection=[('rent', 'Rent'), ('lease', 'Lease')])

    def action_print_report(self):
        # """to print report"""
        # rental = self.env['property.rental'].search([
        #     ('start_date', '>=', self.start_date),
        #     ('end_date', '<=', self.end_date)
        # ])
        # self.env.cr.execute("SELECT start_date FROM property_rental", (1,))
        # date = self.env.cr.fetchone()
        # print(date)
        # print(rental)
        # return self.env.ref('property.action_rent_report').report_action(rental)
        """Generate report using SQL filters from the wizard"""
        query = """
            SELECT 
                pr.id AS name,
                pr.start_date,
                pr.end_date,
                prop.name AS property_name,
                own.name AS owner_name,
                ten.name AS tenant_name,
                line.quantity_ AS quantity,
                line.rent AS rent_amount,
                line.state
            FROM property_rental pr
            JOIN property_rental line ON line.name = pr.id
            JOIN property_property prop ON line.property_id = prop.id
            LEFT JOIN res_partner own ON prop.owner_id = own.id
            LEFT JOIN res_partner ten ON line.tenant_id = ten.id
            WHERE pr.start_date >= %s AND pr.end_date <= %s
        """

        params = [self.start_date, self.end_date]

        if self.property_id:
            query += " AND line.property_id = %s"
            params.append(self.property_id.id)

        self.env.cr.execute(query, tuple(params))
        result = self.env.cr.dictfetchall()

        # Store result in context to pass to the report
        return self.env.ref('property.action_rent_report').report_action(
            self,
            data={'rental_data': result}
        )
