from datetime import timedelta
from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "make an offer"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
    )

    partner_id = fields.Many2one(
        "res.partner",
        required=True,
    )

    property_id = fields.Many2one(
        "estate.property",
        required=True,
    )

    validity = fields.Integer(default=7)

    # ToDo Datetime may be the better type, since it will be computed with create_date
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_deadline",
        inverse="_inverse_deadline",
        store=False,
    )

    
    @api.depends("validity", "create_date")
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = (record.create_date.date() or fields.Date.today()) + timedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

