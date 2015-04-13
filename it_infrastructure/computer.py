# -*- coding: utf-8 -*-

from openerp import models, fields


class computer(models.Model):

    _name = 'it_infrastructure.computer'
    _description = 'Computer'
    _inherit = [
        'it_infrastructure.equipment',
    ]

    hostname = fields.Char(
        string='Hostname',
        required=True
    )

    employee_id = fields.Many2one(
        'hr.employee',
        string='User'
    )

    username = fields.Char(
        string='Username',
        required=True
    )

    ip_address = fields.Char(
        string='IP Address',
        required=True
    )

    netmask = fields.Char(
        string='Network Mask',
        default='255.255.255.0',
        required=True
    )

    os_id = fields.Many2one(
        'it_infrastructure.software',
        string='Operating System',
        domain=[('category_id.parent_id', 'ilike', 'Operating System')],
        required=True
    )

    hardware_data = fields.Html(
        string='Hardware Data'
    )

    hardware_specs = fields.Binary(
        string='Hardware Specifications'
    )

    note = fields.Html(
        string='Note'
    )

    change_ids = fields.One2many(
        'it_infrastructure.computer_change',
        'computer_id',
        string='Changes'
    )

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Computer name must be unique!'),
        ('ip_address_unique', 'unique(ip_address)', 'Computer IP address must be unique!'),
        ('hostname_unique', 'unique(hostname)', 'Computer hostname must be unique!')
    ]
