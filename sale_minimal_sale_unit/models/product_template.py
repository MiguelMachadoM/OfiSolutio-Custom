# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from odoo import models, fields
import odoo.addons.decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = "product.template"

    minimal_sale_unit = fields.Float(
        digits=dp.get_precision('Product Unit of Measure'),
        string="UMV")
    minimal_sale_special_unit = fields.Float(
        digits=dp.get_precision('Product Unit of Measure'),
        string="UVE")

