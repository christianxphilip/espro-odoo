import re

with open('custom_addons/pos_kitchen_screen_odoo/static/src/xml/kitchen_screen_templates.xml', 'r') as f:
    xml_content = f.read()

new_header = """    <t t-name="KitchenCustomDashBoard">
        <div id="kitchen_screen" class="kitchen">
            <div class="body_wrapper">
                <!-- Top Navigation Bar (Native Odoo Style) -->
                <div class="top_bar">
                    <div class="left_section">
                        <!-- Left Icon (e.g., Sidebar toggle placeholder) -->
                        <button class="action-btn">
                            <i class="fa fa-columns"></i>
                        </button>
                    </div>
                    
                    <div class="center_filters">
                        <a class="filter-btn" t-att-class="{'active': state.stages === 'all'}" t-on-click="(e) => this.all_stage(e)">
                            All
                        </a>
                        <a class="filter-btn" t-att-class="{'active': state.stages === 'draft'}" t-on-click="(e) => this.draft_stage(e)">
                            To prepare <span class="badge-count badge-grey"><t t-esc="state.draft_count"/></span>
                        </a>
                        <a class="filter-btn" t-att-class="{'active': state.stages === 'waiting'}" t-on-click="(e) => this.waiting_stage(e)">
                            Ready <span class="badge-count badge-blue"><t t-esc="state.waiting_count"/></span>
                        </a>
                        <a class="filter-btn" t-att-class="{'active': state.stages === 'ready'}" t-on-click="(e) => this.ready_stage(e)">
                            Completed <span class="badge-count badge-green"><t t-esc="state.ready_count"/></span>
                        </a>
                    </div>
                    
                    <div class="right_section">
                        <button class="action-btn" t-on-click="(e) => this.forceRefresh(e)">
                            <i class="fa fa-undo"></i> Recall
                        </button>
                        <button class="action-btn" onclick="window.history.back()">
                            Close <i class="fa fa-sign-out"></i>
                        </button>
                    </div>
                </div>

                <!-- Orders Container -->
                <div class="orders_container container-fluid">
                    <t t-call="KitchenOrder"/>
                </div>
            </div>
        </div>
    </t>"""

# Replace KitchenCustomDashBoard entirely
pattern1 = r'<t t-name="KitchenCustomDashBoard">.*?</t>\s*<!--Template for Kitchen Orders'
xml_content = re.sub(pattern1, new_header + '\n    <!--Template for Kitchen Orders', xml_content, flags=re.DOTALL)

# In KitchenOrder, I also need to make sure the loop uses `state.stages == 'all' or state.stages == order.order_status`
# Wait, the JS already handles `filteredOrders`! 
# Let me change the `t-foreach="state.order_details"` to `t-foreach="this.filteredOrders"` in the XML for cleaner logic!
# Then we don't need the `t-if="state.shop_id==... and state.stages==..."` check inside!

new_kitchen_order = """    <t t-name="KitchenOrder">
        <div class="row">
            <t t-foreach="this.filteredOrders" t-as="order" t-key="order.id">
                <t t-set="bg_class" t-value="order.order_status == 'draft' ? 'bg_grey' : (order.order_status == 'waiting' ? 'bg_blue' : 'bg_green')" />
                <div class="col-lg-3 col-md-4 col-sm-6 col-12 mb-3">
                    <div class="card h-100">
                        <div t-attf-class="card-header text-white #{bg_class} d-flex justify-content-between align-items-center" style="padding: 10px 15px; border-radius: 8px 8px 0 0;">
                            <div>
                                <h6 class="mb-1 fw-bold text-uppercase">
                                    <t t-if="order.order_status == 'draft'">To prepare</t>
                                    <t t-if="order.order_status == 'waiting'">Ready</t>
                                    <t t-if="order.order_status == 'ready'">Completed</t>
                                </h6>
                                <span class="d-block" style="font-size: 13px;">Order: <t t-esc="order.name"/></span>
                                <span class="d-block" style="font-size: 12px; opacity: 0.9;">Time: <t t-esc="order.hour"/>:<t t-esc="order.formatted_minutes"/></span>
                            </div>
                            <div class="text-end" style="font-size: 12px;">
                                <span class="d-block">User: <t t-esc="order.user_id[1]"/></span>
                                <t t-if="order.table_id"><span class="d-block">Table: <t t-esc="order.table_id[1]"/></span></t>
                                <t t-if="order.floor"><span class="d-block">Floor: <t t-esc="order.floor"/></span></t>
                            </div>
                        </div>
                        <div class="card-body p-0">
                            <ul class="list-group list-group-flush border-0">
                                <t t-foreach="order.lines" t-as="lines" t-key="lines">
                                    <t t-foreach="state.lines" t-as="line" t-key="line.id">
                                        <t t-if="lines==line.id">
                                            <t t-set="is_completed" t-value="line.order_status == 'ready'"/>
                                            <button class="list-group-item text-start border-bottom-0 py-2 accept_order_line w-100"
                                                    t-on-click="(e) => this.accept_order_line(e)"
                                                    t-att-value="line.id"
                                                    t-attf-style="{{ is_completed ? 'text-decoration: line-through; color: #999; background: #f8f9fa;' : '' }}">
                                                <div class="d-flex justify-content-between align-items-center" style="pointer-events: none;">
                                                    <div>
                                                        <span class="fw-bold"><t t-esc="line.qty"/>x</span> 
                                                        <span class="ms-1"><t t-esc="line.full_product_name"/></span>
                                                        <t t-if="line.note">
                                                            <br/><small class="text-muted"><i class="fa fa-tag me-1"/> <t t-esc="line.note"/></small>
                                                        </t>
                                                    </div>
                                                    <div t-if="is_completed and line.completion_duration" class="badge bg-secondary text-white rounded-pill" style="font-size:11px;">
                                                        <t t-esc="line.completion_duration"/>
                                                    </div>
                                                </div>
                                            </button>
                                        </t>
                                    </t>
                                </t>
                            </ul>
                        </div>
                        <div class="card-footer bg-white text-center border-top-0 pt-0 pb-3" style="border-radius: 0 0 8px 8px;">
                            <h4 class="mb-3 fw-bold" style="letter-spacing: 1px;">
                                <t t-if="state.countdowns[order.id]">
                                    <t t-if="state.countdowns[order.id].isCompleted">
                                        <span class="text-success">00:00</span>
                                    </t>
                                    <t t-else="">
                                        <t t-esc="state.countdowns[order.id].minutes.toString().padStart(2, '0')"/>:<t t-esc="state.countdowns[order.id].seconds.toString().padStart(2, '0')"/>
                                    </t>
                                </t>
                                <t t-else="">
                                    00:00
                                </t>
                            </h4>
                            <div class="d-flex justify-content-center gap-2">
                                <t t-if="order.order_status == 'draft'">
                                    <button class="btn btn-sm btn-primary flex-grow-1" t-att-value="order.id" t-on-click="(e) => this.accept_order(e)">Start Cooking</button>
                                </t>
                                <t t-elif="order.order_status == 'waiting'">
                                    <button class="btn btn-sm btn-success flex-grow-1" t-att-value="order.id" t-on-click="(e) => this.done_order(e)">Mark Ready</button>
                                </t>
                            </div>
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

print("XML template rewritten successfully.")
