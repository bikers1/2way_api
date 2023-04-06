# -*- coding : utf-8 -*-
# Author => Albertus Restiyanto Pramayudha
# email  => xabre0010@gmail.com
# linkedin => https://www.linkedin.com/in/albertus-restiyanto-pramayudha-470261a8/
# youtube => https://www.youtube.com/channel/UCCtgLDIfqehJ1R8cohMeTXA

from odoo import api, fields, models,  tools, _
from odoo import http


class yummy_api_config_server(models.TransientModel):
    _name = 'yummy.api.server'
    _description = 'Yummy API Server Setting'

    user_name = fields.Char('User Name',index=True,required=True)
    passwd = fields.Char('Password',required=True)
    db_active = fields.Char('Database',required=True)

    @api.model
    def default_get(self, fields):
        res=super(yummy_api_config_server, self).default_get(fields)
        muser = ''
        mpass = ''
        mdb =''
        m_set = self.env['yummy.api.server'].search([])
        if m_set:
            for allset in m_set:
                if 'user_name' in fields:
                    namauser = self.env['ir.config_parameter'].sudo().get_param('api_server_user')
                    if namauser:
                        res.update({'user_name': namauser})

                if 'passwd' in fields:
                    passwordnya = self.env['ir.config_parameter'].sudo().get_param('api_server_password')
                    if passwordnya:
                        res.update({'passwd': passwordnya})
                if 'db_active' in fields:
                    dbactive = self.env['ir.config_parameter'].sudo().get_param('api_server_database')
                    if dbactive:
                        res.update({'db_active': dbactive})
        return res

    def action_apply(self):
        ir_config = self.env['ir.config_parameter'].sudo()
        ir_config.set_param("api_server_user", self.user_name)
        ir_config.set_param("api_server_password", self.passwd)
        ir_config.set_param("api_server_database", self.db_active)

        return {'type': 'ir.actions.act_window_close'}

