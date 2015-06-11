# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp import api

class tekinico_accounting_category(osv.osv):
	
    def name_get(self, cr, uid, ids, context=None):
        """ Return the categories' display name, including their direct
            parent by default.

            If ``context['accounting_category_display']`` is ``'short'``, the short
            version of the category name (without the direct parent) is used.
            The default is the long version.
        """
        if not isinstance(ids, list):
            ids = [ids]
        if context is None:
            context = {}

        if context.get('accounting_category_display') == 'short':
            return super(tekinico_accounting_category, self).name_get(cr, uid, ids, context=context)

        res = []
        for category in self.browse(cr, uid, ids, context=context):
            names = []
            current = category
            while current:
                names.append(current.name)
                current = current.parent_id
            res.append((category.id, ' / '.join(reversed(names))))
        return res

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        if name:
            # Be sure name_search is symetric to name_get
            name = name.split(' / ')[-1]
            args = [('name', operator, name)] + args
        categories = self.search(args, limit=limit)
        return categories.name_get()

    @api.multi
    def _name_get_fnc(self, field_name, arg):
        return dict(self.name_get())

    _description = 'Accounting Line Category'
    _name = 'tekinico.accounting.category'
    _columns = {
        'name': fields.char('Category Name', required=True, translate=True),
        'parent_id': fields.many2one('tekinico.accounting.category', 'Parent Category', select=True, ondelete='cascade'),
        'complete_name': fields.function(_name_get_fnc, type="char", string='Full Name'),
        'child_ids': fields.one2many('tekinico.accounting.category', 'parent_id', 'Child Categories'),
        'active': fields.boolean('Active', help="The active field allows you to hide the category without removing it."),
        'parent_left': fields.integer('Left parent', select=True),
        'parent_right': fields.integer('Right parent', select=True),
        'accounting_line_ids': fields.many2many('tekinico.accounting.line', id1='category_id', id2='accounting_line_id', string='Accounting Lines'),
    }
    _constraints = [
        (osv.osv._check_recursion, 'Error ! You can not create recursive categories.', ['parent_id'])
    ]
    _defaults = {
        'active': 1,
    }
    _parent_store = True
    _parent_order = 'name'
    _order = 'parent_left'

tekinico_accounting_category()