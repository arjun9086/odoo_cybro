/** @odoo-module **/
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component } from "@odoo/owl";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";
import { useDropdownState } from "@web/core/dropdown/dropdown_hooks";
class SystrayQrcode extends Component {
   setup() {
       super.setup();
       this.notification = useService("notification");
       this.action = useService("action");
   }
   openSaleOrders() {
             this.action.doAction({
           type: "ir.actions.act_window",
           name: "Sale Orders",
           res_model: "sale.order",
           views: [[false, "list"], [false, "form"]],
           target: "current",
       });
   }
}
SystrayQrcode.template = "systray_qrcode";
SystrayQrcode.components = { Dropdown, DropdownItem };
export const systrayItem = {
   Component: SystrayQrcode,
};
registry.category("systray").add("SystrayQrcode", systrayItem, { sequence: 1 });
