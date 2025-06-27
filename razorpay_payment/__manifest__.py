{
    'name': 'RazorPay Payment',
    'description': 'Razorpay Payment Provider',
    'version': '18.0.1.0',
    'data': [
        'views/payment_provider_view.xml',
        'data/payment_provider_data.xml',
        'data/payment_method_data.xml'
    ],
    'depends': ['base', 'payment_razorpay','payment_razorpay_oauth','payment'],
    'installable': True,
    'auto_install': False,
}
