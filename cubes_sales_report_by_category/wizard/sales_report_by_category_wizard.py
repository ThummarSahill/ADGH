from operator import itemgetter
from odoo import models, fields, api, _
import io
import base64
import datetime


class SalesReportByCategory(models.TransientModel):
    _name = "sale.category.report"

    start_date = fields.Datetime(string="Start Date", required=True)
    end_date = fields.Datetime(string="End Date", required=True)
    category_ids = fields.Many2many("product.category", string="Product Category")
    select_products = fields.Boolean(default=False)
    product_ids = fields.Many2many("product.product", string="Products")

    def action_print(self):
        data = self.read()[0]
        datas = {"ids": [], "model": "sale.category.report", "form": data}
        return {
            "data": data,
            "type": "ir.actions.report",
            "report_name": "cubes_sales_report_by_category.sale_report_cate_xlsx",
            "report_type": "xlsx",
            "report_file": "Excel Sales Report By Category Sheet.xlsx",
        }


class SalesReportByProductCategoryXlsx(models.AbstractModel):
    _name = "report.cubes_sales_report_by_category.sale_report_cate_xlsx"
    _inherit = "report.report_xlsx.abstract"

    def generate_xlsx_report(self, workbook, data, wizard):
        report_name = "Sale Report By Category"
        worksheet = workbook.add_worksheet(report_name[:31])

        worksheet.set_column("A:A", 35)
        worksheet.set_column("B:B", 20)
        worksheet.set_column("C:C", 20)
        worksheet.set_column("D:D", 25)
        worksheet.set_column("E:E", 20)
        worksheet.set_column("F:F", 30)
        worksheet.set_column("G:G", 20)
        worksheet.set_column("H:H", 20)
        worksheet.set_column("I:I", 20)
        worksheet.set_column("J:J", 20)
        worksheet.set_column("K:K", 20)
        worksheet.set_column("L:L", 20)
        worksheet.set_column("M:M", 20)
        worksheet.set_column("N:N", 20)
        worksheet.set_column("O:O", 20)
        worksheet.set_column("P:P", 20)
        worksheet.set_column("Q:Q", 20)
        worksheet.set_column("R:R", 20)
        worksheet.set_column("S:S", 20)

        head = workbook.add_format({"align": "center", "bold": True, "border": 1, "bg_color": "eeeeee"})
        table_head = workbook.add_format({"align": "left", "bold": True, "border": 1, "bg_color": "eeeeee"})
        table_line = workbook.add_format({"align": "left", "border": 1})
        table_line_center = workbook.add_format({"align": "center", "border": 1})

        worksheet.merge_range(0, 2, 0, 3, "Sale Report By Category", head)
        worksheet.write(1, 2, "From : %s" % (wizard.start_date).date(), head)
        worksheet.write(1, 3, "To : %s" % (wizard.end_date).date(), head)

        rows = []
        rows_with_products = []
        total_qty = 0
        total_qty2 = 0

        # header
        for obj in wizard:
            if not obj.category_ids:
                obj.category_ids = self.env["product.category"].search([])

            for category in obj.category_ids:
                total_qty_delivered = 0
                # Get the product IDs belonging to the selected category
                product_ids = self.env["product.product"].search([("categ_id", "=", category.id)])
                stock_moves = self.env["stock.move"].search(
                    [
                        ("product_id", "in", product_ids.ids),
                        ("state", "=", "done"),
                        ("date", ">=", obj.start_date),
                        ("date", "<=", obj.end_date),
                        ("picking_id", "!=", False),
                        ("picking_id.sale_id", "!=", False),
                    ]
                )
                total_qty_delivered = sum(stock_moves.mapped("quantity"))
                rows.append({"category": category, "qty_delivered": total_qty_delivered})
                total_qty += total_qty_delivered

            if obj.select_products:
                for category in obj.category_ids:
                    qty_delivered = 0
                    total = 0
                    products = []
                    # Get the stock move IDs belonging to the selected products
                    product_ids = obj.product_ids if obj.product_ids else self.env["product.product"].search([("categ_id", "=", category.id)])
                    for product in product_ids:
                        if product.categ_id.id == category.id:
                            stock_move = self.env["stock.move"].search(
                                [
                                    ("product_id", "=", product.id),
                                    ("state", "=", "done"),
                                    ("date", ">=", obj.start_date),
                                    ("date", "<=", obj.end_date),
                                    ("picking_id", "!=", False),
                                    ("picking_id.sale_id", "!=", False),
                                ]
                            )
                            qty_delivered = sum(stock_move.mapped("quantity"))
                            total += qty_delivered
                            total_qty2 += qty_delivered
                            products.append({"product": product.name, "qty_delivered": qty_delivered})
                    products = sorted(products, key=itemgetter("qty_delivered"), reverse=True)
                    rows_with_products.append({"category": category, "qty_delivered": total, "products": products})

            # Sort the rows based on qty_delivered in descending order
        rows = sorted(rows, key=itemgetter("qty_delivered"), reverse=True)
        rows_with_products = sorted(rows_with_products, key=itemgetter("qty_delivered"), reverse=True)

        count = 5
        if wizard.select_products:
            worksheet.write(4, 0, "Category Name", head)
            worksheet.write(4, 1, "Product", head)
            worksheet.write(4, 2, "Total Qty Delivered", head)
            for row in rows_with_products:
                category = row["category"]
                qty_delivered = row["qty_delivered"]

                full_category_name = self._get_full_category_name(category)
                worksheet.write(count, 0, full_category_name, table_head)
                worksheet.write(count, 1, "", table_head)
                worksheet.write(count, 2, qty_delivered, head)

                for product in row["products"]:
                    count += 1
                    worksheet.write(count, 1, product["product"], table_line)
                    worksheet.write(count, 2, product["qty_delivered"], table_line_center)

                count += 1
            worksheet.write(count, 0, "Total", head)
            worksheet.write(count, 1, "", head)
            worksheet.write(count, 2, total_qty2, head)
        else:
            worksheet.write(4, 0, "Category Name", head)
            worksheet.write(4, 1, "Total Qty Delivered", head)
            for row in rows:
                category = row["category"]
                qty_delivered = row["qty_delivered"]

                full_category_name = self._get_full_category_name(category)
                worksheet.write(count, 0, full_category_name, table_head)
                worksheet.write(count, 1, qty_delivered, table_line_center)

                count += 1
            worksheet.write(count, 0, "Total", head)
            worksheet.write(count, 1, total_qty, head)

    def _get_full_category_name(self, category):
        """
        Recursively retrieves the full name of a category, including its parent name and its own name.
        """
        if category.parent_id:
            return self._get_full_category_name(category.parent_id) + " / " + category.name
        return category.name
