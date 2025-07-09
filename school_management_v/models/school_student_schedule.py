# -*- coding: utf-8 -*-
from odoo import models, fields

class StudentSchedule(models.Model):
    _name = 'school.student.schedule'
    _description = 'Horario del Estudiante'

    enrollment_id = fields.Many2one('school.enrollment', string="Inscripción", required=True, ondelete='cascade')
    student_id = fields.Many2one(related='enrollment_id.student_id', store=True, readonly=True)
    subject_id = fields.Many2one(related='enrollment_id.subject_id', store=True, readonly=True)
    teacher_id = fields.Many2one(related='enrollment_id.teacher_id', store=True, readonly=True)
    day_of_week = fields.Selection(related='enrollment_id.schedule_id.day_of_week', store=True, readonly=True)
    start_time = fields.Float(related='enrollment_id.schedule_id.start_time', store=True, readonly=True)
    end_time = fields.Float(related='enrollment_id.schedule_id.end_time', store=True, readonly=True)