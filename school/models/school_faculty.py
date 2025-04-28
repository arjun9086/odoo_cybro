from odoo import fields,models

class schooll_faculty(models.Model):
    _name='school.faculty'
    _description = 'These are the faculty section'

    name=fields.Char(string="Name")
    class_=fields.Many2many("school.class",string="Class Assigned")
    subject_ids=fields.Many2many("school.subject",string='Subject')
    phone=fields.Char()
    address=fields.Char(string="Address")
    department=fields.Many2one("school.department",string="Department")
