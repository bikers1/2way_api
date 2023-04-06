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

class yummy_realtime_uom(models.Model):
    _inherit = 'uom.uom'


    def insert_to_log_table(self, exc=False, func_name="", payload=""):
        #Insert to log table
        error_message = exc if exc else self.error_message
        module_obj = self.env['ir.model'].sudo().search([('model', '=', 'uom.uom')], limit=1)
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

    def email_notif(self, uom_name="", exc=False):
        partner_objs = self.env['res.partner'].sudo().search([('name', '=', 'Tech Product')])
        error_message = exc if exc else self.error_message
        message = '<br>~ ' +str(uom_name)+ ' >> Error Message >> ' + str(error_message)
        for partner_obj in partner_objs:
            body =  """<html>
                            <body>
                                <div>
                                    <strong>Cannot sync UoM</strong>
                                </div>
                                <br>
                                %s
                            </body>
                        </html>
                    """ % (message)
            mail_details = {
                'subject': "Failed Sync UoM",
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
                self.insert_to_log_table(res_auth.json().get('error').get('data').get('message'), 'get_cookies', datas_auth)
                self.email_notif(str(self.name), res_auth.json().get('error').get('data').get('message'))
                cookies = False
        except Exception as exc:
            self.insert_to_log_table(res_auth.json().get('error').get('data').get('message'), 'get_cookies', datas_auth)
            self.email_notif(str(self.name), exc)
                
        return cookies

    @api.model
    def create(self, vals):
        nama_uom = False
        if vals.get('name'):
            nama_uom = vals.get('name')
        faktor = False
        if vals.get('factor'):
            faktor = vals.get('factor')
        categ_id = False
        if vals.get('category_id'):
            categ_id = self.env['uom.category'].browse(vals.get('category_id')).name
        faktorinv = False
        if vals.get('factor_inv'):
            faktorinv = vals.get('factor_inv')
        rounding = False
        if vals.get('rounding'):
            rounding = vals.get('rounding')
        active = False
        if vals.get('active'):
            active = vals.get('active')
        uom_type = False
        if vals.get('uom_type'):
            uom_type = vals.get('uom_type')
        measure_type = False
        if vals.get('measure_type'):
            measure_type = vals.get('measure_type')
        display_name = False
        if vals.get('display_name'):
            display_name = vals.get('display_name')

        # Authenticate user
        cookies = self.get_cookies()
        if not cookies:
            raise UserError(_("Cannot login to odoo outlet, please contact the IT team"))

        res = super(yummy_realtime_uom, self).create(vals)
        if res.id:
            uom_id_core = res.id
            pos_url = self.env['ir.config_parameter'].sudo().get_param('pos_url')

            headers = {'Content-type': 'application/json'}
            data = {
                'params': {
                    'name': nama_uom,
                    'category_id': categ_id,
                    'factor': faktor,
                    'factor_inv': faktorinv,
                    'rounding': rounding,
                    'active': active,
                    'uom_type': uom_type,
                    'measure_type': measure_type,
                    'display_name': display_name,
                    'uom_id_core': uom_id_core,
                }
            }

            try:
                req = requests.post(pos_url + "/api/insert-uom/", headers=headers, data=json.dumps(data), cookies=cookies)
                if req.json().get('result') == 'Failed, UoM Category not found':
                    self.insert_to_log_table('Failed, UoM Category not found', 'start_create_uom', data)
                    self.email_notif(str(nama_uom), 'Failed, UoM Category not found')
                elif req.json().get('error'):
                    self.insert_to_log_table(req.json().get('error'), 'start_create_uom', data)
                    self.email_notif(str(nama_uom), req.json().get('error'))
                _logger.info('datetime: %s, function name: %s,Data %s uid: %s, model: %s',
                             datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                             'create UOM Data realtime To POS', data, self._uid, self._name)
                req.raise_for_status()
            except Exception as exc:
                self.insert_to_log_table(exc, 'create', data)
                self.email_notif(str(res.name), exc)

            _logger.info('datetime: %s, function name: %s, Uom ID %s, uid: %s, model: %s',
                         datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                         'create UOM Data realtime To POS', self.id, self._uid, self._name)
        return res

    def unlink(self):
        product_uom_names = []
        pos_url = self.env['ir.config_parameter'].sudo().get_param('pos_url')
        for alldata in self:
            product_uom_names.append(alldata.name)
            headers = {'Content-type': 'application/json'}
            dataku = {
                'params': {
                    "uom_id_core": alldata.id,
                }
            }
            
            # Authenticate user
            cookies = self.get_cookies()

            try:
                req = requests.post(pos_url + "/api/delete-uom/", headers=headers, data=json.dumps(dataku), cookies=cookies)
                _logger.info('datetime: %s, function name: %s,Data %s uid: %s, model: %s',
                             datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                             'Delete UOM Data realtime To POS', dataku, self._uid, self._name)
                req.raise_for_status()
            except Exception as exc:
                self.insert_to_log_table(exc, 'unlink', dataku)
                self.email_notif(str(product_uom_names), exc)

            _logger.info('datetime: %s, function name: %s, Uom ID %s, uid: %s, model: %s',
                         datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                         'Delete UOM Data realtime To POS', self.id, self._uid, self._name)

        return super(yummy_realtime_uom, self).unlink()

    def write(self, vals):
        # Authenticate user
        cookies = self.get_cookies()
        if not cookies:
            raise UserError(_("Cannot login to odoo outlet, please contact the IT team"))

        res=super(yummy_realtime_uom, self).write(vals)
        self.start_edit_uom(self.id, cookies)
        return res

    def start_edit_uom(self, ids, cookies):
        mydata = False
        mydata = self.env['uom.uom'].browse(ids)
        categ_id = False
        if mydata.category_id.id:
            categ_id = self.env['uom.category'].browse(mydata.category_id.id).name

        pos_url = self.env['ir.config_parameter'].sudo().get_param('pos_url')
        headers = {'Content-type': 'application/json'}
        data = {
            'params': {
                'name': mydata.name,
                'category_id': categ_id,
                'factor': mydata.factor,
                'factor_inv': mydata.factor_inv,
                'rounding': mydata.rounding,
                'active': mydata.active,
                'uom_type': mydata.uom_type,
                'measure_type': mydata.measure_type,
                'display_name': mydata.display_name,
                'uom_id_core':mydata.id,
            }
        }

        try:
            req = requests.post(pos_url + "/api/insert-uom/", headers=headers, data=json.dumps(data), cookies=cookies)
            if req.json().get('result') == 'Failed, UoM Category not found':
                self.insert_to_log_table('Failed, UoM Category not found', 'start_edit_uom', data)
                self.email_notif(str(mydata.name), 'Failed, UoM Category not found')
            elif req.json().get('error'):
                self.insert_to_log_table(req.json().get('error'), 'start_edit_uom', data)
                self.email_notif(str(nama_uom), req.json().get('error'))
            _logger.info('datetime: %s, function name: %s,Data %s uid: %s, model: %s',
                            datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                            'Update UOM Data realtime To POS', data, self._uid, self._name)
            req.raise_for_status()
        except Exception as exc:
            self.insert_to_log_table(exc, 'start_edit_uom', data)
            self.email_notif(str(mydata.name), exc)

        _logger.info('datetime: %s, function name: %s, Uom ID %s, uid: %s, model: %s',
                        datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                        'Update UOM Data realtime To POS', self.id, self._uid, self._name)