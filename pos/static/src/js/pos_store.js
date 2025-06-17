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
        const parsed_discount =
            typeof discount === "number"
                ? discount
                : isNaN(parseFloat(discount))
                ? 0
                : parseFloat("" + discount);

        const disc = Math.min(Math.max(parsed_discount || 0, 0), 100);
        this.discount = disc;
        this.order_id.recomputeOrderData();
        this.setDirty();
//        const product = this.get_product();
//        const pos = this.pos;
//
//        const categoryId = product.pos_categ_id && product.pos_categ_id[0];  // category id of product
//        const isLimited = pos.discount_limit_enabled;
//        const isInCategory = pos.discount_limit_categories?.includes(categoryId);
//
//        if (isLimited && isInCategory && discount > pos.discount_limit_value) {
//            this.pos.env.services.notification.add(
//                _t(`Maximum allowed discount for this category is ${pos.discount_limit_value}%`),
//                { type: 'danger' }
//            );
//            return;
//        }

//        super.set_discount(...arguments);
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


