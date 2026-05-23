import re

with open('custom_addons/pos_kitchen_screen_odoo/static/src/xml/kitchen_screen_templates.xml', 'r') as f:
    xml_content = f.read()

# Make tabs smaller by adding inline styles to .top_bar a
xml_content = xml_content.replace('<div class="top_bar">', '<div class="top_bar" style="padding: 5px 0;">')
xml_content = xml_content.replace('<a href="#">', '<a href="#" style="padding: 5px 15px; font-size: 14px; display: flex; align-items: center; gap: 5px;">')
xml_content = xml_content.replace('width="10"', 'width="12"').replace('width="15"', 'width="12"').replace('width="12"', 'width="12"') # rough resize if any
xml_content = xml_content.replace('<div class="icon">', '<div class="icon" style="width: 14px; height: 14px; margin-right: 5px; display: flex; align-items: center; justify-content: center;">')

# Replace KitchenOrder entirely
new_kitchen_order = """    <t t-name="KitchenOrder">
        <section class="screen_info custom_padding_top">
            <div class="wrapper">
                <div class="container-fluid">
                    <div class="row">
                        <t t-foreach="state.order_details" t-as="order" t-key="order.id">
                            <t t-if="state.shop_id==order.config_id[0] and state.stages==order.order_status">
                                <t t-set="bg_class" t-value="order.order_status == 'draft' ? 'bg_grey' : (order.order_status == 'waiting' ? 'bg_blue' : 'bg_green')" />
                                <div class="col-lg-3 col-md-4 col-sm-6 col-12 mb-3">
                                    <div class="card h-100 shadow-sm border-0">
                                        <div t-attf-class="card-header text-white #{bg_class} d-flex justify-content-between align-items-center" style="padding: 10px 15px; border-radius: 8px 8px 0 0;">
                                            <div>
                                                <h6 class="mb-1 fw-bold text-uppercase">
                                                    <t t-if="order.order_status == 'draft'">Cooking</t>
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
                        </t>
                    </div>
                </div>
            </div>
        </section>
    </t>
</template>"""

# Replace everything from <t t-name="KitchenOrder"> to the end of the file
pattern = r'<t t-name="KitchenOrder">.*</template>'
xml_content = re.sub(pattern, new_kitchen_order, xml_content, flags=re.DOTALL)

with open('custom_addons/pos_kitchen_screen_odoo/static/src/xml/kitchen_screen_templates.xml', 'w') as f:
    f.write(xml_content)

print("XML template rewritten successfully.")
