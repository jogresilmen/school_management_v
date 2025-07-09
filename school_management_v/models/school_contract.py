# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SchoolContract(models.Model):
    _name = "school.contract"
    _description = "Contrato Estudiantil"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(
        string="Referencia del Contrato",
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
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    enrollment_id = fields.Many2one(
        "school.enrollment",
        string="Inscripción Asociada",
        readonly=True,
    )
    contract_line_ids = fields.One2many(
        "school.contract.line",
        "contract_id",
        string="Líneas del Contrato",
        states={"draft": [("readonly", False)]},
        readonly=True,
    )
    state = fields.Selection(
        [
            ("draft", "Borrador"),
            ("confirmed", "Confirmado"),
            ("invoiced", "Facturado"),
            ("paid", "Pagado"),
            ("cancel", "Cancelado"),
        ],
        string="Estado",
        default="draft",
        tracking=True,
    )
    amount_total = fields.Monetary(
        string="Total",
        compute="_compute_amount_total",
        store=True,
        currency_field="currency_id",
    )
    currency_id = fields.Many2one(
        "res.currency",
        string="Moneda",
        default=lambda self: self.env.company.currency_id,
    )
    invoice_id = fields.Many2one(
        "account.move", string="Factura", readonly=True, copy=False
    )
    invoice_status = fields.Selection(
        related="invoice_id.payment_state",
        string="Estado de Pago de Factura",
        store=True,
    )

    @api.model
    def create(self, vals):
        if vals.get("name", _("Nuevo")) == _("Nuevo"):
            vals["name"] = self.env["ir.sequence"].next_by_code("school.contract") or _(
                "Nuevo"
            )
        return super(SchoolContract, self).create(vals)

    @api.depends("contract_line_ids.price_subtotal")
    def _compute_amount_total(self):
        for contract in self:
            contract.amount_total = sum(
                contract.contract_line_ids.mapped("price_subtotal")
            )

    def action_confirm(self):
        self.ensure_one()
        if not self.contract_line_ids:
            raise UserError(
                _("No se puede confirmar un contrato sin líneas de materias.")
            )
        self.write({"state": "confirmed"})

    def action_create_invoice(self):
        self.ensure_one()
        if self.invoice_id:
            raise UserError(_("Este contrato ya tiene una factura asociada."))

        invoice_lines = []
        for line in self.contract_line_ids:
            if not line.subject_id.product_id:
                raise UserError(
                    _(
                        "La materia '%s' no tiene un producto asociado. Por favor, créelo primero."
                    )
                    % line.subject_id.name
                )
            invoice_lines.append(
                (
                    0,
                    0,
                    {
                        "product_id": line.subject_id.product_id.id,
                        "name": f"{line.subject_id.name} (Prof: {line.teacher_id.name})",
                        "quantity": 1,
                        "price_unit": line.price_unit,
                    },
                )
            )

        invoice = self.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "partner_id": self.student_id.id,
                "invoice_date": fields.Date.today(),
                "invoice_line_ids": invoice_lines,
            }
        )
        self.write({"invoice_id": invoice.id, "state": "invoiced"})
        return self.action_view_invoice()

    def action_view_invoice(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Factura"),
            "res_model": "account.move",
            "view_mode": "form",
            "res_id": self.invoice_id.id,
            "target": "current",
        }

    @api.depends("invoice_status")
    def _compute_contract_state_from_invoice(self):
        for contract in self:
            if contract.invoice_status == "paid":
                contract.state = "paid"


class SchoolContractLine(models.Model):
    _name = "school.contract.line"
    _description = "Línea de Contrato Estudiantil"

    contract_id = fields.Many2one(
        "school.contract", string="Contrato", ondelete="cascade"
    )
    subject_id = fields.Many2one("school.subject", string="Materia", required=True)
    teacher_id = fields.Many2one(
        "hr.employee",
        string="Profesor",
        required=True,
        domain="[('is_teacher', '=', True)]",
    )
    price_unit = fields.Float(string="Costo de la Materia", required=True, default=0.0)
    price_subtotal = fields.Monetary(
        string="Subtotal",
        compute="_compute_price_subtotal",
        store=True,
        currency_field="currency_id",
    )
    currency_id = fields.Many2one(related="contract_id.currency_id", store=True)

    @api.depends("price_unit")
    def _compute_price_subtotal(self):
        for line in self:
            line.price_subtotal = line.price_unit
