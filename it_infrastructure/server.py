# -*- coding: utf-8 -*-

from openerp import netsvc
from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning
from fabric.api import env, reboot


class server(models.Model):

    _name = 'it_infrastructure.server'
    _description = 'server'
    _inherit = [
        'it_infrastructure.computer',
    ]

    password = fields.Char(
        string='Password'
    )

    remote_mgmt_port = fields.Char(
        string='Remote Management Port'
    )

    open_ports = fields.Char(
        string='Open Ports'
    )

    vpn_required = fields.Boolean(
        string='VPN Required',
        default=False
    )

    server_repository_ids = fields.One2many(
        'it_infrastructure.server_repository',
        'server_id',
        string='server_repository_ids'
    )

    hostname_ids = fields.One2many(
        'it_infrastructure.server_hostname',
        'server_id',
        string='Hostnames'
    )

    change_ids = fields.One2many(
        'it_infrastructure.computer_change',
        'computer_id',
        string='Changes'
    )

    server_configuration_id = fields.Many2one(
        'it_infrastructure.server_configuration',
        string='Configuration',
        required=True
    )

    @api.one
    def unlink(self):
        if self.state not in ('draft', 'cancel'):
            raise Warning(_(
                'You cannot delete a server which is not draft or cancelled.'))
        return super(server, self).unlink()

    @api.one
    @api.depends('environment_ids')
    def _get_environments(self):
        self.environment_count = len(self.environment_ids)

    @api.one
    def get_env(self):
        if not self.user_name:
            raise Warning(_('Not User Defined for the server'))
        if not self.password:
            raise Warning(_('Not Password Defined for the server'))
        env.user = self.user_name
        env.password = self.password
        env.host_string = self.main_hostname
        env.port = self.ssh_port
        return env

    @api.one
    def show_passwd(self):
        raise except_orm(
            _("Password for user '%s':") % self.user_name,
            _("%s") % self.password
        )

    @api.multi
    def reboot_server(self):
        self.get_env()
        reboot()

    def action_wkf_set_draft(self, cr, uid, ids, *args):
        self.write(cr, uid, ids, {'state': 'draft'})
        wf_service = netsvc.LocalService("workflow")
        for obj_id in ids:
            wf_service.trg_delete(uid, 'it_infrastructure.server', obj_id, cr)
            wf_service.trg_create(uid, 'it_infrastructure.server', obj_id, cr)
        return True
