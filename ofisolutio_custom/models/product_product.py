# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if args is None:
            args = []
        if not name or len(name) < 3:
            return super(ProductProduct, self).name_search(
                name=name, args=args, operator=operator, limit=limit)
        supplierinfo_obj = self.env['product.supplierinfo']
        supps = supplierinfo_obj.search([('product_code', operator, name)])
        if supps:
            records = self.search(
                args +
                [('product_tmpl_id', 'in', [x.product_tmpl_id.id
                                            for x in supps])], limit=limit)
        else:
            records = self
        names = super(ProductProduct, self).name_search(
            name=name, args=args, operator=operator, limit=limit)
        ids2 = [x[0] for x in names]
        return self.search([('id', 'in', records.ids + ids2)],
                            limit=limit).name_get()
