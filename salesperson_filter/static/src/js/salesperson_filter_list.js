/** @odoo-module **/
import { ListController } from "@web/views/list/list_controller";
import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { useState, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { user } from "@web/core/user";

export class CrmListController extends ListController {
    setup() {
        super.setup();
        this.orm = useService("orm");
        this.user = user;
        this.state = useState({
            salespersons: [],
            selectedSalesperson: null,
        });

        onWillStart(async () => {
            const users = await this.orm.searchRead('res.users', [['share', '=', false]], ['name']);
            this.state.salespersons = users;
            this.state.selectedSalesperson = this.user.userId.toString();
            this.applySalespersonFilter(this.state.selectedSalesperson);
        });
    }

    onSalespersonChange(ev) {
        const selectedId = ev.target.value;
        this.state.selectedSalesperson = selectedId;
        this.applySalespersonFilter(selectedId);
    }

    applySalespersonFilter(userId) {
        const searchModel = this.env.searchModel;
        if (!searchModel) {
            console.warn("SearchModel not available");
            return;
        }
        const selectedId = parseInt(userId);
        const domain = selectedId ? [["user_id", "=", selectedId]] : [];
        searchModel.clearQuery();
        searchModel.createNewFilters([
            {
                id: "salesperson_filter",
                description: selectedId
                    ? `Salesperson: ${this.state.salespersons.find(u => u.id === selectedId)?.name || ''}`
                    : "All Salespersons",
                domain: domain,
                isDefault: false,
                groupId: "custom_filters",
            },
        ]);
    }
}
CrmListController.template = "module.stock.ListView.Filter";
export const customCrmListController = {
    ...listView,
    Controller: CrmListController,
};
registry.category("views").add("filter_in_list", customCrmListController);
