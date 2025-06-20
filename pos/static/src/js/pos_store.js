/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { Orderline } from "@point_of_sale/app/generic_components/orderline/orderline";
import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
import { _t } from "@web/core/l10n/translation";
import { parseFloat } from "@web/views/fields/parsers";
import { useListener } from "@web/core/utils/hooks";
import { ReachedLimitPopup } from "@pos/js/reached_limit_popup";
import { WarningDialog } from "@web/core/errors/error_dialogs";
import { useService } from "@web/core/utils/hooks";

let discount_limit=0
let remaining_discount_limit=0

patch(PosStore.prototype, {
     async setup() {
     await super.setup(...arguments);
     // Get the current POS session
     const currentSession = this.models['pos.session']?.getAll()?.[0] || {};
     discount_limit = currentSession.discount_limit || 0;
     remaining_discount_limit = discount_limit;
     console.log("Session discount limit from backend:",discount_limit)

     },
//     getTotalAppliedDiscount() {
//        let total = 0;
//        const order = this.get_order();
//        if (!order) return total;
//        for (const line of order.get_orderlines()) {
//            if (line.discount) {
//                total += parseFloat(line.discount);
//            }
//        }
//        return total;
//     },
//     hasRemainingDiscount(discount) {
//        const totalUsed = this.getTotalAppliedDiscount();
//        const projected = totalUsed + discountToApply;
//        console.log(`Total used: ${totalUsed}, Trying to apply: ${discountToApply}, Projected: ${projected},
//        Limit: ${discount_limit}`);
//        return projected <= discount_limit;
//       },
//     deductFromDiscountLimit(percentUsed) {
//        remaining_discount_limit = Math.max(0, remaining_discount_limit - percentUsed);
//        },
    });

patch(Orderline, {
        setup(){
        super.setup();
        this.dialogService = useService("dialog");
        },
         props: {
            ...Orderline.props,
         line: {
            ...Orderline.props.line,
         shape: {
            ...Orderline.props.line.shape,
                rating: { type: [String, Boolean], optional: true },
                 discount: { type: [String, Boolean], optional: true },
             },
            },
           },
        });

patch(PosOrderline.prototype, {
     setup() {
     console.log("PosOrderline setup - discount_limit:",discount_limit);
     },
//},
     getDisplayData() {
     return {
     ...super.getDisplayData(),
     rating: this.get_product().rating || "",
     discount: this.discountStr || "0",
        };
     },
   async set_discount(discount) {
     const parsedDiscount = typeof discount === "number" ? discount :
        isNaN(parseFloat(discount)) ? 0 : parseFloat(discount);
     const disc = Math.min(Math.max(parsedDiscount, 0), 100);
    if (disc > discount_limit) {
        this.dialogService.add(WarningDialog, {
            title: _t("Warning: Reached Limit"),
            message: _t("Warning the discount limit has been reached")
            });
//        this.pos('discount_limit:exceeded', {});
//        await this.services.popup.add(ReachedLimitPopup,{});
        alert(`Reached Discount Limit`)
        this.discount = 0;
        this.discountStr = "0";
        return;
    }
    discount_limit-=disc
    // Valid discount, apply it
    this.discount = disc;
    this.discountStr = "" + disc;
   },
});
