/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState } from "@odoo/owl";

class SystrayQrcode extends Component {
    setup() {
        this.state = useState({
            inputText: "",
            qrcodeUrl: null,
            isVisible: false,
        });
    }

    togglePopover() {
        this.state.isVisible = !this.state.isVisible;
    }

    generateQR() {
        if (this.state.inputText.trim()) {
            this.state.qrcodeUrl = `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(this.state.inputText)}`;
        }
    }

    reset() {
        this.state.inputText = "";
        this.state.qrcodeUrl = null;
    }

    downloadQR() {
        if (!this.state.qrcodeUrl) return;
        const link = document.createElement("a");
        link.href = this.state.qrcodeUrl;
        link.download = "qrcode.png";
        link.click();
    }
}

SystrayQrcode.template = "systray_qrcode";
export const systrayItem = {
    Component: SystrayQrcode,
};
registry.category("systray").add("SystrayQrcode", systrayItem, { sequence: 100 });



///** @odoo-module **/
//import { registry } from "@web/core/registry";
//import { useService } from "@web/core/utils/hooks";
//import { Component } from "@odoo/owl";
//import { Dropdown } from "@web/core/dropdown/dropdown";
//import { DropdownItem } from "@web/core/dropdown/dropdown_item";
//import { useDropdownState } from "@web/core/dropdown/dropdown_hooks";
//class SystrayQrcode extends Component {
//   setup() {
//       super.setup();
//       this.notification = useService("notification");
//       this.action = useService("action");
//   }
//   openSaleOrders() {
//             this.action.doAction({
//           type: "ir.actions.act_window",
//           name: "Sale Orders",
//           res_model: "sale.order",
//           views: [[false, "list"], [false, "form"]],
//           target: "current",
//       });
//   }
//}
//SystrayQrcode.template = "systray_qrcode";
//SystrayQrcode.components = { Dropdown, DropdownItem };
//export const systrayItem = {
//   Component: SystrayQrcode,
//};
//registry.category("systray").add("SystrayQrcode", systrayItem, { sequence: 1 });
