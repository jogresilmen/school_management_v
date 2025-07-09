# -*- coding: utf-8 -*-
from odoo import models, fields, api

class SubjectSchedule(models.Model):
    _name = 'school.subject.schedule'
    _description = 'Horario de Materia'
    _rec_name = 'display_name'

    subject_id = fields.Many2one('school.subject', string="Materia", required=True, ondelete='cascade')
    teacher_id = fields.Many2one(
        'res.partner',
        string="Profesor",
        required=True,
        domain="[('is_teacher', '=', True)]"
    )
    day_of_week = fields.Selection([
        ('monday', 'Lunes'),
        ('tuesday', 'Martes'),
        ('wednesday', 'Miércoles'),
        ('thursday', 'Jueves'),
        ('friday', 'Viernes'),
        ('saturday', 'Sábado'),
    ], string="Día de la Semana", required=True)
    start_time = fields.Float(string="Hora de Inicio", required=True)
    end_time = fields.Float(string="Hora de Fin", required=True)

    display_name = fields.Char(string="Descripción", compute='_compute_display_name', store=True)

    @api.depends('subject_id.name', 'teacher_id.name', 'day_of_week', 'start_time', 'end_time')
    def _compute_display_name(self):
        for rec in self:
            day_str = dict(self._fields['day_of_week'].selection).get(rec.day_of_week)
            rec.display_name = f"{rec.subject_id.name} - {rec.teacher_id.name} ({day_str} {rec.start_time:05.2f}-{rec.end_time:05.2f})".replace('.', ':')