from datetime import datetime


from odoo import models,fields,api
from odoo.addons.test_new_api.models.test_new_api import Display


class property(models.Model):
    _name = "property.main"
    _description='Property Management'


    _inherit =['mail.thread']

    name=fields.Char(required=True)
    # address=fields.Char()
    street1=fields.Char()
    street2=fields.Char()
    state=fields.Char()
    country=fields.Char()
    built_date=fields.Date(default=datetime.today())
    description=fields.Html()
    owner=fields.Many2one('res.partner',string='Owner')
    can_be_sold=fields.Boolean()
    legal_amount=fields.Char()
    image=fields.Binary()
    rent=fields.Char()
    status=fields.Selection(
        selection=[
            ('rented', 'Rented'),
            ('leased', 'Leased'),
            ('sold', 'Sold'),
            ('draft','Draft')],
    string = 'Status',
    default = 'rented',
    tracking=True,
    # track_visibility = 'onchange'
    )


