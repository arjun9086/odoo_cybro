/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.Rentals = publicWidget.Widget.extend({
    selector: "#rental_form_wrap",
    events: {
        'click .add_rental_line': '_onAddLine',
        'click .remove_rental_line': '_onRemoveLine',
        'change select[name^="property_id_"]': '_onPropertyChange',
        'change #start_date, #end_date': '_onDateChange',
        'change #type': '_onTypeChange'
    },

    _onAddLine: function (ev) {
    ev.preventDefault();
    const index = $('.property_order_line').length;
    const $last = $('.property_order_line').last();
    const $new = $last.clone();

    $new.find('select[name^="property_id_"]').attr('name', 'property_id_' + index).val('');
    $new.find('input[name^="quantity_"]').attr('name', 'quantity_' + index).val('');
    $new.find('input[name^="rent_amount_"]').attr('name', 'rent_amount_' + index).val('');
    $new.find('input[name^="subtotal_"]').attr('name', 'subtotal_' + index).val('');

    $new.find('td:last').html('<button type="button" class="btn btn-danger remove_rental_line">Delete</button>');
    $('#rental_lines_container').append($new);
    this._onDateChange();
    this._updatePropertyOptions();
    },

    _onRemoveLine: function (ev) {
        ev.preventDefault();
        const $row = $(ev.currentTarget).closest('tr.property_order_line');
        if ($('.property_order_line').length > 1) {
            $row.remove();
            this._reindexLines();
            this._updatePropertyOptions();
        }
    },

    _reindexLines: function () {
        $('.property_order_line').each(function (i, row) {
            const $row = $(row);
            $row.find('select[name^="property_id_"]').attr('name', 'property_id_' + i);
            $row.find('input[name^="quantity_"]').attr('name', 'quantity_' + i);
            $row.find('input[name^="rent_amount_"]').attr('name', 'rent_amount_' + i);
            $row.find('input[name^="subtotal_"]').attr('name', 'subtotal_' + i);
        });
    },

    _onPropertyChange: function (ev) {
        const $select = $(ev.currentTarget);
        const propId = $select.val();
        const $row = $select.closest('tr');
        if (!propId) return;

        $.get('/property/rent/' + propId).then(function (data) {
            const type = $('#type').val();
            const rent = type === 'rent'
            ? parseFloat(data.rent_amount || 0)
            : parseFloat(data.lease_amount || 0);
            const qty = parseFloat($row.find('input[name^="quantity_"]').val() || 0);
            $row.find('input[name^="rent_amount_"]').val(rent);
            $row.find('input[name^="subtotal_"]').val((qty * rent).toFixed(2));
            self._updatePropertyOptions();
        });
    },

    _onDateChange: function () {
        const $start = $('#start_date');
        const $end = $('#end_date');
        const startVal = $start.val();
        const endVal = $end.val();

        if (!startVal || !endVal) return;

        const start = new Date(startVal);
        const end = new Date(endVal);
        if (isNaN(start.getTime()) || isNaN(end.getTime()) || end <= start) return;
        const diffDays = Math.floor((end - start) / (1000 * 60 * 60 * 24));
//        if (diffDays=0)
        $('.property_order_line').each(function () {
            const $row = $(this);
            $row.find('input[name^="quantity_"]').val(diffDays);
            const rent = parseFloat($row.find('input[name^="rent_amount_"]').val() || 0);
            $row.find('input[name^="subtotal_"]').val((diffDays * rent).toFixed(2));
        });
    },

    _updatePropertyOptions: function () {
    // Gather all selected property values
    const selected = [];
    $('select[name^="property_id_"]').each(function () {
        const val = $(this).val();
        if (val) selected.push(val);
    });
    $('select[name^="property_id_"]').each(function () {
        const $select = $(this);
        const currentVal = $select.val();

        $select.find('option').each(function () {
            const $option = $(this);
            const val = $option.attr('value');

            if (!val || val === currentVal) {
                $option.prop('disabled', false); // Always allow current or empty
            } else {
                $option.prop('disabled', selected.includes(val));
            }
        });
    });
    },
    _onTypeChange: function () {
    const self = this;
    $('select[name^="property_id_"]').each(function () {
        $(this).trigger('change');
    });
}
});