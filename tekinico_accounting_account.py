# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
import logging
import time
from calendar import monthrange
import datetime
from dateutil import relativedelta

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
            lines = line_obj.search(cr, uid, [('account_id', '=', bid), ('date', '<=', time.strftime("%Y-%m-%d"))], order='date')
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


    def _get_balance_month_id(self, cr, uid, ids, name, args, context):
        res = {}

        line_obj = self.pool.get('tekinico.accounting.line')
        date = datetime.datetime.now()
        lastdayofmonth = monthrange(date.year, date.month)[1]
        max_date = "%s-%s-%s" % (date.year, date.month, lastdayofmonth)
        for bid in ids:
            lines = line_obj.search(cr, uid, [('account_id', '=', bid), ('date', '<=', max_date)], order='date')
            res[bid] = 0
            for line in line_obj.browse(cr, uid , lines, context=context):
                res[bid] = res[bid] + (line.credit - line.debit)

        return res

    def _get_balance_next_month_id(self, cr, uid, ids, name, args, context):
        res = {}

        line_obj = self.pool.get('tekinico.accounting.line')

        date = datetime.date.today() + relativedelta.relativedelta(months=1)
        lastdayofmonth = monthrange(date.year, date.month)[1]
        max_date = "%s-%s-%s" % (date.year, date.month, lastdayofmonth)
        for bid in ids:
            lines = line_obj.search(cr, uid, [('account_id', '=', bid), ('date', '<=', max_date)], order='date')
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
        'balance_month' : fields.function(_get_balance_month_id, type='integer', string='Balance eom'),
        'balance_next_month' : fields.function(_get_balance_next_month_id, type='integer', string='Balance eom+1'),
        'balance_ticked' : fields.function(_get_balance_ticked_id, type='integer', string='Balance ticked')
    }

tekinico_accounting_account()
