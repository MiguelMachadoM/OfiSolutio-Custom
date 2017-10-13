# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, api


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    @api.multi
    def product_id_change(
            self, product_id, uom_id, qty=0, name='', type='out_invoice',
            partner_id=False, fposition_id=False, price_unit=False,
            currency_id=False, company_id=None):
        result = super(AccountInvoiceLine, self).product_id_change(
            product_id, uom_id, qty=qty, name='', type=type,
            partner_id=partner_id, fposition_id=fposition_id,
            price_unit=price_unit, currency_id=currency_id,
            company_id=company_id)
        if product_id and type in ('out_invoice', 'out_refund'):
            partner = self.env['res.partner'].browse(partner_id)
            context_partner = {'lang': partner.lang, 'partner_id': partner_id}
            product = self.env['product.product'].with_context(
                context_partner).browse(product_id)
            result['value']['name'] = product.partner_ref
        return result
