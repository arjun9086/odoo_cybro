# -*- coding: utf-8 -*-
"""importing xls file to sale order line """
import base64
from io import BytesIO
import openpyxl
from odoo import fields, models


class ImportFileWiz(models.TransientModel):
    """wizard model"""
    _name = "import.file.wiz"
    _description = "Import file Wizard"

    import_file = fields.Binary(string='Add file')
    filename = fields.Char('Filename')

    def import_sol(self):
        """  Import xlsx report to saleOrder line """
        wb = openpyxl.load_workbook(
            filename=BytesIO(base64.b64decode(self.import_file)),
            read_only=True)
        ws = wb.active
        for record in ws.iter_rows(min_row=2, values_only=True):
            product_name = record[0]
            qty = record[1]
            uom = record[2]
            description = record[3]
            price = record[4]
            order_id = self.env.context.get('order_id')
            product = self.env['product.product'].search([('name', '=', product_name)])
            if not product:
                product = self.env['product.product'].create([{
                    'name': product_name,
                    'description': description,
                    'list_price': price,
                }])
            self.env['sale.order.line'].create([{
                'product_id': product.id,
                'name': description or product.name,
                'product_uom_qty': qty,
                'product_uom': self.env['uom.uom'].search([('name', '=', uom)]).id,
                'price_unit': price,
                'order_id': order_id,
            }])
