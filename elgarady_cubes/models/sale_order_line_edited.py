# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.onchange('product_id')
    def get_qty_available_forcasted(self):
        for elem in self:
            purchase_quantity = 0
            elem.qty_available_forcasted = '0'
            if elem.product_id:
                quantity_count_purchase = self.env['purchase.order.line'].search([('state','=', 'purchase'), ('product_id','=',elem.product_id.id)])
                for ele in quantity_count_purchase:
                    purchase_quantity +=ele.product_qty
                    for rec in ele.order_id.picking_ids:
                        for move in rec.move_ids_without_package:
                            if move.product_id.id == elem.product_id.id:
                                purchase_quantity-=move.quantity_done
                elem.qty_available_forcasted = str(purchase_quantity)
            else:
                elem.qty_available_forcasted = '0'
                    # t_quantity.update({ele.product_qty: 0})
                    # t_quantity[ele.product_qty] += ele.product_qty
                # print(t_quantity)
                # poname = self.env['purchase.order'].search(
                #     [('state', '=', 'purchase'), ('product_id', '=', elem.product_id.id)])
                # tt_name= {}
                # for po in poname:
                #     print(po.order_line)
                #     # tt_name.update({po.name :po.order_line.product_qty})
                #     for pp in po.order_line:
                #         tt_name.setdefault(po.name ,0)
                #         tt_name[po.name]+=pp.product_qty
                # for item in tt_name:
                #     purchase_quantity_text = purchase_quantity_text + ' ** ' + item + ': ' + str(tt_name[item])
                # elem.qty_available_forcasted = purchase_quantity_text

    # qty_other_stock_available = fields.Float(string="ALL WHs Quantity",compute='get_qty_other_stock_available')
    qty_available_forcasted = fields.Text(string="الكمية في الطريق",compute='get_qty_available_forcasted')

    warehouse_quantity1 = fields.Text(related='product_id.warehouse_quantity', string='الكمية المتاحة')


class ProductTemplate(models.Model):
    _inherit = "product.template"

    warehouse_quantity = fields.Text(compute='_get_warehouse_quantity', string='Quantity per warehouse')

    def _get_warehouse_quantity(self):
        for record in self:
            warehouse_quantity_text = ''
            record.warehouse_quantity = ''
            product_id = self.env['product.product'].sudo().search([('product_tmpl_id', '=', record.id)])
            if product_id:
                quant_ids = self.env['stock.quant'].sudo().search([('product_id','=',product_id[0].id),('location_id.usage','=','internal')])
                t_warehouses = {}
                for quant in quant_ids:
                    if quant.location_id:
                        if quant.location_id not in t_warehouses:
                            t_warehouses.update({quant.location_id:0})
                        t_warehouses[quant.location_id] += quant.quantity

                tt_warehouses = {}
                for location in t_warehouses:
                    warehouse = False
                    location1 = location
                    while (not warehouse and location1):
                        warehouse_id = self.env['stock.warehouse'].sudo().search([('lot_stock_id','=',location1.id)])
                        if len(warehouse_id) > 0:
                            warehouse = True
                        else:
                            warehouse = False
                        location1 = location1.location_id
                    if warehouse_id:
                        if warehouse_id.name not in tt_warehouses:
                            tt_warehouses.update({warehouse_id.name:0})
                        tt_warehouses[warehouse_id.name] += t_warehouses[location]

                for item in tt_warehouses:
                    if tt_warehouses[item] != 0:
                        warehouse_quantity_text =  warehouse_quantity_text + '\n' + item + ': ' + str(tt_warehouses[item])
                record.warehouse_quantity = warehouse_quantity_text

