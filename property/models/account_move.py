# -*- coding: utf-8 -*-
"""utf8"""
from odoo import models, fields, api


class AccountMove(models.Model):
    """class for Invoice in property """
    _inherit = ['account.move']
    _description = 'Property Invoice'

    rental_id = fields.Many2one('property.rental', string="Rent id", readonly=True)


