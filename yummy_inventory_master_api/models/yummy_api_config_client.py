# -*- coding : utf-8 -*-
# Author => Albertus Restiyanto Pramayudha
# email  => xabre0010@gmail.com
# linkedin => https://www.linkedin.com/in/albertus-restiyanto-pramayudha-470261a8/
# youtube => https://www.youtube.com/channel/UCCtgLDIfqehJ1R8cohMeTXA

from odoo import api, fields, models,  tools, _
from odoo import http


class yummy_api_config_client(models.TransientModel):
    _name = 'yummy.api.client'
    _description = 'Yummy API Setting Client'

    url_host = fields.Char('URL Host',index=True,required=True)
    token_login = fields.Char('Token')

    @api.model
    def default_get(self, fields):
        res=super(yummy_api_config_client, self).default_get(fields)
        muser = ''
        mpass = ''
        mdb =''
        m_set = self.env['yummy.api.client'].search([])
        if m_set:
            for allset in m_set:
                if 'url_host' in fields:
                    urlhost = self.env['ir.config_parameter'].sudo().get_param('api_client_host')
                    if urlhost:
                        res.update({'url_host': urlhost})
                    tokennya = self.env['ir.config_parameter'].sudo().get_param('api_client_token')
                    if tokennya:
                        res.update({'token_login': tokennya})
        return res

    def action_apply(self):
        ir_config = self.env['ir.config_parameter'].sudo()
        ir_config.set_param("api_client_host", self.url_host)
        ir_config.set_param("api_client_token", self.token_login)
        return {'type': 'ir.actions.act_window_close'}

