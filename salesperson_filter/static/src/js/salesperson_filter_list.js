/** @odoo-module */
import { ListController } from "@web/views/list/list_controller";
import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { useState, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { SearchModel } from "@web/search/search_model";

export class StockListController extends ListController {
    setup() {
        super.setup();
        this.state = useState({ salespersons: [] });
        this.orm = useService("orm");
        onWillStart(async () => {
            const users = await this.orm.searchRead('res.users', [['share', '=', false]], ['name']);
            this.state.salespersons = users;
        });
    }
    onSalespersonChange(ev) {
        const selectedId = parseInt(ev.target.value);
//        this.trigger("salesperson-selected", { selectedId });
        const domain = selectedId ? [["user_id", "=", selectedId]] : [];
//        this.env.searchModel.setDomainParts({
//            custom_salesperson: domain,
//        });
//        this.actionService.doAction({
//            type: "ir.actions.act_window",
//            res_model: this.props.resModel,
//            view_mode: "list",
//            domain: domain,
//            target: "current",
//            views: [[false, "list"]],
//        });
        console.log("Selected Salesperson ID:", selectedId);
    }
}
StockListController.template = "module.stock.ListView.Filter";

export const customStockListController = {
    ...listView,
    Controller: StockListController,
};
registry.category("views").add("filter_in_list", customStockListController);

