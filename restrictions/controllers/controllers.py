# -*- coding: utf-8 -*-
# from odoo import http


# class Restrictions(http.Controller):
#     @http.route('/restrictions/restrictions', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/restrictions/restrictions/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('restrictions.listing', {
#             'root': '/restrictions/restrictions',
#             'objects': http.request.env['restrictions.restrictions'].search([]),
#         })

#     @http.route('/restrictions/restrictions/objects/<model("restrictions.restrictions"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('restrictions.object', {
#             'object': obj
#         })
