/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { Orderline } from "@point_of_sale/app/generic_components/orderline/orderline";
import {PosOrderline} from "@point_of_sale/app/models/pos_order_line";
import { _t } from "@web/core/l10n/translation";
import { parseFloat } from "@web/views/fields/parsers";
//import { ErrorPopup } from "@point_of_sale/app/errors";

patch(PosStore.prototype, {
    async _processData(loadedData) {
        await super._processData(...arguments);

       const isDiscountLimitEnabled = await this.rpc({
            model: "ir.config_parameter",
            method: "get_param",
            args: ["pos_discount_limit.is_discount_limit"],
        });

        const discountLimit = await this.rpc({
            model: "ir.config_parameter",
            method: "get_param",
            args: ["pos_discount_limit.discount"],
        });
        this.is_discount_limit_enabled = isDiscountLimitEnabled === "True";
        this.discount_limit = parseFloat(discountLimit || "0");

        console.log("Discount limit loaded:", this.discount_limit);
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
                is_discount_limit_enabled:{type:[Boolean],optional:true}

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
    async set_discount(discount) {
        var parsed_discount =
            typeof discount === "number" ?
            discount :
            isNaN(parseFloat(discount)) ?
            0 :
            parseFloat("" + discount);
        var disc = Math.min(Math.max(parsed_discount || 0, 0), 100);
        var DiscountLimit=this.discount;
        console.log(this.discount)
        if (disc<DiscountLimit) {
            console.log('Working');
//            await this.env.services.popup.add(alert, {
//                title: _t("Exceed Discount Limit!"),
//                body: _t("Sorry, Discount is not allowed. Maximum discount for this Product is %s %", DiscountLimit),

            this.discount = 0;
            this.discountStr = "0";
        } else {
            this.discount = disc;
            this.discountStr = "" + disc;
        }
    },

});


