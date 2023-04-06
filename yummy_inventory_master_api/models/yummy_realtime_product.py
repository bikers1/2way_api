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


class yummy_realtime_product(models.Model):
    _inherit = 'product.template'

    core_item = fields.Boolean(string='is Core', default=True)
    is_new_data = fields.Boolean(default=False)

    def get_notification_mail(self):
        email_from = "odoobot@yummycorp.com"
        email_to = "tech-product@yummycorp.com"
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        mail_server_ids = self.env['ir.mail_server'].sudo().search([('sequence', '=', '10')])
        mail_server_id = mail_server_ids[0].id if mail_server_ids else 1
        mail_mail_obj = self.env['mail.mail']
        msg_id = mail_mail_obj.create({
            'email_from': email_from,
            'subject': 'Failed Sync Product Master Data',
            'email_to': email_to,
            'mail_server_id': mail_server_id,
            'body_html': u"""
                            <H3>List of Product Failed to Sync</H3>
                            <hr />
                            <table border='0' style='font-size:14px;font-family:verdana'>
                            <tr>
                                <td style='width:230px'>Product</td><td>: {_product}</td>
                            </tr>
                            </table>
                        """.format(_product=self.display_name, _categ=self.categ_id.name, _uom=self.uom_id.name)
        })
        mail_mail_obj.send([msg_id])
        return True

    @api.model
    def create(self, vals):
        vals.update({'is_new_data': True})
        myactive = vals.get('active')
        res = super(yummy_realtime_product, self).create(vals)
        for rec in res:
            if rec.state_product == 'approve':
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
                check_data_sync = {
                    'params': {
                        'default_code': rec.default_code,
                        'idcore': rec.id,
                    }
                }
                integration = pos_url + "/api/sync-product-pos-from-core/"
                check_sync = requests.post(integration, headers=headers, data=json.dumps(check_data_sync),cookies=cookies)
                get_data_sync = check_sync.json()
                if len(get_data_sync['result']['response']) == 0:
                    email_from = "odoobot@yummycorp.com"
                    email_to = "tech-product@yummycorp.com"
                    mail_server_ids = self.env['ir.mail_server'].sudo().search([('sequence', '=', '10')])
                    mail_server_id = mail_server_ids[0].id if mail_server_ids else 1
                    mail_mail_obj = self.env['mail.mail']
                    msg_id = mail_mail_obj.create({
                        'email_from': email_from,
                        'subject': 'Failed Sync Product Master Data',
                        'email_to': email_to,
                        'mail_server_id': mail_server_id,
                        'body_html': u"""
                                        <H3>List of Product Failed to Sync</H3>
                                        <hr />
                                        <table border='0' style='font-size:14px;font-family:verdana'>
                                        <tr>
                                            <td style='width:230px'>Product</td><td>: {_product}</td>
                                        </tr>
                                        </table>
                                    """.format(_product=rec.display_name, _categ=rec.categ_id.name, _uom=rec.uom_id.name)
                    })
                    mail_mail_obj.send([msg_id])
                else:
                    pass
        return res

    def approve(self):
        res = super(yummy_realtime_product,self).approve()
        for alldata in self:
            product_obj = self.env['product.product']
            find_product = product_obj.search([('product_tmpl_id', '=', alldata.id)], limit=1)
            if find_product.state == 'approve':
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
                categ_id = False
                if alldata.categ_id.id:
                    categ_id = self.env['product.category'].browse(alldata.categ_id.id).complete_name
                mycom  = False
                if alldata.company_id:
                    mycom = self.env['res.company'].browse(alldata.company_id.id).name
                myuom = False
                if alldata.uom_id:
                    myuom = self.env['uom.uom'].browse(alldata.uom_id.id).name
                myuompoid = False
                if alldata.uom_po_id:
                    myuompoid =  self.env['uom.uom'].browse(alldata.uom_po_id.id).name

                data = {
                    'params': {
                        "idcore": str(find_product.id),
                        'name': find_product.name,
                        'sale_ok': alldata.sale_ok,
                        'purchase_ok': alldata.purchase_ok,
                        'type': alldata.type,
                        'categ_id': categ_id,
                        'default_code': find_product.default_code,
                        'defcode_template': alldata.default_code,
                        'list_price': alldata.list_price,
                        'standard_price': alldata.standard_price,
                        'company_id': mycom,
                        'uom_id': myuom,
                        'uom_po_id': myuompoid,
                        'dari_sync': False,
                        'barcode': alldata.barcode,
                        'core_item': alldata.core_item,
                        'display_name': alldata.display_name,
                        'idcore_temp': alldata.id,
                        'product_brand_id': alldata.product_brand_id.name,
                    }
                }
                sync_url = pos_url + "/api/insert-product"
                try:
                    req = requests.post(sync_url, headers=headers, data=json.dumps(data),cookies=cookies)
                    req.raise_for_status()
                except requests.HTTPError:
                    raise UserError(_(requests.status_codes))
                alldata.is_new_data = False

                check_data_sync = {
                    'params': {
                        'default_code': self.default_code,
                        'idcore': self.id,
                    }
                }
                integration = pos_url+"/api/sync-product-pos-from-core/"
                check_sync = requests.post(integration, headers=headers, data=json.dumps(check_data_sync),cookies=cookies)
                get_data_sync = check_sync.json()
                if len(get_data_sync['result']['response']) == 0:
                    self.get_notification_mail()
                else:
                    pass
        return res

    def unlink(self):
        for alldata in self:
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

            headers = {'Content-type': 'multipart/form-data; boundary=---- '}
            product_obj = self.env['product.product']
            find_product = product_obj.search([('product_tmpl_id', '=', alldata.id)], limit=1)
            put_url = '/api/delete-product?name='+ alldata.name +'&idcore='+ str(find_product.id)
            urldelete = pos_url + put_url
            try:
                    req = requests.delete(urldelete,  headers=headers,cookies=cookies)
                    req.raise_for_status()
            except requests.HTTPError:
                raise UserError(_(requests.status_codes))
        return super(yummy_realtime_product,self).unlink()

    def start_realtime_sync(self,ids,databaru=False):

        mydata = False
        if not ids and databaru:
            date_format = '%Y-%m-%d'
            mydate = datetime.now()
            current_date = (mydate).strftime(date_format)
            myobj = self.env['product.template'].search([])
            mycari = myobj.filtered(lambda jj: jj.is_new_data == True)
            if mycari:
                for allcari in mycari:
                    mydata = allcari
        else:
            mydata = self.env['product.template'].browse(ids)
        product_obj = self.env['product.product']
        find_product = product_obj.search([('product_tmpl_id', '=', mydata.id)], limit=1)
        if find_product.state == 'approve' :
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
            data = {
                'params': {
                    "idcore": str(find_product.id),
                    'name': find_product.name,
                    'sale_ok': mydata.sale_ok,
                    'purchase_ok': mydata.purchase_ok,
                    'type': mydata.type,
                    'categ_id': mydata.categ_id.complete_name,
                    'default_code': find_product.default_code,
                    'defcode_template': mydata.default_code,
                    'list_price': mydata.list_price,
                    'taxes_id': mydata.taxes_id.name,
                    'standard_price': mydata.standard_price,
                    'company_id': mydata.company_id.name,
                    'uom_id': mydata.uom_id.name,
                    'uom_po_id': mydata.uom_po_id.name,
                    'dari_sync': False,
                    'barcode': mydata.barcode,
                    'core_item': mydata.core_item,
                    'display_name': mydata.display_name,
                    'idcore_temp': mydata.id,
                    'product_brand_id': mydata.product_brand_id.name,
                }
            }
            sync_url = pos_url + "/api/insert-product"
            try:
                req = requests.post(sync_url, headers=headers, data=json.dumps(data),cookies=cookies)
                req.raise_for_status()
            except requests.HTTPError:
                raise UserError(_(requests.status_codes))
            mydata.is_new_data = True


    def write(self, vals):
        myactive = self.active
        res = super(yummy_realtime_product,self).write(vals)
        if myactive != self.active:
            self.start_archive_product(self.id,self.active)

        return res

    def start_archive_product(self,ids,arch):
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
        allres = self.env['product.template'].browse(ids)
        product_obj = self.env['product.product']
        find_product = product_obj.search([('product_tmpl_id', '=', allres.id),'|',('active','=',True),('active','=',False)],limit=1)
        data = {
            'params': {
                "idcore": str(find_product.id),
                'name': find_product.name,
                'default_code': find_product.default_code,
                'active': arch,
            }
        }

        sync_url = pos_url + "/api/product/edit"
        try:
            req = requests.post(sync_url, headers=headers, data=json.dumps(data),cookies=cookies)
            req.raise_for_status()
        except requests.HTTPError:
            raise UserError(_(requests.status_codes))


