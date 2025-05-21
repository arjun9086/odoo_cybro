# -*- coding: utf-8 -*-
"""utf8"""
from odoo import models, fields


class SaleOrder(models.Model):
    """class for Invoice in property """
    _inherit = 'sale.order'
    _description = 'Sale order'

def action_upload():
    print("upload")