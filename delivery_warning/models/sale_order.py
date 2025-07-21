# -*- coding: utf-8 -*-
from odoo import models, fields


class SaleOrder(models.Model):
    """class for Invoice in property """
    _inherit = ['sale.order']
    _description = 'Sale order'

    delivery_warning = fields.Boolean(default=False, string='Delivery Warning')
