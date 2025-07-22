# -*- coding: utf-8 -*-
"""importing xls file to sale order line """
import base64
from io import BytesIO
import openpyxl
from odoo import fields, models


class CustomerImport(models.TransientModel):
    """customer import wizard model"""
    _name = "customer.import"
    _description = "Customer Import Wizard"
    user_name = fields.Char('Username')
