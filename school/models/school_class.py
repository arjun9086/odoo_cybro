from odoo import fields,models

class class__(models.Model):
    _name='school.class'
    _description = 'These are the class section'


    name=fields.Char(string="class")
    class_teacher=fields.Many2one("school.faculty",string="Class teacher")
    subject=fields.Many2many("school.subject",string="Subjects")
    student=fields.Many2many("school.student")
    # student=fields.Many2one(string='Students',related="student1.class_")