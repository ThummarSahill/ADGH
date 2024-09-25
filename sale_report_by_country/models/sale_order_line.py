# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ProductBrand(models.Model):
    _name = "product.brand"
    _description = "ProductBrand"

    name = fields.Char()


class ProductProduct(models.Model):
    _inherit = "product.product"

    country_id = fields.Many2one(comodel_name="res.country")
    brand_id = fields.Many2one(comodel_name="product.brand")


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    product_country_id = fields.Many2one(related="product_id.country_id")
    brand_id = fields.Many2one(related="product_id.brand_id")
