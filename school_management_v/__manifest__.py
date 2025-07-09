# -*- coding: utf-8 -*-
{
    "name": "Gestión Educativa",
    "summary": """
        Módulo completo para la gestión de materias, profesores, estudiantes,
        inscripciones y horarios.""",
    "description": """
        Este módulo proporciona una solución integral para instituciones educativas,
        permitiendo administrar:
        - Materias y sus horarios.
        - Perfiles de Profesores y Estudiantes.
        - Proceso de inscripción de estudiantes a materias.
        - Generación automática de horarios para estudiantes.
        - Dashboard de análisis.
        - Informes de inscripción.
    """,
    "author": "jose Silva ",
    "website": "",
    "category": "Educación",
    "version": "16.0.1.0.0",
    "depends": [
        "base",
        "web",
        "mail",
        "product",
        "sale",
        "hr",
        "account",
    ],
    "data": [
        "security/school_security.xml",
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "data/ir_config_parameter_data.xml",
        # Vistas primero
        "views/res_partner_views.xml",
        "views/school_subject_views.xml",
        "views/school_enrollment_views.xml",
        "views/school_student_schedule_views.xml",
        "views/school_contract_views.xml",
        "views/school_dashboard_views.xml",
        # Menús al final
        "views/menu_items.xml",
        "report/enrollment_report.xml",
        "report/enrollment_report_templates.xml",
    ],
    'demo': [
        'demo/demo_data.xml',
    ],
    "assets": {
        "web.assets_backend": [
            "school_management_v/static/src/**/*",
        ],
    },
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}
