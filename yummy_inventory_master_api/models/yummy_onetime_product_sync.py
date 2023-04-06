# -*- coding : utf-8 -*-
# Author => Albertus Restiyanto Pramayudha
# email  => xabre0010@gmail.com
# linkedin => https://www.linkedin.com/in/albertus-restiyanto-pramayudha-470261a8/
# youtube => https://www.youtube.com/channel/UCCtgLDIfqehJ1R8cohMeTXA
from odoo import api, fields, models , tools, _
from urllib.parse import urlparse
from datetime import date, datetime
import requests
from odoo.exceptions import UserError
import json
from datetime import datetime, timedelta


class yummy_onetime_product_sync(models.Model):
    _inherit = 'product.product'

    def start_onetime_product_sync(self):
        product_data = self.env['product.product'].search([('state','=','approve'),('active','=',True)])
        pos_url = self.env['ir.config_parameter'].sudo().get_param("pos_url")
        pos_username = self.env['ir.config_parameter'].sudo().get_param('pos_username')
        pos_password = self.env['ir.config_parameter'].sudo().get_param('pos_password')
        pos_db = self.env['ir.config_parameter'].sudo().get_param('pos_db')
        AUTH_URL = pos_url + "/web/session/authenticate/"

        headersauth = {'Content-type': 'application/json'}
        dataauth = {
            'params': {
                'login': pos_username,
                'password': pos_password,
                'db': pos_db
            }
        }
        res = requests.post(
            AUTH_URL,
            data=json.dumps(dataauth),
            headers=headersauth
        )

        try:
            cookies = res.cookies
        except Exception:
            return "Invalid credentials."

        headers = {'Content-type': 'application/json'}

        token = req.content.decode().strip('"')
        for alldata in product_data:
            data = {
                'params': {
                    "idcore": str(alldata.id),
                    'name': alldata.name,
                    'sale_ok': alldata.sale_ok,
                    'purchase_ok': alldata.purchase_ok,
                    'type': alldata.type,
                    'categ_id': alldata.categ_id.complete_name,
                    'default_code': alldata.default_code,
                    'list_price': alldata.list_price,
                    'taxes_id': alldata.taxes_id.name,
                    'standard_price': alldata.product_tmpl_id.standard_price,
                    'company_id': alldata.company_id.name,
                    'uom_id': alldata.uom_id.name,
                    'uom_po_id': alldata.uom_po_id.name,
                    'dari_sync': False,
                    'barcode': alldata.barcode,
                    'core_item': alldata.core_item,
                    'display_name': alldata.display_name,
                    'idcore_temp': alldata.product_tmpl_id.id,
                    'defcode_template': alldata.product_tmpl_id.default_code,
                    'product_brand_id': alldata.product_brand_id.name,
                }
            }
            sync_url = pos_url + "/api/insert-product?session_id=" + token
            try:
                req = requests.post(sync_url, headers=headers, data=json.dumps(data),cookies=cookies)
                req.raise_for_status()
            except requests.HTTPError:
                raise UserError(_(requests.status_codes))
