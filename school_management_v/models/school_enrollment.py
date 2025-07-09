# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SchoolEnrollment(models.Model):
    _name = "school.enrollment"
    _description = "Inscripción de Estudiante"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(
        string="Referencia",
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _("Nuevo"),
    )
    student_id = fields.Many2one(
        "res.partner",
        string="Estudiante",
        required=True,
        domain="[('is_student', '=', True)]",
    )
    schedule_id = fields.Many2one(
        "school.subject.schedule", string="Horario de Materia", required=True
    )

    # Campos relacionados para fácil acceso
    subject_id = fields.Many2one(
        "school.subject",
        related="schedule_id.subject_id",
        string="Materia",
        store=True,
        readonly=True,
    )
    teacher_id = fields.Many2one(
        "res.partner",
        related="schedule_id.teacher_id",
        string="Profesor",
        store=True,
        readonly=True,
    )

    state = fields.Selection(
        [
            ("draft", "Borrador"),
            ("confirmed", "Confirmado"),
            ("cancelled", "Cancelado"),
        ],
        string="Estado",
        default="draft",
        tracking=True,
    )

    student_schedule_id = fields.Many2one(
        "school.student.schedule",
        string="Registro de Horario Estudiante",
        readonly=True,
    )

    contract_count = fields.Integer(
        compute="_compute_contract_count", string="Contratos"
    )
    contract_ids = fields.One2many(
        "school.contract", "enrollment_id", string="Contratos"
    )

    def _compute_contract_count(self):
        for enrollment in self:
            enrollment.contract_count = len(enrollment.contract_ids)

    def action_confirm(self):

        res = super().action_confirm()
        self._create_contract()
        self.write({"state": "confirmed"})
        return res

    def _create_contract(self):
        for enrollment in self:
            if enrollment.contract_count > 0:
                continue  # Evita crear contratos duplicados

            contract_lines = []
            for (
                line
            ) in (
                enrollment.enrollment_subject_ids
            ):  # Asumo que así se llama tu One2many
                contract_lines.append(
                    (
                        0,
                        0,
                        {
                            "subject_id": line.subject_id.id,
                            "teacher_id": line.teacher_id.id,
                            "price_unit": 0,  # El costo se ingresa manualmente en el contrato
                        },
                    )
                )

            self.env["school.contract"].create(
                {
                    "student_id": enrollment.student_id.id,
                    "enrollment_id": enrollment.id,
                    "contract_line_ids": contract_lines,
                }
            )

    def action_view_contracts(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Contratos",
            "res_model": "school.contract",
            "view_mode": "tree,form",
            "domain": [("id", "in", self.contract_ids.ids)],
            "context": {"default_student_id": self.student_id.id},
        }

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", _("Nuevo")) == _("Nuevo"):
                vals["name"] = self.env["ir.sequence"].next_by_code(
                    "school.enrollment"
                ) or _("Nuevo")
        return super().create(vals_list)

    def action_confirm(self):
        self.ensure_one()
        if not self.student_schedule_id:
            schedule = self.env["school.student.schedule"].create(
                {
                    "enrollment_id": self.id,
                }
            )
            self.student_schedule_id = schedule.id
        self.write({"state": "confirmed"})

    def action_cancel(self):
        self.write({"state": "cancelled"})
        if self.student_schedule_id:
            self.student_schedule_id.unlink()

    def action_draft(self):
        self.write({"state": "draft"})
