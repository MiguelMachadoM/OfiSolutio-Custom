# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012-Today Serpent Consulting Services Pvt. Ltd.
#                            (<http://www.serpentcs.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

{
    'name': 'Websile Sale Show only PriceList',
    'author': 'OfiSolutio Logistic, S.L.',
    'category': 'e-Commerce',
    'website': 'http://www.ofisolutio.com',
    'version': '8.0.1.0.0',
    'sequence': 1,
    'description': """
Remove Default Pricelist from Shop
=========================
With this module when you have assign a price list to a customer will by hidden default price set in product sheet.
     """,
    'depends': ['website_sale'],
    'data': [
        'views/website_sale_opl.xml',
    ],
    'installable': True,
}
