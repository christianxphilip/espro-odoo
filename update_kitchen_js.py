import re

with open('custom_addons/pos_kitchen_screen_odoo/static/src/js/kitchen_screen.js', 'r') as f:
    content = f.read()

# 1. Update relevantMessages
messages = """            'pos_order_cancelled',
            'pos_order_completed',
            'pos_order_line_updated',
            'pos_order_line_progress',
            'pos_order_recalled',
            'pos_order_cleared'
        ];"""
content = re.sub(r'            \'pos_order_cancelled\',\n            \'pos_order_completed\',\n            \'pos_order_line_updated\'\n        \];', messages, content)

# 2. Add new methods
methods = """    async recall_order(e) {
        try {
            await this.orm.call("pos.order", "recall_latest_ready_order", [this.currentShopId]);
            setTimeout(() => this.loadOrders(), 500);
        } catch (error) {
            console.error("Error recalling order:", error);
        }
    }

    async clear_completed_orders(e) {
        try {
            await this.orm.call("pos.order", "clear_completed_orders", [this.currentShopId]);
            setTimeout(() => this.loadOrders(), 500);
        } catch (error) {
            console.error("Error clearing completed orders:", error);
        }
    }

    async accept_order(e) {"""

content = content.replace('    async accept_order(e) {', methods)

with open('custom_addons/pos_kitchen_screen_odoo/static/src/js/kitchen_screen.js', 'w') as f:
    f.write(content)

print("kitchen_screen.js updated successfully.")
