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
from datetime import datetime, timedelta, date

import logging
import inspect
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_compare, float_is_zero, float_round

_logger = logging.getLogger(__name__)

class yummy_realtime_product_category(models.Model):
    _inherit = 'product.category'


    def insert_to_log_table(self, categ_name="", exc=False, func_name="", payload=""):
        #Insert to log table
        error_message = exc if exc else self.error_message
        module_obj = self.env['ir.model'].sudo().search([('model', '=', 'product.category')], limit=1)
        if module_obj:
            self.env['yummy.allsync.log'].create({
                'model_name': module_obj.name,
                'nama_module': module_obj.id,
                'error_details': error_message,
                'func_name': func_name,
                'payload': payload
            })
            self.env.cr.commit()
        return True

    def email_notif(self, categ_name="", exc=False):
        partner_objs = self.env['res.partner'].sudo().search([('name', '=', 'Tech Product')])
        error_message = exc if exc else self.error_message
        message = '<br>~ ' +str(categ_name)+ ' >> Error Message >> ' + str(error_message)
        for partner_obj in partner_objs:
            body =  """<html>
                            <body>
                                <div>
                                    <strong>Cannot sync product category</strong>
                                </div>
                                <br>
                                %s
                            </body>
                        </html>
                    """ % (message)
            mail_details = {
                'subject': "Failed Sync Product Category",
                'body': body,
                'partner_ids': [partner_obj.id]
            }
            partner_obj.message_post(message_type="email", **mail_details)
            partner_obj.env.cr.commit()
        return True

    def get_cookies(self):
        pos_url = self.env['ir.config_parameter'].sudo().get_param('pos_url')
        pos_username = self.env['ir.config_parameter'].sudo().get_param('pos_username')
        pos_password = self.env['ir.config_parameter'].sudo().get_param('pos_password')
        pos_db = self.env['ir.config_parameter'].sudo().get_param('pos_db')
        cookies = False

        headers = {'Content-type': 'application/json'}
        datas_auth = {
            'params': {
                'login': pos_username,
                'password': pos_password,
                'db': pos_db
            }
        }

        # Authenticate user
        try:
            res_auth = requests.post(pos_url+'/api/auth/', data=json.dumps(datas_auth), headers=headers)
            cookies = res_auth.cookies
            if res_auth.json().get('error'):
                self.insert_to_log_table(str(self.name), res_auth.json().get('error').get('data').get('message'), 'get_cookies', datas_auth)
                self.email_notif(str(self.name), res_auth.json().get('error').get('data').get('message'))
                cookies = False
        except Exception as exc:
            self.insert_to_log_table(str(self.name), res_auth.json().get('error').get('data').get('message'), 'get_cookies', datas_auth)
            self.email_notif(str(self.name), exc, 'get_cookies', datas_auth)
                
        return cookies

    @api.model
    def create(self, vals):
        categ_id = False
        if vals.get('parent_id'):
            categ_id = self.browse(vals.get('parent_id')).complete_name
        myremov = False
        if vals.get('removal_strategy_id'):
            myremov = self.env['product.removal'].browse(vals.get('removal_strategy_id')).name

        cname=''
        com_name=''
        pro_method=False
        pro_val=False
        if vals.get('name'):
            cname= vals.get('name')
        if vals.get('complete_name'):
            com_name = vals.get('complete_name')
        if vals.get('property_cost_method'):
            pro_method = vals.get('property_cost_method')
        if vals.get('property_valuation'):
            pro_val = vals.get('property_valuation')

        # Authenticate user
        cookies = self.get_cookies()
        if not cookies:
            raise UserError(_("Cannot login to odoo outlet, please contact the IT team"))
        
        res = super(yummy_realtime_product_category, self).create(vals)
        routes = []
        for route_id in res.route_ids:
            routes.append({
                'name': route_id.name,
                'company_name': route_id.company_id.name
            })
        if res.id:
            pos_url = self.env['ir.config_parameter'].sudo().get_param('pos_url')

            headers = {'Content-type': 'application/json'}
            data = {
                "params":{
                    'name': cname,
                    'complete_name': com_name,
                    'parent_id': categ_id,
                    'property_cost_method': pro_method,
                    'property_valuation': pro_val,
                    'removal_strategy_id': myremov,
                    'product_category_id_core': res.id,
                    'routes': routes
                }
            }

            try:
                req = requests.post(pos_url + "/api/insert-category/", headers=headers, data=json.dumps(data), cookies=cookies)
                _logger.info('datetime: %s, function name: %s,Data %s uid: %s, model: %s',
                                datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                                'Insert Product Category Data realtime To POS', data, self._uid, self._name)
                req.raise_for_status()
            except Exception as exc:
                self.insert_to_log_table(str(res.name), exc, 'create', data)
                self.email_notif(str(res.name), exc, 'create', data)
        
        return res

    def unlink(self):
        product_category_core_ids = []
        product_category_names = []
        pos_url = self.env['ir.config_parameter'].sudo().get_param('pos_url')
        for alldata in self:
            product_category_core_ids.append(alldata.id)
            product_category_names.append(alldata.name)

        if product_category_core_ids:
            # Authenticate user
            cookies = self.get_cookies()
            if not cookies:
                raise UserError(_("Cannot login to odoo outlet, please contact the IT team"))

            headers = {'Content-type': 'application/json'}
            data = {
                "params":{
                    "product_category_core_ids": product_category_core_ids
                }
            }

            try:
                req = requests.post(pos_url + "/api/delete-category/", headers=headers, data=json.dumps(data), cookies=cookies)
                _logger.info('datetime: %s, function name: %s, Data %s uid: %s, Product Categories: %s',
                                datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                                'Delete Product Category Data realtime To POS', data, self._uid, product_category_names)
                req.raise_for_status()
            except Exception as exc:
                self.insert_to_log_table(str(product_category_names), exc, 'unlink', data)
                self.email_notif(str(product_category_names), exc, 'unlink', data)

            _logger.info('datetime: %s, function name: %s, Product Categ Ids %s, uid: %s, Product Categories: %s',
                            datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                            'Delete Product Category Data realtime To POS', self.ids, self._uid, product_category_names)

        return super(yummy_realtime_product_category, self).unlink()

    def write(self, vals):
        # Authenticate user
        cookies = self.get_cookies()
        if not cookies:
            raise UserError(_("Cannot login to odoo outlet, please contact the IT team"))

        res = super(yummy_realtime_product_category, self).write(vals)
        self.start_edit_category(self.id, cookies)
        return res

    def start_edit_category(self, ids, cookies):
        mydata = False
        mydata = self.env['product.category'].browse(ids)
        for alldata in mydata:
            pos_url = self.env['ir.config_parameter'].sudo().get_param('pos_url')

            routes = []
            for route_id in alldata.route_ids:
                routes.append({
                    'name': route_id.name,
                    'company_name': route_id.company_id.name
                })

            headers = {'Content-type': 'application/json'}
            data = {
                'params': {
                    'name': alldata.name,
                    'complete_name': alldata.complete_name,
                    'parent_id': alldata.parent_id.complete_name,
                    'property_cost_method': alldata.property_cost_method,
                    'property_valuation': alldata.property_valuation,
                    'removal_strategy_id': alldata.removal_strategy_id.name,
                    'product_category_id_core':alldata.id,
                    'routes': routes
                }
            }

            try:
                req = requests.post(pos_url + "/api/insert-category/", headers=headers, data=json.dumps(data), cookies=cookies)
                _logger.info('datetime: %s, function name: %s,Data %s uid: %s, model: %s',
                                datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                                'Update Product Category Data realtime To POS', data, self._uid, self._name)
            except Exception as exc:
                self.insert_to_log_table(str(alldata.name), exc, 'start_edit_category', data)
                self.email_notif(str(alldata.name), exc, 'start_edit_category', data)