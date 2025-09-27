/** @odoo-module **/

import { ListRenderer } from "@web/views/list/list_renderer";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { onMounted } from "@odoo/owl";

patch(ListRenderer.prototype, {
    setup() {
        super.setup();
        this.orm = useService("orm");
        this.salespersons = [];

        onMounted(() => {
            this.fetchSalespersons();
        });
    },

    async fetchSalespersons() {
        const users = await this.orm.searchRead(
            "res.users",
            [["active", "=", true]],
            ["id", "name"]
        );
        this.salespersons = users;
        this.populateDropdown(users);
    },

    populateDropdown(users) {
        const select = document.getElementById("salespersonSelect");
        if (!select) return;

        select.innerHTML = '<option value=""></option>';
        users.forEach((user) => {
            const option = document.createElement("option");
            option.value = user.id;
            option.textContent = user.name;
            select.appendChild(option);
        });

        console.log("Dropdown options populated");
    },
});
