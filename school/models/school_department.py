from odoo import fields,models

class department(models.Model):
    _name='school.department'
    _description = 'These are the department section'

    name=fields.Char(string="Department Name")