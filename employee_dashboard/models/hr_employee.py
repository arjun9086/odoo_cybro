# -*- coding: utf-8 -*-
"""hr employee model"""
from datetime import date

from odoo import models, fields, api
from odoo.http import request


class HrEmployeeDashboard(models.AbstractModel):
    _name = 'hr.employee.dashboard'
    _description = 'hr employee dashboard model'

    @api.model
    def get_employee_dashboard_data(self):
        user = request.env.user
        employee = request.env['hr.employee'].sudo().search([('user_id', '=', user.id)], limit=1)
        attendance_records = request.env['hr.attendance'].sudo().search([
            ('employee_id', '=', employee.id)
        ])
        total_attendance = sum(attendance_records.mapped('worked_hours'))
        leave_records = request.env['hr.leave'].sudo().search([
            ('employee_id', '=', employee.id),
            ('state', '=', 'validate')
        ])
        total_leaves = sum(leave_records.mapped('number_of_days'))
        projects = request.env['project.project'].sudo().search([('user_id', '=', user.id)])
        project_names = projects.mapped('name')
        tasks = request.env['project.task'].sudo().search([
            ('user_ids', '=', user.id)])
        task_list = [{
            'name': t.name,
            'project': t.project_id.name,
            'deadline': t.date_deadline.strftime('%Y-%m-%d') if t.date_deadline else '',
            'stage': t.stage_id.name
        } for t in tasks]
        experience = []
        for line in employee.resume_line_ids.filtered(lambda l: l.line_type_id.name == "Experience"):
            experience.append({
                'line_type': line.line_type_id.name or '',
                'name': line.name or '',
                'description': line.description or '',
                'date_start': line.date_start.strftime('%Y-%m-%d') if line.date_start else '',
                'date_end': line.date_end.strftime('%Y-%m-%d') if line.date_end else '',
            })
        employees = request.env['hr.employee'].sudo().search([
            ('parent_id', '=', employee.id)
        ])
        is_manager = bool(employees)
        managed_employee_names = employees.mapped('name') if is_manager else []
        org_employee = {
            'id': employee.id,
            'name': employee.name,
            'job_title': employee.job_id.name if employee.job_id else '',
            'parent_id': employee.parent_id.id if employee.parent_id else None,
            'direct_sub_count': len(employee.child_ids),
            'indirect_sub_count': len(employee.child_ids)  # Adjust if you're calculating true indirects
        }
        org_managers = []
        if employee.parent_id:
            org_managers.append({
                'id': employee.parent_id.id,
                'name': employee.parent_id.name,
                'job_title': employee.parent_id.job_id.name if employee.parent_id.job_id else ''
            })
        org_children = [{
            'id': child.id,
            'name': child.name,
            'job_title': child.job_id.name if child.job_id else ''
        } for child in employee.child_ids]

        org_managers_more = False

        return {
            'employee_name': employee.name,
            'employee_email': employee.work_email or '',
            'employee_phone': employee.work_phone or '',
            # 'employee_image': employee.image_128.decode() if employee.image_128 else '',
            'total_attendance': round(total_attendance, 2),
            'total_leaves': round(total_leaves, 2),
            'total_projects': len(projects),
            'project_names': project_names,
            'tasks': task_list,
            'experience': experience,
            'is_manager': is_manager,
            'managed_employees': managed_employee_names,
            'org_employee': org_employee,
            'org_managers': org_managers,
            'org_children': org_children,
            'org_managers_more': org_managers_more,
        }