/** @odoo-module **/
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { patch } from "@web/core/utils/patch";

patch(ControlButtons.prototype, {
    async onClickClearAll() {
        const order = this.pos.get_order();
        const orderline = order.get_orderlines();
        orderline.filter(line=>line.get_product()).forEach(single_line=>order.removeOrderline(single_line));
    }
});
