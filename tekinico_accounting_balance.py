# -*- coding: utf-8 -*-
from openerp import tools
from openerp.osv import fields,osv

class tekinico_accounting_balance(osv.osv):
    _name = "tekinico.accounting.balance"
    _description = "View accounting balance"
    _auto = False
    _order = "year asc, month asc"

    _columns = {
        'year':fields.integer('Year',readonly=True),
        'month':  fields.integer('Month',readonly=True),
        'balance': fields.integer('Balance',readonly=True)
    }
    
    def init(self, cr):
        tools.drop_view_if_exists(cr, 'tekinico_accounting_balance')
        cr.execute("""
            create or replace view tekinico_accounting_balance as (
                select row_number() OVER(ORDER BY year, month) as id, * from (
                    select 
                        extract(year from date) as year,
                        extract(month from date) as month,
                        sum(sum(credit - debit)) 
                            over (order by extract(year from date),extract(month from date))
                            as balance
                        from 
                            tekinico_accounting_line
                        group by 
                            year,month
                    ) view
            )
        """)