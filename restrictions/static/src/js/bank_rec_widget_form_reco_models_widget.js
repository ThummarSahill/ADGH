/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";
import { useService } from "@web/core/utils/hooks";

import { BankRecWidgetFormRecoModelsWidget } from "@account_accountant/components/bank_reconciliation/bank_rec_widget_form_reco_models_widget";

import { patch } from "@web/core/utils/patch";
const { Component } = owl;
import { session } from "@web/session";
var rpc = require('web.rpc');


patch(BankRecWidgetFormRecoModelsWidget.prototype, 'Button', {
        async selectRecoModel(reco_model_id, already_selected) {
            if (already_selected) {
                this.record.update({ todo_command: `unselect_reconcile_model_button,${reco_model_id}` });
            } else {
                await this.record.update({ todo_command: `select_reconcile_model_button,${reco_model_id}` });

                const line_index = this.record.data.lines_widget.lines.slice(-1)[0].index.value;
                await this.record.update({ todo_command: `select_reconcile_model_button,${reco_model_id}` });
                const analytic_distribution = await rpc.query({
                    model: 'res.users',
                    method: 'search_read',
                    domain: [['id', '=', session.uid]],
                    fields: ['analytic_account_ids'],
                });
                const data= {}
                if (analytic_distribution[0] && analytic_distribution[0]['analytic_account_ids']){
                    if (analytic_distribution[0]['analytic_account_ids'][0]){
                        data[analytic_distribution[0]['analytic_account_ids'][0]] = 100;
                    }
                }
                await this.record.update({ analytic_distribution: data });
                
            }
        }
    });

