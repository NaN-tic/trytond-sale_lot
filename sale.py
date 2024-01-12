#The COPYRIGHT file at the top level of this repository contains the full
#copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.model import fields
from trytond.pyson import Eval

__all__ = ['SaleLine']


class SaleLine(metaclass=PoolMeta):
    __name__ = 'sale.line'

    product_type = fields.Function(fields.Char('Product Type'),
        'on_change_with_product_type')
    lot = fields.Many2One('stock.lot', 'Lot',
        domain=[
            ('product', '=', Eval('product')),
            ],
        states={
            'invisible': ((Eval('type') != 'line')
                | (Eval('product_type') == 'service')),
            'readonly': Eval('sale_state') != 'draft',
            })

    @fields.depends('product')
    def on_change_with_product_type(self, name=None):
        if not self.product:
            return
        return self.product.type

    def get_move(self, shipment_type):
        move = super(SaleLine, self).get_move(shipment_type)
        if move and self.lot:
            move.lot = self.lot
        return move
