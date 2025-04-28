from tokenize import String

from odoo import fields,models
from odoo.tools.view_validation import READONLY


class student(models.Model):
    _name="school.student"
    _description = "Datas of students"

    name=fields.Char(required=True)
    class_=fields.Many2one("school.class",String="Class")
    admission_no=fields.Integer()
    guardian=fields.Char()
    guardian_phone=fields.Char()
    class_teacher_=fields.Many2one(string="Class teacher",related="class_.class_teacher")
    phone_no=fields.Char()
    age=fields.Integer()
    address=fields.Char()
    subject=fields.Many2many(string="Subjects",related="class_.subject")