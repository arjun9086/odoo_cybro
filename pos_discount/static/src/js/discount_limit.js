odoo.define('pos_session_discount_limit.DiscountButton', function (require) {
    'use strict';
    const DiscountButton = require('pos_discount.DiscountButton');
    const Registries = require('point_of_sale.Registries');

    const PosSessionDiscountButton = DiscountButton => class extends DiscountButton {
        async apply_discount(value, discountType) {
            const session = this.env.pos.get_session();
            const totalDiscount = session.total_discount_applied || 0;
            const maxDiscount = session.max_discount_limit || 0;
            const order = this.env.pos.get_order();
            let discountAmount = discountType === 'percentage' ? (value / 100) * order.get_total_with_tax() : value;

            if (totalDiscount + discountAmount > maxDiscount && maxDiscount > 0) {
                await this.showPopup('ErrorPopup', {
                    title: this.env._t('Discount Limit Exceeded'),
                    body: this.env._t('The total discount in this session exceeds the allowed limit.'),
                });
                return;
            }
            return super.apply_discount(value, discountType);
        }
    };

    Registries.Component.extend(DiscountButton, PosSessionDiscountButton);
    return PosSessionDiscountButton;
});