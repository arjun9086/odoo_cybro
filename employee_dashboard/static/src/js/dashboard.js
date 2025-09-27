/** @odoo-module **/
import { Component, useState, onMounted } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { loadJS } from "@web/core/assets";

const actionRegistry = registry.category("actions");

export class EmployeeDashboard extends Component {
    static template = "employee_dashboard.EmployeeDashboard";

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.state = useState({ data: null });
        this.filteredTasks = useState({ list: [] });
        this.filter = useState({
            deadline: "all",
            start_date: null,
            end_date: null,
        });
        this.taskChartInstance = null;
        this.experienceChartInstance = null;
        onMounted(async () => {
            await loadJS("https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js");
            await this.loadDashboardData();
        });
    }
    async loadDashboardData() {
        const context = {
            date_start: this.filter.start_date,
            date_end: this.filter.end_date,
        };
        const data = await this.orm.call(
            "hr.employee.dashboard",
            "get_employee_dashboard_data",
            [this.filter.start_date, this.filter.end_date],
            { context }
        );
        this.state.data = data;
        this.filteredTasks.list = this.filterTasks(data.tasks, this.filter.deadline);
        this.renderTaskProjectChart();
        this.renderExperienceChart();
    }
    onDateRangeApply() {
        this.loadDashboardData();
    }
    onCardClick(ev) {
        const type = ev.currentTarget.dataset.type;
        if (type === "attendance"){
            this.action.doAction("hr_attendance.hr_attendance_action");
        } else if (type === "leave"){
            this.action.doAction("hr_holidays.hr_leave_action_my");
        } else if (type === "project") {
            this.action.doAction("project.open_view_project_all");
        } else if (type === "task") {
            this.action.doAction("project.action_view_all_task");
        } else if (type === "personal_information") {
            this.action.doAction("hr.hr_employee_public_action");
        }
    }
    onTaskClick(ev) {
        const taskId = ev.currentTarget.dataset.taskId;
        if (!taskId) {
            alert("No task ID found");
            return;
        }
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "project.task",
            res_id: parseInt(taskId),
            views: [[false, "form"]],
            target: "current",
        });
    }
    renderTaskProjectChart() {
        const canvas = document.getElementById("taskProjectChart");
        const tasks = this.state.data?.tasks || [];
//        const tasks = (this.state.data?.tasks || []).filter(task => {
//            const date = task.deadline ? new Date(task.deadline) : null;
//            if (!date) return false;
//
//            const start = this.filter.start_date ? new Date(this.filter.start_date) : null;
//            const end = this.filter.end_date ? new Date(this.filter.end_date) : null;
//
//            if (start && date < start) return false;
//            if (end && date > end) return false;
//            return true;
//        });
        if (this.taskChartInstance) {
        this.taskChartInstance.destroy();
        }
        const projectCounts = {};
        tasks.forEach(task => {
            const project = task.project || "Unassigned";
            projectCounts[project] = (projectCounts[project] || 0) + 1;
        });
        const labels = Object.keys(projectCounts);
        const counts = Object.values(projectCounts);
        this.taskChartInstance = new Chart(canvas, {
            type: "bar",
            data: {
                labels: labels,
                datasets: [{
                    label: "Tasks per Project",
                    data: counts,
                    backgroundColor: "rgba(54, 162, 235, 0.6)",
                    borderColor: "rgba(54, 162, 235, 1)",
                    borderWidth: 1,
                }],
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: "Number of Tasks",
                        },
                    },
                    x: {
                        title: {
                            display: true,
                            text: "Projects",
                        },
                    },
                },
            },
        });
    }
    renderExperienceChart() {
        const canvas = document.getElementById("experienceChart");
        const resumeLines = this.state.data?.experience || [];
//        const resumeLines = (this.state.data?.experience || []).filter(line => {
//            const start = line.date_start ? new Date(line.date_start) : null;
//            const end = line.date_end ? new Date(line.date_end) : new Date();
//
//            const filterStart = this.filter.start_date ? new Date(this.filter.start_date) : null;
//            const filterEnd = this.filter.end_date ? new Date(this.filter.end_date) : null;
//
//            if (filterStart && end < filterStart) return false;
//            if (filterEnd && start > filterEnd) return false;
//            return true;
//        });
        if (!resumeLines.length || !window.Chart) {
            console.warn("Chart.js not loaded or resumeLines empty.");
            return;
        }
        if (this.experienceChartInstance) {
        this.experienceChartInstance.destroy();
        }
        const labels = [];
        const durations = [];
        resumeLines.forEach(line => {
            const start = line.date_start ? new Date(line.date_start) : null;
            const end = line.date_end ? new Date(line.date_end) : new Date();
            if (start) {
                const diffYears = ((end - start) / (1000 * 60 * 60 * 24 * 365)).toFixed(1);
                labels.push(line.name || "Unknown");
                durations.push(parseFloat(diffYears));
            }
        });
        this.experienceChartInstance = new Chart(canvas, {
            type: "line",
            data: {
                labels: labels,
                datasets: [{
                    label: "Experience (years)",
                    data: durations,
                    fill: false,
                    borderColor: "#3498DB",
                    backgroundColor: "#3498DB",
                    tension: 0.3,
                    pointRadius: 5,
                    pointBackgroundColor: "#2980B9",
                }],
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: true },
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: "Years",
                        },
                    },
                    x: {
                        title: {
                            display: true,
                            text: "Experience Name",
                        },
                    },
                },
            },
        });
    }
    onDeadlineFilterChange(ev) {
        const selected = ev.target.value;
        this.filter.deadline = selected;
        this.filteredTasks.list = this.filterTasks(this.state.data.tasks, selected);
    }
    filterTasks(tasks, filterType) {
        const now = new Date();
        const currentMonth = now.getMonth();
        const currentYear = now.getFullYear();
        return tasks.filter(task => {
            if (!task.deadline) return false;
            const deadline = new Date(task.deadline);
            switch (filterType) {
                case "this_month":
                    return deadline.getMonth() === currentMonth && deadline.getFullYear() === currentYear;
                case "upcoming":
                    return deadline > now;
                case "overdue":
                    return deadline < now;
                case "all":
                default:
                    return true;
            }
        });
    }
}
actionRegistry.add("employee_dashboard_tag", EmployeeDashboard);

