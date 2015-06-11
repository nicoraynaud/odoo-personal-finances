# -*- encoding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _
from datetime import datetime

class wizard_import_accounting_lines(osv.osv_memory):
    _name = 'wizard.import.accounting.lines'

    _columns = {
        'import' : fields.binary('File', required=True),
        'wiz_msg': fields.text('Message'),
        'state': fields.selection((('choose','choose'),('error','error'),('success','success')),'State')
    }

    _defaults = {
        'state' : 'choose'
    }
    
    def view_accounting_lines(self, cr, uid, ids, context):
        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')
        xml_id = 'action_invoice_tree1'
        result = mod_obj._get_id(cr, uid, 'account', xml_id)
        id = mod_obj.read(cr, uid, result, ['res_id'])['res_id']
        result = act_obj.read(cr, uid, id)
        result['domain'] = "[('id','in', ["+','.join(map(str,context['generated_accounting_line_ids']))+"])]"
        return result

    def import_data(self, cr, uid, ids, context):
        
        wiz = self.read(cr, uid, ids[0], ['import'])
        import_data = wiz['import'].decode('base64').strip('\n\r ')
        
        all_errors = []
        lines = import_data.strip('\n\r').split('\n')
        nbLine = 0
        data_to_import = []
        for line in lines:
            #get and store delivery form data
            line_datas = line.split(';')
            nbLine += 1

            print '---'
            print line
            
            data = {
                'date': line_datas[0],
                'description': line_datas[1],
                'state': 'ticked' if line_datas[3] else 'new',
                'debit': line_datas[4],
                'credit': line_datas[5]
            }
            data_to_import.append(data)
            print data
        
        if all_errors:
            error_msg = '\n'.join(all_errors)
            self.write(cr, uid, ids, {'wiz_msg': error_msg, 'state': 'error'})
        else:
            accounting_line_ids = []
            accounting_line_obj = self.pool.get('tekinico.accounting.line')
            # category_obj = self.pool.get('tekinico.accounting.category')
        
            #create delivery form and associated delivery form lines
            for vals in data_to_import:
                accounting_line_id = accounting_line_obj.create(cr, uid, vals, context)
                accounting_line_ids.append(accounting_line_id)
            
            context['generated_accounting_line_ids'] = accounting_line_ids
            success_msg = _("%s accounting lines have been created") % (len(accounting_line_ids))
            self.write(cr, uid, ids, {'wiz_msg': success_msg, 'state': 'success'})
            
        return {
            'name': _('Import Accounting Lines'),
            'type': 'ir.actions.act_window',
            'res_model': 'wizard.import.accounting.lines',
            'res_id': ids[0],
            'view_mode': 'form',
            'view_type': 'form',
            'views': [(False, 'form')],
            'target': 'new',
            'context' : context,
        }

wizard_import_accounting_lines()

