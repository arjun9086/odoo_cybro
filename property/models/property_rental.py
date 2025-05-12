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
    # amount = fields.Integer(string="Amount")
    start_date = fields.Date(string="Period")
    end_date = fields.Date(string="End date")
    status = fields.Selection(
        selection=[('draft', 'Draft'), ('confirm', 'Confirmed'), ('closed', 'Closed'), ('returned', 'Returned'),
                   ('expired', 'Expired')],
        string='Status',
        default='draft',
        tracking=True)
    remaining_days = fields.Char(string="Remaining days", compute='_compute_remaining_days', store=True)
    company_id = fields.Many2one('res.company')
    rental_count = fields.Integer(string="Invoice", compute="_compute_rental_count")

    @api.depends('end_date', 'start_date')
    def _compute_remaining_days(self):
        """remaining date"""
        for record in self:
            if record.end_date and record.start_date:
                record.remaining_days = record.end_date - record.start_date
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
        # invoiced quantities
        posted_invoices = accountmove.search([
            ('rental_id', '=', self.id),
            ('state', '=', 'posted')
        ])
        property_qty_map = {}
        for inv in posted_invoices:
            for line in inv.invoice_line_ids:
                property = self.property_ids.filtered(lambda p: p.property_id.name == line.name)
                if property:
                    property = property[0]
                    property_qty_map.setdefault(property.id, 0)
                    property_qty_map[property.id] += line.quantity
        # remaining lines
        invoice_lines = []
        for property in self.property_ids:
            invoiced_qty = property_qty_map.get(property.id, 0)
            property.invoiced_qty = invoiced_qty
            remaining_qty = property.quantity_ - invoiced_qty

            if remaining_qty > 0:
                invoice_lines.append((0, 0, {
                    'name': property.property_id.name,
                    'quantity': remaining_qty,
                    'price_unit': property.rent,
                }))
        # existing draft invoice
        draft_invoice = accountmove.search([
            ('rental_id', '=', self.id),
            ('state', '=', 'draft')
        ])
        if draft_invoice:
            existing_names = draft_invoice.mapped('invoice_line_ids.name')
            new_lines = [
                line for line in invoice_lines if line[2]['name'] not in existing_names
            ]
            if new_lines:
                draft_invoice.write({'invoice_line_ids': new_lines})
            invoice = draft_invoice
        else:
            #  create invoice if empty
            invoice = accountmove.create({
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
