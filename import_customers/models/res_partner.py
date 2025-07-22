# -*- coding: utf-8 -*-
"""sale order model"""
from odoo import models


class ResPartner(models.Model):
    """class for Invoice in property """
    _inherit = 'res.partner'
    _description = 'res partner'

    def action_import(self):
        print('hello')