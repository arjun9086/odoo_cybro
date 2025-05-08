
# -*- coding: utf-8 -*-
"""utf8"""

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class PropertyRental(models.Model):
    """Rental or Lease Management"""
    _name = "property.rental"
    _description = "Rental or Lease Management"
    _inherit = ['mail.thread']

    name = fields.Char(string="Sequence number", default=lambda self: 'New', readonly=True)
    type = fields.Selection(selection=[('rent', 'Rent'), ('lease', 'Lease')])
    property_ids = fields.Many2many('property.property', string="Property",
                                   required=True)
    tenant_id = fields.Many2one("res.partner", string="Tenant")
    amount = fields.Integer(string="Amount")
    start_date = fields.Date(string="Period")
    end_date = fields.Date(string="End date")
    total_amount = fields.Integer(string="Total Amount", related="property_ids.legal_amount")
    status = fields.Selection(
        selection=[('draft', 'Draft'), ('confirm', 'Confirmed'), ('closed', 'Closed'), ('returned', 'Returned'),
                   ('expired', 'Expired')],
        string='Status',
        default='draft',
        tracking=True)
    remaining_days = fields.Char(string="Remaining days", compute='_compute_remaining_days', store=True)
    company_id = fields.Many2one('res.company')
    # invoice_ids = fields.Many2one('account.move')
    rental_count = fields.Integer(string="Invoice", compute="compute_rental_count")

    def compute_rental_count(self):
        """smart button"""
        for record in self:
            record.rental_count = self.env['account.move'].search_count([("rental_id", "=", self.id)])

    def action_get_invoice_record(self):
        """smart button config"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'view_mode': 'list,form',
            'res_model': 'account.move',
            'domain': [('rental_id', '=', self.id)],
            'context': {'create': False}
        }

    # def invoice_form(self):
    #     """Invoice creation"""
    #     # AccountMove = self.env['account.move']
        # existing_invoice = AccountMove.search([
        #     ('rental_id', '=', self.id),
        #     ('state', '=', 'draft')
        # ], limit=1)
        #
        # invoice_lines = []
        # for property in self.property_ids:
        #     line = {
        #         'name': property.name,
        #         'quantity': 1,
        #         'price_unit': property.rent,
        #     }
        #     invoice_lines.append((0, 0, line))
        #
        # if existing_invoice:
        #     # Overwrite existing lines to match rental record
        #     existing_invoice.invoice_line_ids.unlink()  # Clear existing lines
        #     existing_invoice.write({'invoice_line_ids': invoice_lines})
        #     invoice = existing_invoice
        # else:
        #     # Create new invoice
        #     invoice = AccountMove.create({
        #         'move_type': 'out_invoice',
        #         'partner_id': self.tenant_id.id,
        #         'invoice_date': fields.Date.today(),
        #         'invoice_line_ids': invoice_lines,
        #         'rental_id': self.id
        #     })
        #
        # return {
        #     'type': 'ir.actions.act_window',
        #     'name': 'Invoice',
        #     'res_model': 'account.move',
        #     'res_id': invoice.id,
        #     'view_mode': 'form',
        #     'target': 'current',
        # }

    def invoice_form(self):
        """Create or reuse a draft invoice with uninvoiced properties only"""
        AccountMove = self.env['account.move']
        AccountMoveLine = self.env['account.move.line']

        # Step 1: Get all product_ids (properties) already invoiced in POSTED invoices
        posted_invoices = AccountMove.search([
            ('rental_id', '=', self.id),
            ('state', '=', 'posted')
        ])
        invoiced_property_names = posted_invoices.mapped('invoice_line_ids.name')

        # Step 2: Filter rental properties not yet invoiced
        uninvoiced_properties = self.property_ids.filtered(
            lambda prop: prop.name not in invoiced_property_names
        )

        if not uninvoiced_properties:
            raise UserError("All rental properties have already been invoiced.")

        # Step 3: Prepare invoice lines only for uninvoiced properties
        invoice_lines = []
        for property in uninvoiced_properties:
            line = {
                'name': property.name,
                'quantity': 1,
                'price_unit': property.rent,
            }
            invoice_lines.append((0, 0, line))

        # Step 4: Check for existing draft invoice
        draft_invoice = AccountMove.search([
            ('rental_id', '=', self.id),
            ('state', '=', 'draft')
        ], limit=1)

        if draft_invoice:
            # Only add new lines for uninvoiced properties
            existing_names = draft_invoice.mapped('invoice_line_ids.name')
            new_lines = [
                line for line in invoice_lines if line[2]['name'] not in existing_names
            ]
            if new_lines:
                draft_invoice.write({'invoice_line_ids': new_lines})
            invoice = draft_invoice
        else:
            # Create new invoice
            invoice = AccountMove.create({
                'move_type': 'out_invoice',
                'partner_id': self.tenant_id.id,
                'invoice_date': fields.Date.today(),
                'invoice_line_ids': invoice_lines,
                'rental_id': self.id
            })

        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'view_mode': 'form',
            'target': 'current',
        }

    @api.model_create_multi
    def create(self, vals_list):
        """Automatically generate a reference number for rental."""
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('property.rental')
        return super(PropertyRental, self).create(vals_list)

    @api.depends('end_date', 'start_date')
    def _compute_remaining_days(self):
        """remaining date"""
        for record in self:
            if record.end_date and record.start_date:
                record.remaining_days = record.end_date - record.start_date
            else:
                record.remaining_days = 0

    def confirm(self):
        """Confirm state"""
        if self.message_attachment_count == 0:
            self.write({'status': 'confirm'})
        else:
            raise ValidationError("At least 1 file must be attached")

    def closed(self):
        """closed state"""
        self.write({'status': 'closed'})

    def returned(self):
        """returned state"""
        self.write({'status': 'returned'})

    def expire(self):
        """expire state"""
        self.write({'status': 'expired'})
