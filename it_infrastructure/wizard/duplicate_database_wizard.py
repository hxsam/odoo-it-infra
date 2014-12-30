# -*- coding: utf-8 -*-

from openerp import fields, api, _
from openerp.osv import osv
from openerp.exceptions import Warning


class infrastructure_duplicate_database_wizard(osv.osv_memory):
    _name = "it_infrastructure.duplicate_db.wizard"
    _description = "IT Infrastructure Duplicate db Wizard"

    new_database_name = fields.Char(string='New db Name', required=True)
    change_user = fields.Boolean(string='Change Instance?')
    server_id = fields.Many2one('it_infrastructure.server', string='Server')
    instance_id = fields.Many2one('it_infrastructure.instance', string='Instance')

    @api.one
    def duplicate_db(self):
        # TODO implementar si hay cambio de usuario
        if self.change_user:
            raise Warning(_("Not Implemented Yet!"))
        active_ids = self.env.context.get('active_ids', False)
        if not active_ids:
            raise Warning(
                _("Can not duplicate database, no active_ids on context"))
        databases = self.env['it_infrastructure.database'].search(
            [('id', 'in', active_ids)])
        for database in databases:
            database.duplicate_db(self.new_database_name)
