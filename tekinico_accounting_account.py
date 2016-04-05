# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
import logging
import time

_logger = logging.getLogger(__name__)

class tekinico_accounting_account(osv.osv):
    _name = 'tekinico.accounting.account'
    _description = 'Account'
    _order = "label asc"
    _rec_name = "label"

    def _get_balance_id(self, cr, uid, ids, name, args, context):
        res = {}

        line_obj = self.pool.get('tekinico.accounting.line')
        for bid in ids:
            lines = line_obj.search(cr, uid, [('account_id', '=', bid), '|', ('date_effect', '<=', time.strftime("%Y-%m-%d")), ('date_effect', '=', None)], order='date')
            res[bid] = 0
            for line in line_obj.browse(cr, uid , lines, context=context):
                res[bid] = res[bid] + (line.credit - line.debit)

        return res

    def _get_balance_ticked_id(self, cr, uid, ids, name, args, context):
        res = {}

        line_obj = self.pool.get('tekinico.accounting.line')
        for bid in ids:
            lines = line_obj.search(cr, uid, [('account_id', '=', bid), ('state', '=', 'ticked')], order='date')
            res[bid] = 0
            for line in line_obj.browse(cr, uid , lines, context=context):
                res[bid] = res[bid] + (line.credit - line.debit)

        return res


    def _get_balance_future_id(self, cr, uid, ids, name, args, context):
        res = {}

        line_obj = self.pool.get('tekinico.accounting.line')
        for bid in ids:
            lines = line_obj.search(cr, uid, [('account_id', '=', bid)], order='date')
            res[bid] = 0
            for line in line_obj.browse(cr, uid , lines, context=context):
                res[bid] = res[bid] + (line.credit - line.debit)

        return res

    _columns = {
        'bank': fields.char('Bank', required=True),
        'label': fields.char('Label', required=True),
        'type': fields.selection([('checking','Checking'),('savings','Savings')], 'Type'),
        'account_number': fields.char('Account Number'),
        'balance' : fields.function(_get_balance_id, type='integer', string='Balance'),
        'balance_future' : fields.function(_get_balance_future_id, type='integer', string='Balance future'),
        'balance_ticked' : fields.function(_get_balance_ticked_id, type='integer', string='Balance ticked')
    }

tekinico_accounting_account()
