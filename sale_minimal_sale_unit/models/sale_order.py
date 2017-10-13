# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, exceptions, fields, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    minimal_sale_unit = fields.Float(
        string="UMV", related="product_id.minimal_sale_unit", readonly=True)
    minimal_sale_special_unit = fields.Float(
        string="UVE", related="product_id.minimal_sale_special_unit",
        readonly=True)

    @api.multi
    def product_id_change(
            self, pricelist, product, qty=0, uom=False, qty_uos=0, uos=False,
            name='', partner_id=False, lang=False, update_tax=True,
            date_order=False, packaging=False, fiscal_position=False,
            flag=False):
        res = super(SaleOrderLine, self).product_id_change(
            pricelist, product, qty=qty, uom=uom, qty_uos=qty_uos, uos=uos,
            name=name, partner_id=partner_id, lang=lang, update_tax=update_tax,
            date_order=date_order, packaging=packaging,
            fiscal_position=fiscal_position, flag=flag)
        if product:
            qty = res['value'].get('product_uom_qty', qty)
            product = self.env['product.product'].browse(product)
            if product.minimal_sale_special_unit:
                if qty < product.minimal_sale_special_unit:
                    res['value']['product_uom_qty'] = (
                        product.minimal_sale_special_unit)
                if qty < product.minimal_sale_unit:
                    # Apply increment and return
                    res['value']['price_unit'] = res['value'].get(
                        'price_unit', 0.0) * 1.10
                    return res
            if product.minimal_sale_unit:
                multiple = int((qty - 0.0001) /
                               product.minimal_sale_unit) + 1
                res['value']['product_uom_qty'] = (multiple *
                                                   product.minimal_sale_unit)
        return res
