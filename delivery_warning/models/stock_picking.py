# -*- coding: utf-8 -*-
"""Delivery warning"""
from odoo import models, fields, api


class StockPicking(models.Model):
    """class for Stock picking """
    _inherit = 'stock.picking'
    _description = 'Stock Picking/Delivery'
    sale_id = fields.Many2one('sale.order', compute='_compute_sale_id', store=True)
    delivery_warning = fields.Boolean(readonly=True, compute='_get_delivery_warning_status')

    def _compute_sale_id(self):
        for picking in self:
            sale = self.env['sale.order'].search([('name', '=', picking.origin)], limit=1)
            picking.sale_id = sale

    def _get_delivery_warning_status(self):
        for picking in self:
            picking.delivery_warning = picking.sale_id.delivery_warning if picking.sale_id else False
