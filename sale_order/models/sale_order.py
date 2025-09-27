# -*- coding: utf-8 -*-
from odoo import models


class SaleOrder(models.Model):
    """class for Invoice in property """
    _inherit = ['sale.order']
    _description = 'Sale order'

    def action_upload(self):
        """uploading file"""
        # print(self.name)
        return {'type': 'ir.actions.act_window',
                'name': 'Import file',
                'res_model': 'import.file.wiz',
                'target': 'new',
                'view_mode': 'form',
                'context': {'order_id': self.id}
                }
