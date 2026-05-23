from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re


class ProductProduct(models.Model):
    _inherit = 'product.product'

    prepair_time_minutes = fields.Float(
        string='Preparation Time (MM:SS)',
        digits=(12, 2),
        help="Enter time in MM:SS format (e.g., 20:12 for 20 minutes 12 seconds)"
    )

    pos_sales_count = fields.Integer(string="POS Sales Count (30 Days)", compute="_compute_pos_sales_count")

    def _compute_pos_sales_count(self):
        thirty_days_ago = fields.Datetime.now() - __import__('dateutil').relativedelta.relativedelta(days=30)
        domain = [
            ('product_id', 'in', self.ids),
            ('order_id.date_order', '>=', thirty_days_ago),
            ('order_id.state', 'in', ['paid', 'done', 'invoiced'])
        ]
        line_data = self.env['pos.order.line'].read_group(domain, ['product_id', 'qty'], ['product_id'])
        sales_map = {data['product_id'][0]: data['qty'] for data in line_data}
        for product in self:
            product.pos_sales_count = int(sales_map.get(product.id, 0))

    @api.model
    def _load_pos_data_fields(self, config_id):
        result = super()._load_pos_data_fields(config_id)
        result.extend(['is_favorite', 'pos_sales_count'])
        return result

    @api.onchange('prepair_time_minutes')
    def _onchange_prepair_time(self):
        if isinstance(self.prepair_time_minutes, str):
            try:
                # Validate format MM:SS
                if not re.match(r'^\d{1,3}:[0-5][0-9]$', self.prepair_time_minutes):
                    raise ValidationError("Please enter time in MM:SS format (e.g., 20:12)")

                minutes, seconds = map(int, self.prepair_time_minutes.split(':'))
                self.prepair_time_minutes = minutes + (seconds / 60.0)
            except (ValueError, AttributeError):
                raise ValidationError("Invalid time format. Please use MM:SS (e.g., 20:12)")