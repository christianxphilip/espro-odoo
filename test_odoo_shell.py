shop_id = 1
orders = env['pos.order'].search([('order_status', '=', 'ready'), ('config_id', '=', shop_id), ('is_cooking', '=', True)])
print("Completed orders:", orders)
for o in orders:
    print(o.name, o.order_status, o.is_cooking)
    o.write({'is_cooking': False})
    print("Written is_cooking=False")
