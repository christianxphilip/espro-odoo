/** @odoo-module **/

import { ProductCard } from "@point_of_sale/app/generic_components/product_card/product_card";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";

patch(ProductCard.prototype, {
    setup() {
        super.setup(...arguments);
        this.orm = useService("orm");
    },

    async toggleFavorite(product) {
        if (!product) return;
        
        // Handle differences between raw data and modeled data in POS OWL
        const tmplId = product.raw ? product.raw.product_tmpl_id : product.product_tmpl_id;
        const currentStatus = product.is_favorite !== undefined ? product.is_favorite : (product.raw ? product.raw.is_favorite : false);
        const newStatus = !currentStatus;
        
        // Update backend
        await this.orm.write("product.template", [tmplId], {
            is_favorite: newStatus,
        });
        
        // Update frontend state
        product.is_favorite = newStatus;
        if (product.raw) {
            product.raw.is_favorite = newStatus;
        }
        
        // Re-render component
        this.render(true);
    }
});
