from odoo import fields,models

class school_office_staff(models.Model):
    _name='office.staff'
    _description = 'These are the faculty office staff section section'

    name=fields.Char(string="Name")
    department=fields.Many2one("school.department",string="Department")
    phone=fields.Char()
    address=fields.Char()