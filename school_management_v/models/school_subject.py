# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SchoolSubject(models.Model):
    _name = 'school.subject'
    _description = 'Materia Escolar'

    name = fields.Char(string="Nombre de la Materia", required=True)
    code = fields.Char(string="Código")

    # Profesores que pueden impartir esta materia.
    teacher_ids = fields.Many2many(
        'res.partner',
        'subject_teacher_rel',
        'subject_id',
        'teacher_id',
        string="Profesores",
        domain="[('is_teacher', '=', True)]"
    )

    # Horarios disponibles para esta materia.
    schedule_ids = fields.One2many('school.subject.schedule', 'subject_id', string="Horarios")

    product_id = fields.Many2one(
        "product.product",
        string="Producto Relacionado",
        copy=False,
        help="Producto de tipo servicio usado para la facturación de esta materia.",
    )

    @api.model_create_multi
    def create(self, vals_list):
        subjects = super().create(vals_list)
        for subject in subjects:
            if not subject.product_id:
                product = self.env["product.product"].create(
                    {
                        "name": subject.name,
                        "type": "service",
                        "invoice_policy": "order", # Facturar cantidades pedidas
                        "lst_price": 0.0, # El precio se define en el contrato
                    }
                )
                subject.product_id = product.id
        return subjects

    def write(self, vals):
        res = super().write(vals)
        if "name" in vals:
            for subject in self:
                if subject.product_id and subject.product_id.name != vals["name"]:
                    subject.product_id.name = vals["name"]
        return res