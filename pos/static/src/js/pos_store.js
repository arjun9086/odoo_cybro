/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { Orderline } from "@point_of_sale/app/generic_components/orderline/orderline";
import {PosOrderline} from "@point_of_sale/app/models/pos_order_line";
import { _t } from "@web/core/l10n/translation";

//patch(PosStore.prototype, {
//    async _processData(loadedData) {
//        await super._processData(...arguments);
//          const posConfig = loadedData.pos_config || {};
//        this.discount_limit_enabled = loadedData.pos_config.use_discount_limit;
//        console.log(discount_limit_enabled)
//        this.discount_limit_value = loadedData.pos_config.discount_limit;
//        this.discount_limit_categories = loadedData.pos_config.category_ids;  // list of ids
//    },
//});

patch(Orderline, {
    props: {
        ...Orderline.props,
        line: {
            ...Orderline.props.line,
            shape: {
                ...Orderline.props.line.shape,
                rating: { type: [String,Boolean], optional: true },
            },
        },
    },
});

patch(PosOrderline.prototype, {
    setup(vals) {
        return super.setup(...arguments);
    },
    getDisplayData() {
        return {
            ...super.getDisplayData(),
            rating: this.get_product().rating || "",
        };
    },
     set_discount(discount) {
        const parsedDiscount = typeof discount === "number" ? discount : parseFloat(discount || "0");

        const product = this.get_product();
        const category = product.pos_categ_id?.[0] ? this.pos.db.category_by_id[product.pos_categ_id[0]] : null;
        const maxAllowed = category?.discount ?? 100;

        if (parsedDiscount > maxAllowed) {
            this.pos.env.services.notification.add(
                _t(`Max discount allowed for category '${category?.name}' is ${maxAllowed}%`),
                { type: 'danger' }
            );
            return;
        }

        // Safe to apply discount
        this.discount = Math.min(Math.max(parsedDiscount, 0), 100);
        this.order_id.recomputeOrderData();
        this.setDirty();
    },

//    set_discount(discount) {
//        const product = this.get_product();
//        const pos = this.pos;
//        if (pos.discount_limit_enabled) {
//            const productCategoryId = product.pos_categ_id?.[0] || null;
//            if (productCategoryId && pos.discount_limit_categories.includes(productCategoryId)) {
//                if (discount > pos.discount_limit_value) {
//                    this.pos.env.services.notification.add(
//                        _t(`Maximum allowed discount for this category is ${pos.discount_limit_value}%`),
//                        { type: 'danger' }
//                    );
//                    return;
//                }
//            }
//        }
//        super.set_discount(...arguments);
//    },
});


