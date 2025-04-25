
from odoo import fields,models

class student(models.Model):
    _name="school.student"
    _description = "Datas of students"

    name=fields.Char()
    class_=fields.Integer(string='Class')
    admission_no=fields.Integer()
    guardian=fields.Char()
    class_teacher=fields.Char()
    phone_no=fields.Char()
    age=fields.Integer()
    address=fields.Char()