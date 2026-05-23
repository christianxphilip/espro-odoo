/** @odoo-module **/

import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { patch } from "@web/core/utils/patch";

patch(ProductScreen.prototype, {
    setup() {
        super.setup(...arguments);
        // Default sort by name
        this.state.sortBy = 'name';
    },

    setSortBy(sortType) {
        this.state.sortBy = sortType;
    },

    get productsToDisplay() {
        let list = super.productsToDisplay;
        
        if (this.state.sortBy === 'favorites') {
            return list.sort((a, b) => {
                let pA = (a.is_favorite !== undefined ? a.is_favorite : (a.raw && a.raw.is_favorite)) ? 1 : 0;
                let pB = (b.is_favorite !== undefined ? b.is_favorite : (b.raw && b.raw.is_favorite)) ? 1 : 0;
                return pB - pA || a.display_name.localeCompare(b.display_name);
            });
        }
        
        if (this.state.sortBy === 'most_ordered') {
            return list.sort((a, b) => {
                let sA = (a.pos_sales_count !== undefined ? a.pos_sales_count : (a.raw && a.raw.pos_sales_count)) || 0;
                let sB = (b.pos_sales_count !== undefined ? b.pos_sales_count : (b.raw && b.raw.pos_sales_count)) || 0;
                return sB - sA || a.display_name.localeCompare(b.display_name);
            });
        }
        
        // name sorting is the default behavior from Odoo
        return list;
    }
});
