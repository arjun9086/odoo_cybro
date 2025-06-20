import { Dialog } from "@web/core/dialog/dialog";
import { Component, useState } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { registry } from "@web/core/registry";

export class ReachedLimitPopup extends Component {
    static components = { Dialog };
    static template = "pos.ReachedLimitPopup";
    static props = ["close", "title","body"];

    setup() {};

    confirm() {
//        this.props.getPayload([...this.state.selectedTours]);
        this.props.close();
        }
    }
