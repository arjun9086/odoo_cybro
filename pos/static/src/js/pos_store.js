/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { Orderline } from "@point_of_sale/app/generic_components/orderline/orderline";
import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
import { _t } from "@web/core/l10n/translation";
import { parseFloat } from "@web/views/fields/parsers";
import { useListener } from "@web/core/utils/hooks";
import { WarningDialog } from "@web/core/errors/error_dialogs";
import { useService } from "@web/core/utils/hooks";
import { ActionpadWidget } from "@point_of_sale/app/screens/product_screen/action_pad/action_pad";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";

patch(PosStore.prototype, {
    async setup() {
     await super.setup(...arguments);
     const currentSession = this.models['pos.session'].getAll()?.[0]||{};
     let discount_limit=0;
     discount_limit = currentSession.discount_limit || 0;
     let session_id=currentSession.name;
     this.remaining_discount_limit=discount_limit;
     console.log("Session discount limit from backend:",discount_limit);
    },
    async pay(){
     const currentOrder = this.get_order();
     const orderlines= currentOrder.get_orderlines();
     const totalDiscount = orderlines.reduce((sum, line) => {
     const discount = line.discount || 0;
     console.log(this.remaining_discount_limit)
     return sum + (discount);
     }, 0);
     if (totalDiscount > this.remaining_discount_limit) {
         window.dispatchEvent(new CustomEvent("discount_limit_exceeded", {}));
         return;
     }
     currentOrder._pending_discount = totalDiscount;
     await super.pay(...arguments);
     },
});
patch(PaymentScreen.prototype,{
     async validateOrder() {
        await super.validateOrder(...arguments);
        const currentOrder = this.pos.get_order();
         console.log('order',currentOrder)
        if (this.currentOrder && currentOrder._pending_discount) {
            this.pos.remaining_discount_limit -= this.currentOrder._pending_discount;
            console.log('payment screen',this.pos.remaining_discount_limit)
            currentOrder._pending_discount = 0;
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
     this.dialogTimeout=null;
     this.dialog = useService("dialog");
     this._reachedLimitHandler = this._reachedLimitHandler.bind(this);
     window.addEventListener("discount_limit_exceeded", this._reachedLimitHandler);
     },
 willUnmount() {
    window.removeEventListener("discount_limit_exceeded", this._reachedLimitHandler);
    },
 async _reachedLimitHandler(event) {
     if (this.dialogTimeout) return;
     this.dialogTimeout = setTimeout(() => {
     this.dialogTimeout = null;
    }, 500);
     await this.dialog.add(WarningDialog, {
     title: "Discount Limit Reached",
     message: `Discount Limit has been reached for the session!`,
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
