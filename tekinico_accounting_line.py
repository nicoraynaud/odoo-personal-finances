# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
import logging
import re

_logger = logging.getLogger(__name__)

class tekinico_accounting_line(osv.osv):
    _name = 'tekinico.accounting.line'
    _description = 'Accounting Line'
    _order = "date desc, date_created desc"

    def _get_balance_id(self, cr, uid, ids, name, args, context):
        res = {}
        for line in self.browse(cr, uid ,ids, context=context):
            res[line.id] = line.credit - line.debit
        return res

    _columns = {
        'date': fields.date('Date', required=True),
        'description': fields.char('Description', required=True),
        'debit': fields.float('Debit', digits=(16,0)),
        'credit': fields.float('Credit', digits=(16,0)),
        'date_created': fields.datetime('Date Created', readonly=True, required=True),
        'source': fields.selection([('manual','Manual'),('generated','Generated')], 'Source', readonly=True),
        'state': fields.selection([('new','New'),('ticked','Ticked'),('cancelled','Cancelled')], 'State'),
        'date_effect' : fields.date('Date Effect'),
        'where': fields.char('Place', size=255),
        'category_id': fields.many2one('tekinico.accounting.category', string='Category'),
        'balance' : fields.function(_get_balance_id, type='integer', store=True, string='Balance')
    }
 
    _defaults = {
        'date_created': fields.datetime.now(),
        'state': 'new',
        'source': 'manual',
    }

    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}

        category_obj = self.pool.get('tekinico.accounting.category')
        category_ids = category_obj.search(cr, uid, [('active', '=', True)])
        categories = category_obj.browse(cr, uid, category_ids, context=context)

        cat_id = False
        for c in categories:
            if re.search(c.name, vals['description'], re.IGNORECASE):
                cat_id = c.id

        if cat_id:
            vals['category_ids'] = cat_id

        return super(tekinico_accounting_line, self).create(cr, uid, vals, context=context)

tekinico_accounting_line()