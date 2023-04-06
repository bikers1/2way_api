# -*- coding : utf-8 -*-
# Author => Albertus Restiyanto Pramayudha
# email  => xabre0010@gmail.com
# linkedin => https://www.linkedin.com/in/albertus-restiyanto-pramayudha-470261a8/
# youtube => https://www.youtube.com/channel/UCCtgLDIfqehJ1R8cohMeTXA

import json
import math
import logging
import requests

from odoo import http, _, exceptions
from odoo.http import request
from odoo.addons.website.controllers.main import Home

from .serializers import Serializer
from .exceptions import QueryFormatError
import datetime

def error_response(error, msg):
    return {
        "jsonrpc": "2.0",
        "id": None,
        "error": {
            "code": 200,
            "message": msg,
            "data": {
                "name": str(error),
                "debug": "",
                "message": msg,
                "arguments": list(error.args),
                "exception_type": type(error).__name__
            }
        }
    }

class yummyinventorymasterinsert(Home):
    def make_json_response(self, data, headers=None, cookies=None):
        data = json.dumps(data)
        if headers is None:
            headers = {}
        headers["Content-Type"] = "application/json"
        return request.make_response(data, headers=headers, cookies=cookies)

    @http.route('/api/insert-product', type='json', auth="user", methods=['POST'], csrf=False)
    def insert_master_product_data(self, **params):
        try:
            namaproduct = params['name']
        except KeyError as e:
            msg = "Field Name For Database `%s` does not exist." % 'product.product'
            return self.make_json_response(msg)
        try:
            sale_ok = params['sale_ok']
        except KeyError as e:
            msg = "Field sale_ok For Database `%s` does not exist." % 'product.product'
            return self.make_json_response(msg)
        try:
            purchase_ok = params['purchase_ok']
        except KeyError as e:
            msg = "Field sale_ok For Database `%s` does not exist." % 'product.product'
            return self.make_json_response(msg)
        try:
            tipe = params['type']
        except KeyError as e:
            msg = "Field type For Database `%s` does not exist." % 'product.product'
            return self.make_json_response(msg)
        try:
            categ_id = params['categ_id']
        except KeyError as e:
            msg = "Field type For Database `%s` does not exist." % 'product.product'
            return self.make_json_response(msg)
        try:
            default_code = params['default_code']
        except KeyError as e:
            msg = "Field default_code For Database `%s` does not exist." % 'product.product'
            return self.make_json_response(msg)
        try:
            list_price = params['list_price']
        except KeyError as e:
            msg = "Field list_price For Database `%s` does not exist." % 'product.product'
            return self.make_json_response(msg)
        try:
            taxes_id = params['taxes_id']
        except KeyError as e:
            msg = "Field taxes_id For Database `%s` does not exist." % 'product.product'
            return self.make_json_response(msg)
        try:
            standard_price = params['standard_price']
        except KeyError as e:
            msg = "Field standard_price For Database `%s` does not exist." % 'product.product'
            return self.make_json_response(msg)
        try:
            company_id = params['company_id']
        except KeyError as e:
            msg = "Field company_id For Database `%s` does not exist." % 'product.product'
            return self.make_json_response(msg)
        try:
            uom_id = params['uom_id']
        except KeyError as e:
            msg = "Field company_id For Database `%s` does not exist." % 'product.product'
            return self.make_json_response(msg)
        try:
            uom_po_id = params['uom_po_id']
        except KeyError as e:
            msg = "Field uom_po_id For Database `%s` does not exist." % 'product.product'
            return self.make_json_response(msg)
        mycateg = request.env['product.category'].search([('complete_name','=',categ_id)]).id
        mycomp = request.env['res.company'].search([('name','=',company_id)],limit=1).id
        myuom = request.env['uom.uom'].search([('name','=',uom_id)],limit=1).id
        mypuom = request.env['uom.uom'].search([('name','=',uom_po_id)],limit=1).id
        mytax = request.env['account.tax'].search([('name','=',taxes_id)],limit=1).id
        try:
            prod_categ= request.env['product.template'].search([('name','=',namaproduct)])
            if not prod_categ:
              buat_data=  prod_categ.create({
                'name': namaproduct,
                'sale_ok': sale_ok,
                'purchase_ok': purchase_ok,
                'type': tipe,
                'categ_id': mycateg,
                'default_code': default_code,
                'list_price': list_price,
                'taxes_id': mytax,
                'standard_price': standard_price,
                'company_id': mycomp,
                'uom_id': myuom,
                'uom_po_id': mypuom,
                'dari_sync': params['dari_sync'],
                'core_item': params['core_item']})
            else:
                buat_data= prod_categ.write({
                'name': namaproduct,
                'sale_ok': sale_ok,
                'purchase_ok': purchase_ok,
                'type': tipe,
                'categ_id': mycateg,
                'default_code': default_code,
                'list_price': list_price,
                'taxes_id': mytax,
                'standard_price': standard_price,
                'company_id': mycomp,
                'uom_id': myuom,
                'uom_po_id': mypuom,
                'dari_sync': params['dari_sync'],
                'core_item': params['core_item']
                })
        except KeyError as e:
            return print("Failed to update or create master data product")
        return print("Finish Update or Create Master Data Product")

    @http.route('/product-category-api', type='json', auth="user", methods=['POST'], csrf=False)
    def insert_master_category_data(self, **params):
        try:
            namacateg = request.jsonrequest.get('name')
        except KeyError as e:
            msg = "Missing Field Name For Database `%s` does not exist." % 'product.category'
            return self.make_json_response(msg)
        try:
            complete_name = request.jsonrequest.get('name')
        except KeyError as e:
            msg = "Missing Field complete_name For Database `%s` does not exist." % 'product.category'
            return self.make_json_response(msg)
        try:
            parent_id = request.jsonrequest.get('parent_id')
        except KeyError as e:
            msg = "Missing Field parent_id For Database `%s` does not exist." % 'product.category'
            return self.make_json_response(msg)
        try:
            parent_path = request.jsonrequest.get('parent_path')
        except KeyError as e:
            msg = "Missing Field parent_path For Database `%s` does not exist." % 'product.category'
            return self.make_json_response(msg)
        try:
            route_ids = request.jsonrequest.get('route_ids')
        except KeyError as e:
            msg = "Missing Field route_ids For Database `%s` does not exist." % 'product.category'
            return self.make_json_response(msg)
        try:
            removal_strategy_id = request.jsonrequest.get('removal_strategy_id')
        except KeyError as e:
            msg = "Missing Field removal_strategy_id For Database `%s` does not exist." % 'product.category'
            return self.make_json_response(msg)
        try:
            total_route_ids = request.jsonrequest.get('total_route_ids')
        except KeyError as e:
            msg = "Missing Field total_route_ids For Database `%s` does not exist." % 'product.category'
            return self.make_json_response(msg)
        try:
            putaway_rule_ids = request.jsonrequest.get('putaway_rule_ids')
        except KeyError as e:
            msg = "Missing Field putaway_rule_ids For Database `%s` does not exist." % 'product.category'
            return self.make_json_response(msg)
        try:
            property_account_income_categ_id = request.jsonrequest.get('property_account_income_categ_id')
        except KeyError as e:
            msg = "Missing Field property_account_income_categ_id For Database `%s` does not exist." % 'product.category'
            return self.make_json_response(msg)
        try:
            property_account_expense_categ_id = request.jsonrequest.get('property_account_expense_categ_id')
        except KeyError as e:
            msg = "Missing Field property_account_expense_categ_id For Database `%s` does not exist." % 'product.category'
            return self.make_json_response(msg)
        try:
            property_account_creditor_price_difference_categ = request.jsonrequest.get('property_account_creditor_price_difference_categ')
        except KeyError as e:
            msg = "Missing Field property_account_creditor_price_difference_categ For Database `%s` does not exist." % 'product.category'
            return self.make_json_response(msg)
        try:
            property_valuation = request.jsonrequest.get('property_valuation')
        except KeyError as e:
            msg = "Missing Field property_valuation For Database `%s` does not exist." % 'product.category'
            return self.make_json_response(msg)
        try:
            property_cost_method = request.jsonrequest.get('property_cost_method')
        except KeyError as e:
            msg = "Missing Field property_cost_method For Database `%s` does not exist." % 'product.category'
            return self.make_json_response(msg)
        try:
            property_stock_journal = request.jsonrequest.get('property_stock_journal')
        except KeyError as e:
            msg = "Missing Field property_stock_journal For Database `%s` does not exist." % 'product.category'
            return self.make_json_response(msg)
        try:
            property_stock_account_input_categ_id = request.jsonrequest.get('property_stock_account_input_categ_id')
        except KeyError as e:
            msg = "Missing Field property_stock_account_input_categ_id For Database `%s` does not exist." % 'product.category'
            return self.make_json_response(msg)
        try:
            property_stock_account_output_categ_id = request.jsonrequest.get('property_stock_account_output_categ_id')
        except KeyError as e:
            msg = "Missing Field property_stock_account_output_categ_id For Database `%s` does not exist." % 'product.category'
            return self.make_json_response(msg)
        try:
            property_stock_valuation_account_id = request.jsonrequest.get('property_stock_valuation_account_id')
        except KeyError as e:
            msg = "Missing Field property_stock_valuation_account_id For Database `%s` does not exist." % 'product.category'
            return self.make_json_response(msg)
        try:
            total_group_ids = request.jsonrequest.get('total_group_ids')
        except KeyError as e:
            msg = "Missing Field total_group_ids For Database `%s` does not exist." % 'product.category'
            return self.make_jsontotal_group_idsesponse(msg)
        try:
            categ_seq = request.jsonrequest.get('categ_seq')
        except KeyError as e:
            msg = "Missing Field categ_seq For Database `%s` does not exist." % 'product.category'
            return self.make_json_response(msg)
        try:
            display_name = request.jsonrequest.get('display_name')
        except KeyError as e:
            msg = "Missing Field display_name For Database `%s` does not exist." % 'product.category'
            return self.make_json_response(msg)
        try:
            categ_id = request.env['product.category'].search([('name', '=', parent_id)]).id
        except KeyError as e:
            msg = "Missing Cannot Found Parent ID For Category %s in Database " % parent_id
            return self.make_json_response(msg)
        route_ids = []
        for allroute in route_ids:
            route_id = request.env['stock.location.route'].search([('name', '=', allroute['name'])]).id
            route_ids.append(route_id)
        try:
            domain = [('code', '=ilike', str(property_account_expense_categ_id).split(' ')[0] + '%')]
            a_income_categ = request.env['account.account'].search(domain).id
        except KeyError as e:
            msg = "property_account_expense_categ_id with %s Cannot Be Found in Database " % property_account_expense_categ_id
            return request.make_json_response(msg)
        try:
            domain = [('code', '=ilike', str(property_account_expense_categ_id).split(' ')[0] + '%')]
            a_expense_categ = request.env['account.account'].search(domain).id
        except KeyError as e:
            msg = "property_account_expense_categ_id with %s Cannot Be Found in Database " % property_account_expense_categ_id
            return request.make_json_response(msg)
        try:
            domain = [('code', '=ilike',
                       str(property_account_creditor_price_difference_categ).split(' ')[0] + '%')]
            a_c_d = request.env['account.account'].search(domain).id
        except KeyError as e:
            msg = "property_account_creditor_price_difference_categ with %s Cannot Be Found in Database " % property_account_creditor_price_difference_categ
            return request.make_json_response(msg)
        try:
            domain = [('code', '=ilike', str(property_valuation).split(' ')[0] + '%')]
            p_Value = request.env['account.account'].search(domain).id
        except KeyError as e:
            msg = "property_valuation with %s Cannot Be Found in Database " % property_valuation
            return request.make_json_response(msg)
        try:
            domain = [('code', '=ilike', str(property_cost_method).split(' ')[0] + '%')]
            p_Cost = request.env['account.account'].search(domain).id
        except KeyError as e:
                msg = "property_cost_method with %s Cannot Be Found in Database " % property_cost_method
                return request.make_json_response(msg)
        try:
            domain = [('code', '=ilike', str(property_stock_journal).split(' ')[0] + '%')]
            p_stj = request.env['account.account'].search(domain).id
        except KeyError as e:
            msg = "property_cost_method with %s Cannot Be Found in Database " % property_cost_method
            return request.make_json_response(msg)
        try:
            domain = [
                ('code', '=ilike', str(property_stock_account_input_categ_id).split(' ')[0] + '%')]
            p_input_categ = self.env['account.account'].search(domain).id
        except KeyError as e:
            msg = "property_stock_account_input_categ_id with %s Cannot Be Found in Database " % property_stock_account_input_categ_id
            return request.make_json_response(msg)
        try:
            domain = [
                ('code', '=ilike', str(property_stock_valuation_account_id).split(' ')[0] + '%')]
            p_stock_val = request.env['account.account'].search(domain).id
        except KeyError as e:
            msg = "property_stock_account_input_categ_id with %s Cannot Be Found in Database " % property_stock_account_input_categ_id
            return request.make_json_response(msg)
        try:
            domain = [
                ('code', '=ilike', str(property_stock_account_output_categ_id).split(' ')[0] + '%')]
            p_output_categ = request.env['account.account'].search(domain).id
        except KeyError as e:
            msg = "property_stock_account_output_categ_id with %s Cannot Be Found in Database " % property_stock_account_output_categ_id
            return request.make_json_response(msg)
        try:
            myprodcat = request.env['product.category'].search([('name','=',namacateg)])
            if myprodcat:
                for allcateg in myprodcat:
                    allcateg.write({
                        'name': namacateg,
                        'complete_name': complete_name,
                        'parent_id': categ_id,
                        'parent_path': parent_path,
                        'route_ids': [(6, 0, route_ids)],
                        'removal_strategy_id': removal_strategy_id,
                        'total_route_ids': total_route_ids,
                        'putaway_rule_ids': putaway_rule_ids,
                        'property_account_income_categ_id': a_income_categ,
                        'property_account_expense_categ_id': a_expense_categ,
                        'property_account_creditor_price_difference_categ': a_c_d,
                        'property_valuation': p_Value,
                        'property_cost_method': p_Cost,
                        'property_stock_journal': p_stj,
                        'property_stock_account_input_categ_id': p_input_categ,
                        'property_stock_account_output_categ_id': p_output_categ,
                        'property_stock_valuation_account_id': p_stock_val,
                        'total_group_ids': total_group_ids,
                        'categ_seq': categ_seq,
                        'display_name': display_name,
                    })
            else:
                myprodcat.create({
                        'name': namacateg,
                        'complete_name': complete_name,
                        'parent_id': categ_id,
                        'parent_path': parent_path,
                        'route_ids': [(6, 0, route_ids)],
                        'removal_strategy_id': removal_strategy_id,
                        'total_route_ids': total_route_ids,
                        'putaway_rule_ids': putaway_rule_ids,
                        'property_account_income_categ_id': a_income_categ,
                        'property_account_expense_categ_id': a_expense_categ,
                        'property_account_creditor_price_difference_categ': a_c_d,
                        'property_valuation': p_Value,
                        'property_cost_method': p_Cost,
                        'property_stock_journal': p_stj,
                        'property_stock_account_input_categ_id': p_input_categ,
                        'property_stock_account_output_categ_id': p_output_categ,
                        'property_stock_valuation_account_id': p_stock_val,
                        'total_group_ids': total_group_ids,
                        'categ_seq': categ_seq,
                        'display_name': display_name,
                    })
        except KeyError as e:
            msg = "'Update Or Create Product Category For Name %s Error." % namacateg
            return self.make_json_response(msg)
        msg = 'Update Or Create Product Category For Name %s Success' % namacateg
        return self.make_json_response(msg)

    @http.route('/stock-warehouse-api', type='json', auth="user", methods=['POST'], csrf=False)
    def insert_master_warehouses_data(self, **params):
        try:
            name = request.jsonrequest.get('name')
        except KeyError as e:
            msg = "Missing Field Name In Database `%s`" %'stock.warehouse'
            return self.make_json_response(msg)
        try:
            active = request.jsonrequest.get('active')
        except KeyError as e:
            msg = "Missing Field active In Database `%s`" % 'stock.warehouse'
            return self.make_json_response(msg)
        try:
            company_id = request.jsonrequest.get('company_id')
        except KeyError as e:
            msg = "Missing Field company_id In Database `%s`" % 'stock.warehouse'
            return self.make_json_response(msg)
        try:
            partner_id = request.jsonrequest.get('partner_id')
        except KeyError as e:
            msg = "Missing Field partner_id In Database `%s`" % 'stock.warehouse'
            return self.make_json_response(msg)
        try:
            view_location_id = request.jsonrequest.get('view_location_id')
        except KeyError as e:
            msg = "Missing Field view_location_id In Database `%s`" % 'stock.warehouse'
            return self.make_json_response(msg)
        try:
            lot_stock_id = request.jsonrequest.get('lot_stock_id')
        except KeyError as e:
            msg = "Missing Field lot_stock_id In Database `%s`" % 'stock.warehouse'
            return self.make_json_response(msg)
        try:
            code = request.jsonrequest.get('code')
        except KeyError as e:
            msg = "Missing Field code In Database `%s`" % 'stock.warehouse'
            return self.make_json_response(msg)
        try:
            reception_steps = request.jsonrequest.get('reception_steps')
        except KeyError as e:
            msg = "Missing Field reception_steps In Database `%s`" % 'stock.warehouse'
            return self.make_json_response(msg)
        try:
            delivery_steps = request.jsonrequest.get('delivery_steps')
        except KeyError as e:
            msg = "Missing Field delivery_steps In Database `%s`" % 'stock.warehouse'
            return self.make_json_response(msg)
        try:
            wh_input_stock_loc_id = request.jsonrequest.get('wh_input_stock_loc_id')
        except KeyError as e:
            msg = "Missing Field wh_input_stock_loc_id In Database `%s`" % 'stock.warehouse'
            return self.make_json_response(msg)
        try:
            wh_qc_stock_loc_id = request.jsonrequest.get('wh_qc_stock_loc_id')
        except KeyError as e:
            msg = "Missing Field wh_qc_stock_loc_id In Database `%s`" % 'stock.warehouse'
            return self.make_json_response(msg)
        try:
            wh_output_stock_loc_id = request.jsonrequest.get('wh_output_stock_loc_id')
        except KeyError as e:
            msg = "Missing Field wh_output_stock_loc_id In Database `%s`" % 'stock.warehouse'
            return self.make_json_response(msg)
        try:
            wh_pack_stock_loc_id = request.jsonrequest.get('wh_pack_stock_loc_id')
        except KeyError as e:
            msg = "Missing Field wh_pack_stock_loc_id In Database `%s`" % 'stock.warehouse'
            return self.make_json_response(msg)
        try:
            pick_type_id = request.jsonrequest.get('pick_type_id')
        except KeyError as e:
            msg = "Missing Field pick_type_id In Database `%s`" % 'stock.warehouse'
            return self.make_json_response(msg)
        try:
            pack_type_id = request.jsonrequest.get('pack_type_id')
        except KeyError as e:
            msg = "Missing Field pack_type_id In Database `%s`" % 'stock.warehouse'
            return self.make_json_response(msg)
        try:
            out_type_id = request.jsonrequest.get('out_type_id')
        except KeyError as e:
            msg = "Missing Field out_type_id In Database `%s`" % 'stock.warehouse'
            return self.make_json_response(msg)
        try:
            int_type_id = request.jsonrequest.get('int_type_id')
        except KeyError as e:
            msg = "Missing Field int_type_id In Database `%s`" % 'stock.warehouse'
            return self.make_json_response(msg)
        try:
           show_resupply = request.jsonrequest.get('show_resupply')
        except KeyError as e:
            msg = "Missing Field show_resupply In Database `%s`" % 'stock.warehouse'
            return self.make_json_response(msg)
        try:
            sequence = request.jsonrequest.get('sequence')
        except KeyError as e:
            msg = "Missing Field sequence In Database `%s`" % 'stock.warehouse'
            return self.make_json_response(msg)
        try:
            manufacture_to_resupply = request.jsonrequest.get('manufacture_to_resupply')
        except KeyError as e:
            msg = "Missing Field manufacture_to_resupply In Database `%s`" % 'stock.warehouse'
            return self.make_json_response(msg)
        try:
            manu_type_id = request.jsonrequest.get('manu_type_id')
        except KeyError as e:
            msg = "Missing Field manu_type_id In Database `%s`" % 'stock.warehouse'
            return self.make_json_response(msg)
        try:
            pbm_type_id = request.jsonrequest.get('pbm_type_id')
        except KeyError as e:
            msg = "Missing Field pbm_type_id In Database `%s`" % 'stock.warehouse'
            return self.make_json_response(msg)
        try:
            sam_type_id = request.jsonrequest.get('sam_type_id')
        except KeyError as e:
            msg = "Missing Field sam_type_id In Database `%s`" % 'stock.warehouse'
            return self.make_json_response(msg)
        try:
            manufacture_steps = request.jsonrequest.get('manufacture_steps')
        except KeyError as e:
            msg = "Missing Field manufacture_steps In Database `%s`" % 'stock.warehouse'
            return self.make_json_response(msg)
        try:
            pbm_loc_id = request.jsonrequest.get('pbm_loc_id')
        except KeyError as e:
            msg = "Missing Field pbm_loc_id In Database `%s`" % 'stock.warehouse'
            return self.make_json_response(msg)
        try:
            sam_loc_id = request.jsonrequest.get('sam_loc_id')
        except KeyError as e:
            msg = "Missing Field sam_loc_id In Database `%s`" % 'stock.warehouse'
            return self.make_json_response(msg)
        try:
            buy_to_resupply = request.jsonrequest.get('buy_to_resupply')
        except KeyError as e:
            msg = "Missing Field buy_to_resupply In Database `%s`" % 'stock.warehouse'
            return self.make_json_response(msg)
        try:
            loc_management_id = request.jsonrequest.get('loc_management_id')
        except KeyError as e:
            msg = "Missing Field loc_management_id In Database `%s`" % 'stock.warehouse'
            return self.make_json_response(msg)
        try:
            view_loc = request.env['stock.location'].search([('complete_name', '=', view_location_id)],
                                                         limit=1).id
        except KeyError as e:
            msg = "Cannot Found Location for name %s In Database" % view_location_id
            return self.make_json_response(msg)
        try:
            loc_stock = self.env['stock.location'].search([('complete_name', '=', lot_stock_id)],
                                                          limit=1).id
        except KeyError as e:
            msg = "Cannot Found Location for name %s In Database" % lot_stock_id
            return self.make_json_response(msg)
        try:
            input_stock_loc = request.env['stock.location'].search(
                [('complete_name', '=', wh_input_stock_loc_id)], limit=1).id
        except KeyError as e:
            msg = "Cannot Found Location for name %s In Database" % input_stock_loc
            return self.make_json_response(msg)
        try:
            wh_Qc = self.env['stock.location'].search([('complete_name', '=',wh_qc_stock_loc_id)],
                                                      limit=1).id
        except KeyError as e:
            msg = "Cannot Found Location for name %s In Database" % lot_stock_id
            return self.make_json_response(msg)
        try:
            wh_output = request.env['stock.location'].search(
                [('complete_name', '=', wh_output_stock_loc_id)], limit=1).id
        except KeyError as e:
            msg = "Cannot Found Location for name %s In Database" % wh_output_stock_loc_id
            return self.make_json_response(msg)
        try:
            wh_pack = request.env['stock.location'].search(
                [('complete_name', '=', wh_pack_stock_loc_id)], limit=1).id
        except KeyError as e:
            msg = "Cannot Found Location for name %s In Database" % wh_output_stock_loc_id
            return self.make_json_response(msg)
        try:
            sam_loc_id = self.env['stock.location'].search([('complete_name', '=',sam_loc_id)],
                                                           limit=1).id
        except KeyError as e:
            msg = "Cannot Found Location for name %s In Database" % sam_loc_id
            return self.make_json_response(msg)
        try:
            pbm_loc_id = self.env['stock.location'].search([('complete_name', '=', pbm_loc_id)],
                                                           limit=1).id
        except KeyError as e:
            msg = "Cannot Found Location for name %s In Database" % pbm_loc_id
            return self.make_json_response(msg)
        try:
            loc_mgmt = self.env['stock.location'].search([('complete_name', '=', loc_management_id)],
                                                         limit=1).id
        except KeyError as e:
            msg = "Cannot Found Location for name %s In Database" % loc_management_id
            return self.make_json_response(msg)
        try:
            domain = ['|', ('name', 'ilike', int_type_id),
                      ('warehouse_id.name', 'ilike',int_type_id)]
            in_type_id = request.env['stock.picking.type'].search(domain, limit=1).id
        except KeyError as e:
            msg = "Cannot Found Stock Picking Type %s In Database" % loc_management_id
            return self.make_json_response(msg)
        try:
            domain = ['|', ('name', 'ilike', pick_type_id),
                      ('warehouse_id.name', 'ilike', pick_type_id)]
            pick_type_id = self.env['stock.picking.type'].search(domain, limit=1).id
        except KeyError as e:
            msg = "Cannot Found Stock Picking Type %s In Database" % pick_type_id
            return self.make_json_response(msg)
        try:
            domain = ['|', ('name', 'ilike', pack_type_id),
                      ('warehouse_id.name', 'ilike', pack_type_id)]
            pack_type_id = self.env['stock.picking.type'].search(domain, limit=1).id
        except KeyError as e:
            msg = "Cannot Found Stock Picking Type %s In Database" % pack_type_id
            return self.make_json_response(msg)
        try:
            domain = ['|', ('name', 'ilike', out_type_id),
                      ('warehouse_id.name', 'ilike',out_type_id)]
            out_type_id = request.env['stock.picking.type'].search(domain, limit=1).id
        except KeyError as e:
            msg = "Cannot Found Stock Picking Type %s In Database" % pack_type_id
            return self.make_json_response(msg)
        try:
            domain = ['|', ('name', 'ilike', sam_type_id),
                      ('warehouse_id.name', 'ilike', sam_type_id)]
            sam_type_id = self.env['stock.picking.type'].search(domain, limit=1).id
        except KeyError as e:
            msg = "Cannot Found Stock Picking Type %s In Database" % sam_type_id
            return self.make_json_response(msg)
        try:
            domain = ['|', ('name', 'ilike', pbm_type_id),
                      ('warehouse_id.name', 'ilike',pbm_type_id)]
            pbm_type_id = self.env['stock.picking.type'].search(domain, limit=1).id
        except KeyError as e:
            msg = "Cannot Found Stock Picking Type %s In Database" % pbm_type_id
            return self.make_json_response(msg)
        try:
            domain = ['|', ('name', 'ilike', manu_type_id),
                      ('warehouse_id.name', 'ilike', manu_type_id)]
            manu_type_id = self.env['stock.picking.type'].search(domain, limit=1).id
        except KeyError as e:
            msg = "Cannot Found Stock Picking Type %s In Database" % pbm_type_id
            return self.make_json_response(msg)
        try:
            rescom = request.env['res.company'].search([('name', '=', company_id)]).id
        except KeyError as e:
            msg = "Cannot Found Company With Name %s In Database" % company_id
            return self.make_json_response(msg)
        try:
            respart = self.env['res.partner'].search([('name', '=', partner_id)]).id
        except KeyError as e:
            msg = "Cannot Found Partner With Name %s In Database" % company_id
            return self.make_json_response(msg)
        try:
            mywarehouse = request.env['stock.warehouse'].search(
                [('name', '=', name)])
            if mywarehouse:
                for allwh in mywarehouse:
                    allwh.write({
                        'name': name,
                        'active': active,
                        'company_id': rescom,
                        'partner_id': respart,
                        'view_location_id': view_loc,
                        'lot_stock_id': loc_stock,
                        'code': code,
                        'reception_steps': reception_steps,
                        'delivery_steps': delivery_steps,
                        'wh_input_stock_loc_id': input_stock_loc,
                        'wh_qc_stock_loc_id': wh_Qc,
                        'wh_output_stock_loc_id': wh_output,
                        'wh_pack_stock_loc_id': wh_pack,
                        'pick_type_id': pick_type_id,
                        'pack_type_id': pack_type_id,
                        'out_type_id': out_type_id,
                        'int_type_id': in_type_id,
                        'show_resupply': show_resupply,
                        'sequence': sequence,
                        'manufacture_to_resupply': manufacture_to_resupply,
                        'manu_type_id': manu_type_id,
                        'pbm_type_id': pbm_type_id,
                        'sam_type_id': sam_type_id,
                        'manufacture_steps': manufacture_steps,
                        'pbm_loc_id': pbm_loc_id,
                        'sam_loc_id': sam_loc_id,
                        'buy_to_resupply': buy_to_resupply,
                        'loc_management_id': loc_mgmt,
                    })
            else:
                mywarehouse.create({
                    'name': name,
                    'active': active,
                    'company_id': rescom,
                    'partner_id': respart,
                    'view_location_id': view_loc,
                    'lot_stock_id': loc_stock,
                    'code': code,
                    'reception_steps': reception_steps,
                    'delivery_steps': delivery_steps,
                    'wh_input_stock_loc_id': input_stock_loc,
                    'wh_qc_stock_loc_id': wh_Qc,
                    'wh_output_stock_loc_id': wh_output,
                    'wh_pack_stock_loc_id': wh_pack,
                    'pick_type_id': pick_type_id,
                    'pack_type_id': pack_type_id,
                    'out_type_id': out_type_id,
                    'int_type_id': in_type_id,
                    'show_resupply': show_resupply,
                    'sequence': sequence,
                    'manufacture_to_resupply': manufacture_to_resupply,
                    'manu_type_id': manu_type_id,
                    'pbm_type_id': pbm_type_id,
                    'sam_type_id': sam_type_id,
                    'manufacture_steps': manufacture_steps,
                    'pbm_loc_id': pbm_loc_id,
                    'sam_loc_id': sam_loc_id,
                    'buy_to_resupply': buy_to_resupply,
                    'loc_management_id': loc_mgmt,
                })
        except KeyError as e:
            msg = "Update Or Create Stock Warehouse For Name %s Error." % name
            return self.make_json_response(msg)
        msg = 'Update Or Create Stock  Warehouse For Name %s Success' % name
        return self.make_json_response(msg)

    @http.route('/stock-location-api', type='json', auth="user", methods=['POST'], csrf=False)
    def insert_stock_location_datas(self, **params):
        try:
            name= request.jsonrequest.get('name')
        except KeyError as e:
            msg = "Missing Field sam_loc_id In Database `%s`" % 'stock.warehouse'
            return self.make_json_response(msg)
        try:
            complete_name= request.jsonrequest.get('complete_name')
        except KeyError as e:
            msg = "Missing Field complete_name In Database `%s`" % 'stock.warehouse'
            return self.make_json_response(msg)
        try:
            active= request.jsonrequest.get('active')
        except KeyError as e:
            msg = "Missing Field active In Database `%s`" % 'stock.warehouse'
            return self.make_json_response(msg)
        try:
            usage= request.jsonrequest.get('usage')
        except KeyError as e:
            msg = "Missing Field usage In Database `%s`" % 'stock.warehouse'
            return self.make_json_response(msg)
        try:
            location_id= request.jsonrequest.get('location_id')
        except KeyError as e:
            msg = "Missing Field location_id In Database `%s`" % 'stock.warehouse'
            return self.make_json_response(msg)
        try:
            comment= request.jsonrequest.get('comment')
        except KeyError as e:
            msg = "Missing Field comment In Database `%s`" % 'stock.warehouse'
            return self.make_json_response(msg)
        try:
            posx= request.jsonrequest.get('posx')
        except KeyError as e:
            msg = "Missing Field sam_loc_id In Database `%s`" % 'stock.warehouse'
            return self.make_json_response(msg)
        try:
            posy= request.jsonrequest.get('posy')
        except KeyError as e:
            msg = "Missing Field sam_loc_id In Database `%s`" % 'stock.warehouse'
            return self.make_json_response(msg)
        try:
            posz= request.jsonrequest.get('posz')
        except KeyError as e:
            msg = "Missing Field posz In Database `%s`" % 'stock.warehouse'
            return self.make_json_response(msg)
        try:
            parent_path= request.jsonrequest.get('parent_path')
        except KeyError as e:
            msg = "Missing Field parent_path In Database `%s`" % 'stock.warehouse'
            return self.make_json_response(msg)
        try:
            company_id= request.jsonrequest.get('company_id')
        except KeyError as e:
            msg = "Missing Field company_id In Database `%s`" % 'stock.warehouse'
            return self.make_json_response(msg)
        try:
            scrap_location= request.jsonrequest.get('scrap_location')
        except KeyError as e:
            msg = "Missing Field scrap_location In Database `%s`" % 'stock.warehouse'
            return self.make_json_response(msg)
        try:
            return_location= request.jsonrequest.get('return_location')
        except KeyError as e:
            msg = "Missing Field return_location In Database `%s`" % 'stock.warehouse'
            return self.make_json_response(msg)
        try:
            removal_strategy_id= request.jsonrequest.get('removal_strategy_id')
        except KeyError as e:
            msg = "Missing Field removal_strategy_id In Database `%s`" % 'stock.warehouse'
            return self.make_json_response(msg)
        try:
            barcode= request.jsonrequest.get('barcode')
        except KeyError as e:
            msg = "Missing Field barcode In Database `%s`" % 'stock.warehouse'
            return self.make_json_response(msg)
        try:
            warehouse_id= request.jsonrequest.get('warehouse_id')
        except KeyError as e:
            msg = "Missing Field warehouse_id In Database `%s`" % 'stock.warehouse'
            return self.make_json_response(msg)
        try:
            analytic_id= request.jsonrequest.get('analytic_id')
        except KeyError as e:
            msg = "Missing Field analytic_id In Database `%s`" % 'stock.warehouse'
            return self.make_json_response(msg)
        try:
            display_name= request.jsonrequest.get('display_name')
        except KeyError as e:
            msg = "Missing Field display_name In Database `%s`" % 'stock.warehouse'
            return self.make_json_response(msg)
        try:
            ana_id = request.env['account.analytic.default'].search(
                [('analytic_id.name', '=', analytic_id)])
        except KeyError as e:
            msg = "Cannot Found Analytic name For %s In Database " % 'stock.warehouse'
            return self.make_json_response(msg)
        try:
            wh_id = request.env['stock.warehouse'].search([('name', '=', warehouse_id)], limit=1).id
        except KeyError as e:
            msg = "Cannot Found Warehouse For Name '%s'  In Database" % warehouse_id
            return self.make_json_response(msg)
        try:
            loc_id = request.env['stock.location'].search([('complete_name', '=', location_id)],
                                                       limit=1).id
        except KeyError as e:
            msg = "Cannot Found Location For Name '%s'  In Database" % location_id
            return self.make_json_response(msg)
        try:
            rescom = request.env['res.company'].search([('name', '=', company_id)]).id
        except KeyError as e:
            msg = "Cannot Found Location For Name '%s'  In Database" % location_id
            return self.make_json_response(msg)
        try:
            slock_obj = request.env['stock.location'].search(
                [('name', '=',name)], limit=1)
            if slock_obj:
                for alloc in slock_obj:
                    slock_obj.write({
                        'name': name,
                        'complete_name': complete_name,
                        'active': active,
                        'usage': usage,
                        'location_id': loc_id,
                        'comment': comment,
                        'posx': posx,
                        'posy': posy,
                        'posz': posz,
                        'parent_path': parent_path,
                        'company_id': rescom,
                        'scrap_location': scrap_location,
                        'return_location': return_location,
                        'removal_strategy_id': removal_strategy_id,
                        'barcode': barcode,
                        'warehouse_id': wh_id,
                        'analytic_id': ana_id,
                        'display_name': display_name,
                    })
            else:
                slock_obj.create({
                     'name': name,
                     'complete_name': complete_name,
                     'active': active,
                     'usage': usage,
                     'location_id': loc_id,
                     'comment': comment,
                     'posx': posx,
                     'posy': posy,
                     'posz': posz,
                     'parent_path': parent_path,
                     'company_id': rescom,
                     'scrap_location': scrap_location,
                     'return_location': return_location,
                     'removal_strategy_id': removal_strategy_id,
                     'barcode': barcode,
                     'warehouse_id': wh_id,
                     'analytic_id': ana_id,
                     'display_name': display_name,
                })
        except KeyError as e:
            msg = "Update Or Create Product Category For Name %s Error." % name
            return self.make_json_response(msg)
        msg = 'Update Or Create Product Category For Name %s Success' % name
        return self.make_json_response(msg)

    @http.route('/stock-operation-type-api', type='json', auth="user", methods=['POST'], csrf=False)
    def insert_model_op_type_data(self, **params):
        try:
            namacateg = request.jsonrequest.get('name')
        except KeyError as e:
            msg = "Field Name For Database `%s` does not exist." % 'product.category'
            return self.make_json_response(msg)
        try:
            prod_categ= request.env['product.category'].search([('name','=',namacateg)])
            if not prod_categ:
                prod_categ.create({'name': namacateg})
            else:
                prod_categ.write({'name': namacateg})
        except KeyError as e:
            msg = "Data Product Category For Name %s does not exist." % namacateg
            return self.make_json_response(msg)
        msg = 'Update Or Create Product Category For Name %s Success' % namacateg
        return self.make_json_response(msg)

    @http.route('/stock-routes-api', type='json', auth="user", methods=['POST'], csrf=False)
    def insert_model_stock_routes_data(self, **params):
        try:
            namacateg = request.jsonrequest.get('name')
        except KeyError as e:
            msg = "Field Name For Database `%s` does not exist." % 'product.category'
            return self.make_json_response(msg)
        try:
            prod_categ= request.env['product.category'].search([('name','=',namacateg)])
            if not prod_categ:
                prod_categ.create({'name': namacateg})
            else:
                prod_categ.write({'name': namacateg})
        except KeyError as e:
            msg = "Data Product Category For Name %s does not exist." % namacateg
            return self.make_json_response(msg)
        msg = 'Update Or Create Product Category For Name %s Success' % namacateg
        return self.make_json_response(msg)

    @http.route('/analiatic-api', type='json', auth="user", methods=['POST'], csrf=False)
    def insert_model_analitic_data(self, **params):
        try:
            namacateg = request.jsonrequest.get('name')
        except KeyError as e:
            msg = "Field Name For Database `%s` does not exist." % 'product.category'
            return self.make_json_response(msg)
        try:
            prod_categ= request.env['product.category'].search([('name','=',namacateg)])
            if not prod_categ:
                prod_categ.create({'name': namacateg})
            else:
                prod_categ.write({'name': namacateg})
        except KeyError as e:
            msg = "Data Product Category For Name %s does not exist." % namacateg
            return self.make_json_response(msg)
        msg = 'Update Or Create Product Category For Name %s Success' % namacateg
        return self.make_json_response(msg)

    @http.route('/stock-rules-api', type='json', auth="user", methods=['POST'], csrf=False)
    def insert_model_stock_rulesdata(self, **params):
        try:
            namacateg = request.jsonrequest.get('name')
        except KeyError as e:
            msg = "Field Name For Database `%s` does not exist." % 'product.category'
            return self.make_json_response(msg)
        try:
            prod_categ= request.env['product.category'].search([('name','=',namacateg)])
            if not prod_categ:
                prod_categ.create({'name': namacateg})
            else:
                prod_categ.write({'name': namacateg})
        except KeyError as e:
            msg = "Data Product Category For Name %s does not exist." % namacateg
            return self.make_json_response(msg)
        msg = 'Update Or Create Product Category For Name %s Success' % namacateg
        return self.make_json_response(msg)


    @http.route('/stock-putaway-rules-api', type='json', auth="user", methods=['POST'], csrf=False)
    def insert_model_stock_putaway_rules_data(self, **params):
        try:
            namacateg = request.jsonrequest.get('name')
        except KeyError as e:
            msg = "Field Name For Database `%s` does not exist." % 'product.category'
            return self.make_json_response(msg)
        try:
            prod_categ= request.env['product.category'].search([('name','=',namacateg)])
            if not prod_categ:
                prod_categ.create({'name': namacateg})
            else:
                prod_categ.write({'name': namacateg})
        except KeyError as e:
            msg = "Data Product Category For Name %s does not exist." % namacateg
            return self.make_json_response(msg)
        msg = 'Update Or Create Product Category For Name %s Success' % namacateg
        return self.make_json_response(msg)

    @http.route('/product-uom-api', type='json', auth="user", methods=['POST'], csrf=False)
    def insert_model_product_uom_data(self, **params):
        try:
            nama_uom =  request.jsonrequest.get('name')
        except KeyError as e:
            msg = "Missing Field Name For Database `%s` does not exist." % 'uom.uom'
            return self.make_json_response(msg)
        try:
            categ_id = request.jsonrequest.get('category_id')
        except KeyError as e:
            msg = "Missing Field Category ID  For Database `%s` does not exist." % 'uom.uom'
            return self.make_json_response(msg)
        try:
            faktor = request.jsonrequest.get('factor')
        except KeyError as e:
            msg = "Missing Field factor  For Database `%s` does not exist." % 'uom.uom'
            return self.make_json_response(msg)
        try:
            faktorinv = request.jsonrequest.get('factor_inv')
        except KeyError as e:
            msg = "Missing Field factor_inv  For Database `%s` does not exist." % 'uom.uom'
            return self.make_json_response(msg)
        try:
            rounding = request.jsonrequest.get('rounding')
        except KeyError as e:
            msg = "Missing Field rounding  For Database `%s` does not exist." % 'uom.uom'
            return self.make_json_response(msg)
        try:
            active = request.jsonrequest.get('active')
        except KeyError as e:
            msg = "Missing Field active  For Database `%s` does not exist." % 'uom.uom'
            return self.make_json_response(msg)
        try:
            uom_type = request.jsonrequest.get('uom_type')
        except KeyError as e:
            msg = "Missing Field uom_type  For Database `%s` does not exist." % 'uom.uom'
            return self.make_json_response(msg)
        try:
            measure_type = request.jsonrequest.get('measure_type')
        except KeyError as e:
            msg = "Missing Field measure_type  For Database `%s` does not exist." % 'uom.uom'
            return self.make_json_response(msg)
        try:
            display_name = request.jsonrequest.get('display_name')
        except KeyError as e:
            msg = "Missing Field display_name  For Database `%s` does not exist." % 'uom.uom'
            return self.make_json_response(msg)
        try:
            categ_obj = self.env['uom.category']
            uom_categ = request.env['product.category'].search([('name', '=', categ_id)]).id
        except KeyError as e:
            msg = "Field Category ID  For Database `%s` does not exist." % 'uom.uom'
            return self.make_json_response(msg)
        try:
            uom_obj = request.env['uom.uom'].search(
                [('name', '=', nama_uom)], limit=1)
            if uom_obj:
                uom_obj.write({
                    'name': nama_uom,
                    'category_id': categ_id,
                    'factor': faktor,
                    'factor_inv': faktorinv,
                    'rounding': rounding,
                    'active': active,
                    'uom_type': uom_type,
                    'measure_type': measure_type,
                    'display_name': display_name,
                })
            else:
                uom_obj.create({
                    'name': nama_uom,
                    'category_id': categ_id,
                    'factor': faktor,
                    'factor_inv': faktorinv,
                    'rounding': rounding,
                    'active': active,
                    'uom_type': uom_type,
                    'measure_type': measure_type,
                    'display_name': display_name,
                })
        except KeyError as e:
            msg = "Update Or Create Product UOM For Name %s Error" % nama_uom
            return self.make_json_response(msg)
        msg = "Update Or Create Product UOM For Name %s Success" % nama_uom
        return self.make_json_response(msg)

    @http.route('/product-uom-categ-api', type='json', auth="user", methods=['POST'], csrf=False)
    def insert_model_product_uom_categ_data(self, **params):
        try:
            namacateg = request.jsonrequest.get('name')
        except KeyError as e:
            msg = "Field Name For Database `%s` does not exist." % 'product.category'
            return self.make_json_response(msg)
        try:
            meastipe = request.jsonrequest.get('measure_type')
        except KeyError as e:
            msg = "Field measure_type For Database `%s` does not exist." % 'product.category'
            return self.make_json_response(msg)
        try:
            prod_categ= request.env['product.category'].search([('name','=',namacateg)])
            if not prod_categ:
                prod_categ.create({
                    'name': namacateg,
                    'measure_type': meastipe,
                })
            else:
                prod_categ.write({
                    'name': namacateg,
                    'measure_type': meastipe,
                })
        except KeyError as e:
            msg = "Update Or Create Product Category For Name %s Error" % namacateg
            return self.make_json_response(msg)
        msg = 'Update Or Create Product Category For Name %s Success' % namacateg
        return self.make_json_response(msg)

    @http.route('/coa-api', type='json', auth="user", methods=['POST'], csrf=False)
    def insert_model_coa_data(self, **params):
        try:
            namacateg = request.jsonrequest.get('name')
        except KeyError as e:
            msg = "Field Name For Database `%s` does not exist." % 'product.category'
            return self.make_json_response(msg)
        try:
            prod_categ= request.env['product.category'].search([('name','=',namacateg)])
            if not prod_categ:
                prod_categ.create({'name': namacateg})
            else:
                prod_categ.write({'name': namacateg})
        except KeyError as e:
            msg = "Data Product Category For Name %s does not exist." % namacateg
            return self.make_json_response(msg)
        msg = 'Update Or Create Product Category For Name %s Success' % namacateg
        return self.make_json_response(msg)

    @http.route('/account-account-type-api', type='json', auth="user", methods=['POST'], csrf=False)
    def insert_model_account_account_type_data(self, **params):
        try:
            namacateg = request.jsonrequest.get('name')
        except KeyError as e:
            msg = "Field Name For Database `%s` does not exist." % 'account.group'
            return self.make_json_response(msg)
        try:
            inbal = request.jsonrequest.get('include_initial_balance')
        except KeyError as e:
            msg = "Field Include Initial balance For Database `%s` does not exist." % 'account.group'
            return self.make_json_response(msg)
        try:
            tipe = request.jsonrequest.get('type')
        except KeyError as e:
            msg = "Field Type For Database `%s` does not exist." % 'account.group'
            return self.make_json_response(msg)
        try:
            intgrp = request.jsonrequest.get('internal_group')
        except KeyError as e:
            msg = "Field internal_group `%s` does not exist." % 'account.group'
            return self.make_json_response(msg)
        try:
            note = request.jsonrequest.get('note')
        except KeyError as e:
            msg = "Field note `%s` does not exist." % 'account.group'
            return self.make_json_response(msg)
        try:
            prod_categ= request.env['account.group'].search([('name','=',namacateg)])
            if not prod_categ:
                prod_categ.create({
                   'name': namacateg,
                   'include_initial_balance': inbal,
                   'type': tipe,
                   'internal_group':intgrp,
                   'note': note,
                })
            else:
                prod_categ.write({
                    'name': namacateg,
                    'include_initial_balance': inbal,
                    'type': tipe,
                    'internal_group': intgrp,
                    'note': note,
                })
        except KeyError as e:
            msg = "Data Account Group For Name %s does not exist." % namacateg
            return self.make_json_response(msg)
        msg = 'Update Or Create Account Group For Name %s Success' % namacateg
        return self.make_json_response(msg)

    @http.route('/account-group-api', type='json', auth="user", methods=['POST'], csrf=False)
    def insert_model_account_group_data(self, **params):
        try:
            namacateg = request.jsonrequest.get('name')
        except KeyError as e:
            msg = "Field Name For Database `%s` does not exist." % 'account.group'
            return self.make_json_response(msg)
        try:
            inbal = request.jsonrequest.get('include_initial_balance')
        except KeyError as e:
            msg = "Field Include Initial balance For Database `%s` does not exist." % 'account.group'
            return self.make_json_response(msg)
        try:
            tipe = request.jsonrequest.get('type')
        except KeyError as e:
            msg = "Field Type For Database `%s` does not exist." % 'account.group'
            return self.make_json_response(msg)
        try:
            intgrp = request.jsonrequest.get('internal_group')
        except KeyError as e:
            msg = "Field internal_group `%s` does not exist." % 'account.group'
            return self.make_json_response(msg)
        try:
            note = request.jsonrequest.get('note')
        except KeyError as e:
            msg = "Field note `%s` does not exist." % 'account.group'
            return self.make_json_response(msg)
        try:
            prod_categ= request.env['account.group'].search([('name','=',namacateg)])
            if not prod_categ:
                prod_categ.create({
                   'name': namacateg,
                   'include_initial_balance': inbal,
                   'type': tipe,
                   'internal_group':intgrp,
                   'note': note,
                })
            else:
                prod_categ.write({
                    'name': namacateg,
                    'include_initial_balance': inbal,
                    'type': tipe,
                    'internal_group': intgrp,
                    'note': note,
                })
        except KeyError as e:
            msg = "Update Or Create Account Group For Name %s Error" % namacateg
            return self.make_json_response(msg)
        msg = 'Update Or Create Account Group For Name %s Success' % namacateg
        return self.make_json_response(msg)