# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

import logging
from openerp import SUPERUSER_ID
from openerp.addons.website_sale.controllers.main import website_sale
from openerp import http
from openerp.http import request

logger = logging.getLogger(__name__)


class website_sale_sale_minimal(website_sale):

    def _compute_minimum_amount(self, product_id, add_qty, set_qty):
        cr, context = request.cr, request.context

        product = request.registry['product.product'].browse(
            cr, SUPERUSER_ID, int(product_id), context=context)

        minimal = int(product.minimal_sale_special_unit) or \
            int(product.minimal_sale_unit)

        if minimal == 0:
            return add_qty, set_qty

        quantity = set_qty if set_qty else add_qty
        if quantity is None:
            return add_qty, set_qty

        quantity = int(quantity)

        if quantity == 0:
            return add_qty, set_qty

        if quantity > 0 and (quantity % minimal != 0):
            quantity = quantity - (quantity % minimal)

        return 0, quantity

    @http.route()
    def cart_update(self, product_id, add_qty=1, set_qty=0, **kw):
        add_qty, set_qty = self._compute_minimum_amount(
            product_id, add_qty, set_qty)

        return super(website_sale_sale_minimal, self) \
            .cart_update(product_id, add_qty, set_qty, **kw)

    @http.route()
    def cart_update_json(self, product_id, line_id, add_qty=None, set_qty=None,
                         display=True):
        add_qty, set_qty = self._compute_minimum_amount(
            product_id, add_qty, set_qty)
        return super(website_sale_sale_minimal, self) \
            .cart_update_json(product_id, line_id, add_qty, set_qty, display)
