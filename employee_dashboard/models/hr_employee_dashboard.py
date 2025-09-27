# -*- coding: utf-8 -*-
"""hr employee model"""

from odoo import models, api
from odoo.http import request
from datetime import datetime


class HrEmployeeDashboard(models.Model):
    _name = 'hr.employee.dashboard'
    _description = 'hr employee dashboard model'

    @api.model
    def get_employee_dashboard_data(self, start_date=None, end_date=None):
        """getting data for employee dashboard"""
        user = request.env.user
        employee = request.env['hr.employee'].sudo().search([('user_id', '=', user.id)], limit=1)
        if not employee:
            return {}
        # Parse dates
        start = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
        end = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None

        def get_managers_chain(emp):
            """Manager chain"""
            chain = []
            while emp.parent_id:
                emp = emp.parent_id
                chain.append({
                    'id': emp.id,
                    'name': emp.name,
                    'job_title': emp.job_id.name if emp.job_id else ''
                })
            return chain

        def get_all_subordinates(emp):
            """full subordinates"""
            result = []
            for child in emp.child_ids:
                child_data = {
                    'id': child.id,
                    'name': child.name,
                    'job_title': child.job_id.name if child.job_id else '',
                    'children': get_all_subordinates(child)
                }
                result.append(child_data)
            return result

        def get_peers(emp):
            """siblings"""
            if not emp.parent_id:
                return []
            return [{
                'id': e.id,
                'name': e.name,
                'job_title': e.job_id.name if e.job_id else ''
            } for e in emp.parent_id.child_ids if e.id != emp.id]

        def get_subtree(emp):
            return {
                'id': emp.id,
                'name': emp.name,
                'children': [get_subtree(e) for e in emp.child_ids],
            }

        is_admin = not employee.parent_id
        org_managers = list(reversed(get_managers_chain(employee)))
        org_peers = get_peers(employee.parent_id) if employee.parent_id else []
        org_children = get_all_subordinates(employee) if is_admin else [{
            'id': child.id,
            'name': child.name,
            'job_title': child.job_id.name if child.job_id else ''
        } for child in employee.child_ids]
        org_employee = {
            'id': employee.id,
            'name': employee.name,
            'job_title': employee.job_id.name if employee.job_id else '',
            'parent_id': employee.parent_id.id if employee.parent_id else None,
            'direct_sub_count': len(employee.child_ids),
            'indirect_sub_count': len(employee.child_ids)
        }
        # Apply date filters
        att_domain = [('employee_id', '=', employee.id)]
        leave_domain = [('employee_id', '=', employee.id), ('state', '=', 'validate')]
        task_domain = [('user_ids', '=', user.id)]
        if start:
            att_domain.append(('check_in', '>=', start))
            leave_domain.append(('request_date_from', '>=', start))
            task_domain.append(('date_deadline', '>=', start))
        if end:
            att_domain.append(('check_out', '<=', end))
            leave_domain.append(('request_date_to', '<=', end))
            task_domain.append(('date_deadline', '<=', end))
        # Fetch and return data
        attendance = request.env['hr.attendance'].sudo().search(att_domain)
        leaves = request.env['hr.leave'].sudo().search(leave_domain)
        tasks = request.env['project.task'].sudo().search(task_domain)
        return {
            'employee_name': employee.name,
            'employee_email': employee.work_email or '',
            'employee_phone': employee.work_phone or '',
            'employee_image': employee.image_128.decode() if employee.image_128 else '',
            'total_attendance': round(sum(attendance.mapped('worked_hours')), 2),
            'total_leaves': round(sum(leaves.mapped('number_of_days')), 2),
            'total_projects': len(request.env['project.project'].sudo().search([('user_id', '=', user.id)])),
            'project_names': request.env['project.project'].sudo().search([('user_id', '=', user.id)]).mapped('name'),
            'tasks': [{
                'id': t.id,
                'name': t.name,
                'project': t.project_id.name,
                'deadline': t.date_deadline.strftime('%Y-%m-%d') if t.date_deadline else '',
                'stage': t.stage_id.name
            } for t in tasks],
            'experience': [{
                'line_type': line.line_type_id.name or '',
                'name': line.name or '',
                'description': line.description or '',
                'date_start': line.date_start.strftime('%Y-%m-%d') if line.date_start else '',
                'date_end': line.date_end.strftime('%Y-%m-%d') if line.date_end else '',
            } for line in employee.resume_line_ids.filtered(lambda l: l.line_type_id.name == "Experience")],
            'is_manager': bool(employee.child_ids),
            'managed_employees': employee.child_ids.mapped('name'),
            'org_employee': {
                'id': employee.id,
                'name': employee.name,
                'children': get_all_subordinates(employee) if employee else []
            },
            # 'org_employee': org_employee,
            'org_managers': org_managers + org_peers if not is_admin else [],
            'org_children': org_children,
        }
