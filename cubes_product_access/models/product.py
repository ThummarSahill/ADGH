# from odoo import api, fields, models
# from odoo.exceptions import ValidationError
#
#
# class ProductProduct(models.Model):
#     _inherit = 'product.product'
#
#     @api.model_create_multi
#     def create(self, vals_list):
#         if not self.env.user.has_group(
#                 'cubes_product_access.product_management_group_create'):
#             raise ValidationError('You are not allowed to perform this action, Kindly contact the Administrator.')
#         products = super(ProductProduct, self).create(vals_list)
#         return products
#
#
# class ProductTemplate(models.Model):
#     _inherit = 'product.template'
#
#     @api.model_create_multi
#     def create(self, vals_list):
#         if not self.env.user.has_group(
#                 'cubes_product_access.product_management_group_create'):
#             raise ValidationError('You are not allowed to perform this action, Kindly contact the Administrator.')
#         templates = super(ProductTemplate, self).create(vals_list)
#         return templates
#
#
# class ProductProduct(models.Model):
#     _inherit = 'product.product'
#
#     @api.model_create_multi
#     def create(self, vals):
#         if not self.env.user.has_group('cubes_product_access.product_management_group_create'):
#             raise ValidationError("You are not allowed to perform this action, Kindly contact the Administrator.")
#         return super(ProductProduct, self).create(vals)
