import re

with open('custom_addons/pos_kitchen_screen_odoo/static/src/xml/kitchen_screen_templates.xml', 'r') as f:
    xml_content = f.read()

new_kitchen_order = """    <t t-name="KitchenOrder">
        <div class="row">
            <t t-foreach="this.filteredOrders" t-as="order" t-key="order.id">
                <div class="col-lg-3 col-md-4 col-sm-6 col-12 mb-3">
                    <div class="card h-100" style="border: none; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                        
                        <!-- Clickable Header that advances state -->
                        <div class="card-header bg-white" 
                             style="cursor: pointer; padding: 12px 15px; border-bottom: 1px solid #f0f0f0; border-radius: 8px 8px 0 0;"
                             t-att-data-order-id="order.id"
                             t-on-click="(e) => order.order_status == 'draft' ? this.accept_order(e) : (order.order_status == 'waiting' ? this.done_order(e) : null)">
                             
                            <!-- Top row: Order Number and User -->
                            <div class="d-flex align-items-center mb-2" style="font-weight: 600; font-size: 16px; color: #000;">
                                <span class="me-2"><t t-if="order.table_id"><t t-esc="order.table_id[1]"/> </t><t t-esc="order.name"/></span>
                                <span class="ms-auto" style="font-size: 14px;"><i class="fa fa-user-circle me-1"/> <t t-esc="order.user_id[1]"/></span>
                            </div>
                            
                            <!-- Bottom row: Status Pill and Timer -->
                            <div class="d-flex align-items-center justify-content-between">
                                <t t-if="order.order_status == 'draft'">
                                    <span class="badge rounded-pill text-white" style="background-color: #6c757d; font-size: 13px; font-weight: 500; padding: 5px 12px;">To prepare</span>
                                </t>
                                <t t-if="order.order_status == 'waiting'">
                                    <span class="badge rounded-pill text-white" style="background-color: #0d6efd; font-size: 13px; font-weight: 500; padding: 5px 12px;">Ready</span>
                                </t>
                                <t t-if="order.order_status == 'ready'">
                                    <span class="badge rounded-pill text-white" style="background-color: #198754; font-size: 13px; font-weight: 500; padding: 5px 12px;">Completed</span>
                                </t>
                                
                                <span class="badge rounded-pill bg-white border text-dark d-flex align-items-center" style="font-size: 13px; font-weight: 500; padding: 5px 10px;">
                                    <i class="fa fa-clock-o me-1"/>
                                    <t t-if="state.countdowns[order.id]">
                                        <t t-if="state.countdowns[order.id].isCompleted">00:00</t>
                                        <t t-else="">
                                            <t t-if="state.countdowns[order.id].minutes > 0">
                                                <t t-esc="state.countdowns[order.id].minutes"/>'
                                            </t>
                                            <t t-else="">
                                                <t t-esc="state.countdowns[order.id].seconds"/>"
                                            </t>
                                        </t>
                                    </t>
                                    <t t-else="">0'</t>
                                </span>
                            </div>
                        </div>

                        <!-- Card Body (Order Lines) -->
                        <div class="card-body p-0">
                            <ul class="list-group list-group-flush border-0">
                                <t t-foreach="order.lines" t-as="lines" t-key="lines">
                                    <t t-foreach="state.lines" t-as="line" t-key="line.id">
                                        <t t-if="lines==line.id">
                                            <t t-set="is_completed" t-value="line.order_status == 'ready'"/>
                                            <button class="list-group-item text-start border-bottom-0 py-3 accept_order_line w-100"
                                                    t-on-click="(e) => this.accept_order_line(e)"
                                                    t-att-value="line.id"
                                                    style="background: transparent; border: none; outline: none; border-bottom: 1px solid #f8f9fa !important;"
                                                    t-attf-style="{{ is_completed ? 'text-decoration: line-through; color: #ced4da;' : 'color: #333;' }}">
                                                <div class="d-flex align-items-start" style="pointer-events: none;">
                                                    <span class="me-2" t-attf-style="{{ is_completed ? 'color: #ced4da;' : 'color: #6c757d;' }}"><t t-esc="line.qty"/>x</span> 
                                                    <div class="flex-grow-1">
                                                        <span class="fw-medium"><t t-esc="line.full_product_name"/></span>
                                                        <t t-if="line.note">
                                                            <br/><span t-attf-style="{{ is_completed ? 'color: #ced4da;' : 'color: #6c757d;' }}" style="font-size: 13px;">- <t t-esc="line.note"/></span>
                                                        </t>
                                                    </div>
                                                </div>
                                            </button>
                                        </t>
                                    </t>
                                </t>
                            </ul>
                        </div>
                    </div>
                </div>
            </t>
        </div>
    </t>
</template>"""

pattern2 = r'<t t-name="KitchenOrder">.*</template>'
xml_content = re.sub(pattern2, new_kitchen_order, xml_content, flags=re.DOTALL)

with open('custom_addons/pos_kitchen_screen_odoo/static/src/xml/kitchen_screen_templates.xml', 'w') as f:
    f.write(xml_content)

print("XML template rewritten successfully for card layout.")
