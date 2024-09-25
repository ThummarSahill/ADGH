from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = "sale.order"



    def action_confirm(self):
        for elem in self:
            error_massage = ''
            negative_sales_user = self.env.user.has_group('cubes_negative_stock.negative_stock_sale_group')
            if not elem.warehouse_id:
                raise ValidationError('يرجى اختيار مخزن!')
            if elem.order_line:
                for each_line in elem.order_line:
                    if (each_line.product_id.detailed_type == 'product') and (each_line.product_uom_qty > 0):## Make sure product is storable
                        count = self.env['stock.quant'].search([('product_id','=',each_line.product_id.id),('location_id','=',elem.warehouse_id.lot_stock_id.id)])
                        if count.quantity < each_line.product_uom_qty and not negative_sales_user:
                            error_massage+= ("لا يوجد كمية كافية من المنتج  ("+str(each_line.product_id.name)+')\n'+"الكمية المتاحة : "+str(count.quantity))
                            error_massage+='\n'
            if error_massage:
                raise ValidationError(error_massage)
        return super(SaleOrder, self).action_confirm()