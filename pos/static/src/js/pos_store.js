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
import { PosOrder } from "@point_of_sale/app/models/pos_order";

let discount_limit=0;
let remaining_discount_limit=0;
let session_id=null;
let dialogTimeout;

patch(PosStore.prototype, {
     async setup() {
     await super.setup(...arguments);
     const currentSession = this.models['pos.session'].getAll()?.[0] || {};
     discount_limit = currentSession.discount_limit || 0;
     session_id=currentSession.name;
     remaining_discount_limit=discount_limit
     console.log("Session discount limit from backend:",discount_limit)
     },
     deductSessionDiscount(amount) {
        remaining_discount_limit = Math.max(0, remaining_discount_limit - amount);
        console.log(amount)
        console.log("[POS] Deducted", amount, "% → Remaining:", remaining_discount_limit);
    },
});
patch(PosOrder.prototype, {
    async finalize() {
        const totalUsed = this.get_orderlines().reduce((sum, line) => {
            const d = parseFloat(line.get_discount());
            return sum + (isNaN(d) ? 0 : d);
        }, 0);
        this.pos.deductSessionDiscount(totalUsed);
        await super.finalize();
    },
});
patch(Orderline, {
        setup(){
        super.setup();
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
patch(Orderline.prototype, {
    setup() {
        super.setup();
        let dialogTimeout;
        this.dialog = useService("dialog");
        this._reachedLimitHandler = this._reachedLimitHandler.bind(this);
        window.addEventListener("discount_limit_exceeded", this._reachedLimitHandler);
    },
    willUnmount() {
        window.removeEventListener("discount_limit_exceeded", this._reachedLimitHandler);
    },
    async _reachedLimitHandler(event) {
        if (dialogTimeout) return;
        dialogTimeout = setTimeout(() => {
            dialogTimeout = null;
        }, 500);
        await this.dialog.add(WarningDialog, {
           title: "Discount Limit Reached",
           message: `Discount Limit has been reached for the session ${session_id}!`,
        });
      },
});
patch(PosOrderline.prototype, {
     setup() {
     console.log("PosOrderline setup - discount_limit:",discount_limit);
     },
       getRemainingSessionDiscount() {
        return remaining_discount_limit;
    },
     getDisplayData() {
     return {
     ...super.getDisplayData(),
     rating: this.get_product().rating || "",
     discount: this.discountStr || "0",
        };
     },
    async set_discount(discount) {
    const parsedDiscount = typeof discount === "number"
        ? discount
        : isNaN(parseFloat(discount))
        ? 0
        : parseFloat(discount);

    const disc = Math.min(Math.max(parsedDiscount, 0), 100);

    // Get all other orderlines from the current order (excluding this one)
    const order = this.order;
    const orderlines = order ? order.get_orderlines() : [];
    console.log('orderlines',orderlines)
    const otherDiscounts = orderlines.reduce((sum, line) => {
        if (line !== this) {
            const d = parseFloat(line.get_discount());
            return sum + (isNaN(d) ? 0 : d);
        }
        return sum;
    }, 0);

    const remaining = discount_limit - otherDiscounts;

    console.log("Total other discounts:", otherDiscounts);
    console.log("Remaining limit:", remaining);
    console.log("Requested:", disc);

    if (disc > remaining) {
        window.dispatchEvent(new CustomEvent("discount_limit_exceeded", {}));
        this.discount = 0;
        this.discountStr = "0";
        return;
    }

    this.discount = disc;
    this.discountStr = "" + disc;
},

//   async set_discount(discount) {
//     const parsedDiscount = typeof discount === "number" ? discount :
//     isNaN(parseFloat(discount)) ? 0 : parseFloat(discount);
//     const disc = Math.min(Math.max(parsedDiscount, 0), 100);
//     const remaining = this.getRemainingSessionDiscount();
//     console.log(remaining)
//    if (disc > remaining) {
//          window.dispatchEvent(new CustomEvent("discount_limit_exceeded", {}));
//          this.discount = 0;
////        this.discountStr = "0";
//        return;
//    }
//    remaining_discount_limit = Math.max(0,remaining_discount_limit - disc);
//    this.discount = disc;
//    this.discountStr = "" + disc;
//   },
});