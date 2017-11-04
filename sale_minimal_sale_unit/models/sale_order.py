
# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from odoo import models, exceptions, fields, api


class SaleOrderLine(models.Model):
        _inherit = "sale.order.line"

        minimal_sale_unit = fields.Float(
                string="UMV", related="product_id.minimal_sale_unit", readonly=True)
        minimal_sale_special_unit = fields.Float(
                string="UVE", related="product_id.minimal_sale_special_unit",
                readonly=True)
        @api.multi
        @api.onchange('product_uom_qty','product_id')

        def product_uom_change_qty(self):

                if self.order_id.pricelist_id and self.order_id.partner_id:
                        product = self.product_id.with_context(
                        lang=self.order_id.partner_id.lang,
                        partner=self.order_id.partner_id.id,
                        quantity=self.product_uom_qty,
                        date_order=self.order_id.date_order,
                        pricelist=self.order_id.pricelist_id.id,
                        uom=self.product_uom.id,
                        fiscal_position=self.env.context.get('fiscal_position')
                        )

                        qty = self.product_uom_qty
                        if product.minimal_sale_special_unit:
                                if qty < product.minimal_sale_special_unit:
                                        vals = {'product_uom_qty': (product.minimal_sale_special_unit)}
                                if qty < product.minimal_sale_unit:
                                # Apply increment and return
                                        vals = {'price_unit': self.price_unit * 1.10}
                                        self.update(vals)
                        if product.minimal_sale_unit:
                                multiple = int((qty - 0.0001) / product.minimal_sale_unit) + 1
                                vals = {'product_uom_qty': (multiple * product.minimal_sale_unit)}
                                self.update(vals)
