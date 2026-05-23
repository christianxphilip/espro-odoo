import re

with open('custom_addons/pos_kitchen_screen_odoo/models/pos_orders.py', 'r') as f:
    content = f.read()

# 1. Add completion_duration to pos.order
if "completion_duration =" not in content[:1500]: # check near top where pos.order fields are
    field_def = """    is_cooking = fields.Boolean(string="Cooking", default=False,
                                help='To identify the order is kitchen orders')
    completion_duration = fields.Char(string="Completion Duration", help="Total time taken to complete the order")"""
    content = content.replace("    is_cooking = fields.Boolean(string=\"Cooking\", default=False,\n                                help='To identify the order is kitchen orders')", field_def)

# 2. Update order_progress_change in pos.order to calculate completion_duration
order_change_func = """    def order_progress_change(self):
        \"\"\"Action for "Done" button: Move order from 'waiting' (ready) to 'ready' (completed) status.\"\"\"
        self.ensure_one()
        self.order_status = "ready"
        if self.date_order:
            from datetime import datetime
            delta = datetime.now() - self.date_order
            total_seconds = int(delta.total_seconds())
            minutes = total_seconds // 60
            seconds = total_seconds % 60
            self.completion_duration = f"{minutes:02d}:{seconds:02d}"
        
        kitchen_screen = self.env["kitchen.screen"].search(
            [("pos_config_id", "=", self.config_id.id)], limit=1)
        if kitchen_screen:
            for line in self.lines:
                if line.product_id.pos_categ_ids and any(
                        cat.id in kitchen_screen.pos_categ_ids.ids for cat in line.product_id.pos_categ_ids):
                    line.order_status = "ready"
                    if not line.completion_duration and self.date_order:
                        line.completion_duration = f"{minutes:02d}m {seconds:02d}s"
        message = {"""
content = re.sub(r'    def order_progress_change\(self\):\n.*?(?=\n        message = \{)', order_change_func, content, flags=re.DOTALL)

# 3. Update order_progress_change in pos.order.line to check if all lines are ready
line_change_func = """    def order_progress_change(self):
        \"\"\"Toggle status of an order line between 'waiting' and 'ready'.\"\"\"
        self.ensure_one()
        old_status = self.order_status
        if self.order_status == 'ready':
            self.order_status = 'waiting'
            self.completion_duration = False
        else:
            self.order_status = 'ready'
            if self.order_id.date_order:
                from datetime import datetime
                delta = datetime.now() - self.order_id.date_order
                total_seconds = int(delta.total_seconds())
                minutes = total_seconds // 60
                seconds = total_seconds % 60
                self.completion_duration = f"{minutes:02d}m {seconds:02d}s"

        if old_status != self.order_status:
            # Check if all kitchen lines for this order are now ready
            all_lines_ready = True
            for line in self.order_id.lines:
                if line.is_cooking and line.order_status != 'ready' and line.order_status != 'cancel':
                    all_lines_ready = False
                    break
            
            if all_lines_ready and self.order_id.order_status != 'ready':
                # Auto-advance the order to completed
                self.order_id.order_progress_change()
            else:
                # Just notify about this line
                message = {
                    'res_model': self._name,
                    'message': 'pos_order_line_progress',
                    'order_id': self.order_id.id,
                    'config_id': self.order_id.config_id.id
                }
                channel = f'pos_order_created_{self.order_id.config_id.id}'
                self.env["bus.bus"]._sendone(channel, "notification", message)"""

content = re.sub(r'    def order_progress_change\(self\):\n\s+"""Toggle status of an order line.*?self\.env\["bus\.bus"\]\._sendone\(channel, "notification", message\)', line_change_func, content, flags=re.DOTALL)

with open('custom_addons/pos_kitchen_screen_odoo/models/pos_orders.py', 'w') as f:
    f.write(content)

print("pos_orders.py updated successfully.")
