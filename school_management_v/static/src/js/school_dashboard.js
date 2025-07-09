/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";

class SchoolDashboard extends Component {
    static template = "school_management_v.SchoolDashboard";
}

registry.category("actions").add("school_management_v.dashboard", SchoolDashboard);
