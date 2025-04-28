from odoo import fields,models

class subject(models.Model):
    _name='school.subject'
    _description = 'These are the subject section'

    name=fields.Char(string="Subject")
