import re

with open('custom_addons/pos_kitchen_screen_odoo/models/pos_orders.py', 'r') as f:
    content = f.read()

methods_code = """
    @api.model
    def recall_latest_ready_order(self, shop_id):
        latest_waiting_order = self.search([
            ('order_status', '=', 'waiting'), 
            ('config_id', '=', shop_id)
        ], order='write_date desc', limit=1)
        
        if latest_waiting_order:
            latest_waiting_order.order_status = 'draft'
            for line in latest_waiting_order.lines:
                if line.order_status == 'waiting':
                    line.order_status = 'draft'
            message = {
                'res_model': self._name,
                'message': 'pos_order_recalled',
                'order_id': latest_waiting_order.id,
                'config_id': latest_waiting_order.config_id.id
            }
            channel = f'pos_order_created_{latest_waiting_order.config_id.id}'
            self.env["bus.bus"]._sendone(channel, "notification", message)
            return True
        return False

    @api.model
    def clear_completed_orders(self, shop_id):
        completed_orders = self.search([
            ('order_status', '=', 'ready'),
            ('config_id', '=', shop_id),
            ('is_cooking', '=', True)
        ])
        if completed_orders:
            completed_orders.write({'is_cooking': False})
            
            message = {
                'res_model': self._name,
                'message': 'pos_order_cleared',
                'config_id': shop_id
            }
            channel = f'pos_order_created_{shop_id}'
            self.env["bus.bus"]._sendone(channel, "notification", message)
            return True
        return False

"""

# Insert these methods into pos.order class
match = re.search(r'    @api\.model\n    def check_order\(self, order_name\):', content)
if match:
    content = content[:match.start()] + methods_code + content[match.start():]

with open('custom_addons/pos_kitchen_screen_odoo/models/pos_orders.py', 'w') as f:
    f.write(content)

print("pos_orders.py updated successfully.")
