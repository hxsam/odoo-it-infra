# -*- coding: utf-8 -*-

from openerp import models, fields


class workstation(models.Model):

    _name = 'it_infrastructure.workstation'
    _description = 'workstation'
    _inherit = [
        'it_infrastructure.computer',
    ]

    product_key = fields.Char(
        size=29
    )

    office_suite_id = fields.Many2one(
        'it_infrastructure.software',
        string='Office Suite',
        domain=[('category_id.parent_id', 'ilike', 'Office Suite')]
    )
