/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { Orderline } from "@point_of_sale/app/generic_components/orderline/orderline";
import {PosOrderline} from "@point_of_sale/app/models/pos_order_line";
import { _t } from "@web/core/l10n/translation";
import { parseFloat } from "@web/views/fields/parsers";
//import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";

patch(PosStore.prototype, {
    async setup() {
        await super.setup(...arguments);
        const sessionDiscountLimit = this.pos.session.discount_limit || 0;

        console.log("Session discount limit from backend:", sessionDiscountLimit);

        this.discount_limit = sessionDiscountLimit;
        this.is_discount_limit_enabled = sessionDiscountLimit > 0;
        this.remaining_discount_limit = sessionDiscountLimit;
    },

    deductFromDiscountLimit(percentUsed) {
        this.remaining_discount_limit -= percentUsed;
    },
});

patch(Orderline, {
    props: {
        ...Orderline.props,
        line: {
            ...Orderline.props.line,
            shape: {
                ...Orderline.props.line.shape,
                rating: { type: [String,Boolean], optional: true },
                discount:{ type: [String,Boolean] ,optional: true},
//                is_discount_limit_enabled:{type:[Boolean],optional:true}
            },
        },
    },
});
patch(PosOrderline.prototype, {
    setup() {
//        limit_discount=this.models['pos.session'].getAll().map((limit)=>({
//        discount_limit:limit.discount_limit}));
//        console.log(limit_discount)
        return super.setup(...arguments);
    },
    getDisplayData() {
        return {
            ...super.getDisplayData(),
            rating: this.get_product().rating || "",
        };
    },
    async set_discount(discount) {
    // Safely parse the discount input
    var parsed_discount =
        typeof discount === "number" ? discount :
        isNaN(parseFloat(discount)) ? 0 :
        parseFloat("" + discount);
    var disc = Math.min(Math.max(parsed_discount || 0, 0), 100);
    //  Get the actual discount limit from POS session settings
//    const pos = this.order?.pos;
    var DiscountLimit = this.discount_limit || 0;
    console.log(this.discount_limit)
//    var isLimitEnabled = this.order?.pos?.posStore?.is_discount_limit_enabled;
    // Debugging
    console.log("Trying to apply:", disc);
    console.log("Session discount limit is:", DiscountLimit);
    if (disc > DiscountLimit) {
        alert('Reached Discount Limit! Cannot apply more than ' + DiscountLimit + '%');
        this.discount = 0;
        this.discountStr = "0";
    } else {
        this.discount = disc;
        this.discountStr = "" + disc;
    }
}

//        if (posStore.is_discount_limit_enabled) {
//            if (!posStore.hasRemainingDiscount(parsedDiscount)) {
//                alert(`You cannot give more than ${posStore.remaining_discount_limit}% discount remaining in this session.`);
//                this.discount = 0;
//                this.discountStr = "0";
//                return;
//            }
//
//            // Accept and deduct from remaining limit
//            posStore.deductFromDiscountLimit(parsedDiscount);
//        }
//
//        this.discount = parsedDiscount;
//        this.discountStr = discountStr;
//    },


});


