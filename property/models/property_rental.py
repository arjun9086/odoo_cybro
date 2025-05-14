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
    property_ids = fields.One2many('property.line', 'property_inverse_id', string="Property")
    tenant_id = fields.Many2one("res.partner", string="Tenant")
    start_date = fields.Date(string="Period")
    end_date = fields.Date(string="End date")
    status = fields.Selection(
        selection=[('draft', 'Draft'), ('confirm', 'Confirmed'), ('closed', 'Closed'), ('returned', 'Returned'),
                   ('expired', 'Expired')],
        string='Status',
        default='draft',
        tracking=True)
    remaining_days = fields.Float(string="Remaining days", compute='_compute_remaining_days', store=True)
    company_id = fields.Many2one('res.company')
    rental_count = fields.Integer(string="Invoice", compute="_compute_rental_count")

    @api.depends('end_date', 'start_date')
    def _compute_remaining_days(self):
        """remaining date"""
        for record in self:
            if record.end_date:
                record.remaining_days = max((record.end_date - record.start_date).days, 0)
            else:
                record.remaining_days = 0

    def _compute_rental_count(self):
        """smart button"""
        for record in self:
            record.rental_count = self.env['account.move'].search_count([("rental_id", "=", self.id)])

    @api.model_create_multi
    def create(self, vals_list):
        """Automatically generate a reference number for rental."""
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('property.rental')
                # print('vals=', vals_list)
        return super(PropertyRental, self).create(vals_list)

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

    def action_create_invoice(self):
        # """Invoice creation"""
        """Create or update invoice with correct remaining qty and link invoice lines"""
        accountmove = self.env['account.move']
        invoice_lines = []

        for line in self.property_ids:
            # posted invoice lines
            posted_lines = line.invoice_line_ids.filtered(lambda l: l.move_id.state == 'posted')
            invoiced_qty = sum(posted_lines.mapped('quantity'))
            remaining_qty = line.quantity_ - invoiced_qty
            print(f"Invoiced: {invoiced_qty}, Remaining: {remaining_qty}")
            if remaining_qty > 0:
                invoice_lines.append({
                    'name': line.property_id.name,
                    'quantity': remaining_qty,
                    'price_unit': line.rent,
                    'invoice_line': line  # link
                })

        if not invoice_lines:
            return

        draft_invoice = accountmove.search([
            ('rental_id', '=', self.id),
            ('state', '=', 'draft')
        ])
        # created_invoice_lines = []
        if draft_invoice:
            existing_names = set(draft_invoice.invoice_line_ids.mapped('name'))
            new_lines = []
            for vals in invoice_lines:
                if vals['name'] not in existing_names:
                    line_vals = {
                        'name': vals['name'],
                        'quantity': vals['quantity'],
                        'price_unit': vals['price_unit'],
                    }
                    new_lines.append((0, 0, line_vals))
            if new_lines:
                draft_invoice.write({'invoice_line_ids': new_lines})
            invoice = draft_invoice
        else:
            # Create new invoice
            new_invoice_lines = [
                (0, 0, {
                    'name': vals['name'],
                    'quantity': vals['quantity'],
                    'price_unit': vals['price_unit'],
                })
                for vals in invoice_lines
            ]
            invoice = accountmove.create({
                'move_type': 'out_invoice',
                'partner_id': self.tenant_id.id,
                'invoice_date': fields.Date.today(),
                'invoice_line_ids': new_invoice_lines,
                'rental_id': self.id
            })
        # link created invoice lines back to property lines
        for vals in invoice_lines:
            line = vals['invoice_line']
            inv_line = invoice.invoice_line_ids.filtered(lambda l: l.name == vals['name'])
            if inv_line:
                line.invoice_line_ids |= inv_line
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_confirm(self):
        """Confirm state"""
        if self.message_attachment_count >= 0:
            self.write({'status': 'confirm'})
        else:
            raise ValidationError("At least 1 file must be attached")

    def action_closed(self):
        """closed state"""
        self.write({'status': 'closed'})

    def action_returned(self):
        """returned state"""
        self.write({'status': 'returned'})

    def action_expire(self):
        """expire state"""
        self.write({'status': 'expired'})
