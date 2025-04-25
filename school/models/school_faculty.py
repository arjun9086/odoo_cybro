from odoo import fields,models

class schooll_faculty(models.Model):
    _name='school.faculty'
    _description = 'These are the faculty section'

    name=fields.Char()