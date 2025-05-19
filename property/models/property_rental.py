# -*- coding: utf-8 -*-
"""utf8"""

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class PropertyRental(models.Model):
    """Rental or Lease Management"""
    _name = "property.rental"
    _description = "Rental or Lease Management"
    _inherit = ['mail.thread', 'mail.activity.mixin']

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
        """Invoice creation"""
        accountmove = self.env['account.move']
        invoice_lines = []
        # posted invoice
        for line in self.property_ids:
            posted_qty = sum(line.invoice_line_ids.filtered(lambda l: l.move_id.state == 'posted').mapped('quantity'))
            remaining_qty = line.quantity_ - posted_qty
            if remaining_qty > 0:
                invoice_lines.append({
                    'name': line.property_id.name,
                    'quantity': remaining_qty,
                    'price_unit': line.rent,
                })
        if not invoice_lines:
            return
        # draft invoice
        draft_invoice = accountmove.search([
            ('rental_id', '=', self.id),
            ('state', '=', 'draft')
        ])
        new_invoice_lines = [(0, 0, {
            'name': vals['name'],
            'quantity': vals['quantity'],
            'price_unit': vals['price_unit'],
        }) for vals in invoice_lines]
        if draft_invoice:
            draft_invoice.write({'invoice_line_ids': [(5, 0, 0)] + new_invoice_lines})
            invoice = draft_invoice
        else:
            # Create new invoice
            invoice = accountmove.create({
                'move_type': 'out_invoice',
                'partner_id': self.tenant_id.id,
                'invoice_date': fields.Date.today(),
                'invoice_line_ids': new_invoice_lines,
                'rental_id': self.id
            })
        # Link invoice lines to rental lines
        self.property_ids.link_invoice_lines(invoice)
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
            template = self.env.ref('property.tenant_mail')
            template.send_mail(self.id, force_send=True)
        else:
            raise ValidationError("At least 1 file must be attached")

    def action_closed(self):
        """closed state"""
        self.write({'status': 'closed'})
        template = self.env.ref('property.tenant_mail')
        template.send_mail(self.id, force_send=True)

    def action_returned(self):
        """returned state"""
        self.write({'status': 'returned'})

    def action_expire(self):
        """expire state"""
        self.write({'status': 'expired'})
        template = self.env.ref('property.tenant_mail')
        template.send_mail(self.id, force_send=True)

    def action_change_state(self):
        """change state"""
        record = self.search([('end_date', '<', fields.Date.today()), ('status', '!=', 'expired')])
        record.write({'status': 'expired'})

    def late_payment_mail(self):
        """late payment mail"""
        expired_rental = self.search([('status', '=', 'expired')])
        template = self.env.ref('property.late_payment_mail')
        for rental in expired_rental:
            invoices = self.env['account.move'].search([
                ('rental_id', '=', rental.id),
                ('state', '=', 'posted'),
                ('payment_state', '!=', 'paid')
            ])
            if invoices and template:
                template.send_mail(rental.id, force_send=True)
