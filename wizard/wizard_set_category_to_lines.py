# -*- encoding: utf-8 -*-
from openerp.osv import fields, osv

class wizard_set_category_to_lines(osv.osv_memory):
    _name = 'wizard.set.category.to.lines'

    _columns = {
        'category_id': fields.many2one('tekinico.accounting.category', string='Category')
    }
    
    def set_category(self, cr, uid, ids, context):

        if context == None:
            return

        wiz = self.read(cr, uid, ids[0], ['category_id'])
        accounting_line_obj = self.pool.get('tekinico.accounting.line')

        print wiz['category_id']
        accounting_line_obj.write(cr, uid, context['active_ids'], { 'category_id': wiz['category_id'][0] })
            
        return

wizard_set_category_to_lines()

