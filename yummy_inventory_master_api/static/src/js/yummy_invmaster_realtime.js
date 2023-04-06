// Author => Albertus Restiyanto Pramayudha
// email  => xabre0010@gmail.com
// linkedin => https://www.linkedin.com/in/albertus-restiyanto-pramayudha-470261a8/
// youtube => https://www.youtube.com/channel/UCCtgLDIfqehJ1R8cohMeTXA

odoo.define('yummy_inventory_master_api.realtime_sync', function (require) {
"use strict";
    var BasicController = require('web.BasicController');
    var FormController = require('web.FormController');
    var Dialog = require('web.Dialog');
    var core = require('web.core');
    var rpc = require('web.rpc');
    var _t = core._t;
    var isineditmode = false;
    var isincreate  = false;

    FormController.include({
        init: function (parent, model, renderer, params) {
            this.archiveEnabled = true;
            isineditmode = false;
            this._super.apply(this, arguments);
         },

         _onEdit: function () {
            isineditmode = true;
            this._super.apply(this, arguments);
         },
         _onCreate: function () {
            isincreate  = true;
            this._super.apply(this, arguments);
        },
        _onSave: function (ev) {
            var self = this;
            this._super.apply(this, arguments);
                if (self.modelName =='product.template' || self.modelName=='product.product') {
                    if (isineditmode == true){
                        rpc.query({
                            model: self.modelName,
                            method: 'start_realtime_sync',
                            args: [self.handle,self.getSelectedIds(),false],
                        });
                    }
                } /*else if (self.modelName =='uom.uom') {
                   if (isineditmode == true){
                        rpc.query({
                            model: self.modelName,
                            method: 'start_edit_uom',
                            args: [self.handle,self.getSelectedIds()],
                        });
                    }
                } else if (self.modelName =='product.category') {
                   if (isineditmode == true){
                        rpc.query({
                            model: self.modelName,
                            method: 'start_edit_category',
                            args: [self.handle,self.getSelectedIds()],
                        });
                    }
                }*/
        },
   });
});
