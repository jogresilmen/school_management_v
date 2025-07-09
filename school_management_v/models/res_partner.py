# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_student = fields.Boolean(string="Es Estudiante")
    is_teacher = fields.Boolean(string="Es Profesor")

    # Relación Many2many para indicar qué materias puede impartir un profesor.
    teach_subject_ids = fields.Many2many(
        'school.subject',
        'subject_teacher_rel',
        'teacher_id',
        'subject_id',
        string="Materias que Imparte",
        # The domain was incorrect as it was trying to filter 'school.subject' records
        # with a field ('is_teacher') that only exists on 'res.partner'.
    )

    # Campo computado para mostrar las materias en las que un estudiante está inscrito.
    enrolled_subject_ids = fields.Many2many(
        'school.subject', string="Materias Inscritas", compute='_compute_enrolled_subjects')

    def _compute_enrolled_subjects(self):
        # Esta función se puede implementar para buscar en las inscripciones del estudiante.
        for partner in self:
            enrollments = self.env['school.enrollment'].search([('student_id', '=', partner.id), ('state', '=', 'confirmed')])
            partner.enrolled_subject_ids = enrollments.mapped('subject_id')