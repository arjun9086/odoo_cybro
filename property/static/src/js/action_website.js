/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";
publicWidget.registry.Rentals = publicWidget.Widget.extend({
    selector: "#wrap",
    events: {
        'click .add_rental_line': '_onAddLine',
        'click .remove_rental_line': '_onRemoveLine'
    },
    _onAddLine: function (ev) {
        ev.preventDefault();
        const $template = $('.property_rental_template').first().clone();
        $template.removeClass('property_rental_template d-none').addClass('property_order_line');
        $template.find('select, input').val('');
        $('#rental_lines_container').append($template);
    },
    _onRemoveLine: function (ev) {
        ev.preventDefault();
        $(ev.currentTarget).closest('tr.property_order_line').remove();
    },
});
