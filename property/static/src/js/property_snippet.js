/** @odoo-module **/
import { renderToElement } from "@web/core/utils/render";
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.get_product_tab = publicWidget.Widget.extend({
    selector: '.categories_section',
    async willStart() {
        const result = await rpc('/property/json', {});
        if (result && Array.isArray(result)) {
            const chunk_size = 4;
            const chunks = [];
            for (let i = 0; i < result.length; i += chunk_size) {
                chunks.push({
                    items: result.slice(i, i + chunk_size),
                    is_active: i === 0,
                });
            }
            this.$target.empty().html(renderToElement('property.category_data', {
                chunks: chunks,
            }));
        }
    },
});

