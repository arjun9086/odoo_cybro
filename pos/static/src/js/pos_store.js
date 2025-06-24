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
import { PosPayment } from "@point_of_sale/app/models/pos_payment";

let discount_limit=0;
let remaining_discount_limit=0;
let dialogTimeout;
let session_id=null;

patch(PosStore.prototype, {
     async setup() {
     await super.setup(...arguments);
     const currentSession = this.models['pos.session'].getAll()?.[0]||{};
     discount_limit = currentSession.discount_limit || 0;
     session_id=currentSession.name;
     remaining_discount_limit=discount_limit;
     console.log("Session discount limit from backend:",discount_limit);
     },
    async pay(){
    const currentOrder = this.get_order();
    const orderlines=currentOrder.get_orderlines();
        const totalDiscount = orderlines.reduce((sum, line) => {
            const discount = line.discount || 0;
            return sum + (discount);
        }, 0);
        console.log('totaldiscount',totalDiscount)
        if (totalDiscount > remaining_discount_limit) {
             window.dispatchEvent(new CustomEvent("discount_limit_exceeded", {}));
            return;
        }
//        if(currentOrder.canPay()){
//        return remaining_discount_limit=discount_limit;
//        }

        console.log('remaining',remaining_discount_limit)
        currentOrder._pending_discount = totalDiscount;
        await super.pay(...arguments);
        if (this.payment_status=='done')
        {
        remaining_discount_limit -= totalDiscount;
        }
    },
});
patch(PosPayment.prototype,{
    async is_done(){
    if (this.get_payment_status() === "done")
        {
        remaining_discount_limit -= totalDiscount;
        }
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
     getDisplayData() {
     return {
        ...super.getDisplayData(),
         rating: this.get_product().rating || "",
        };
     },
});

