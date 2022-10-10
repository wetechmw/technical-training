from datetime import timedelta

from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "the type of the property"

    name = fields.Char(required=True)


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "tag your property"

    name = fields.Char(required=True)


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "manage estate properties"

    name = fields.Char(
        required=True,
    )

    description = fields.Text()

    active = fields.Boolean(
        default=True,
    )

    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("received", "Received"),
            ("accepted", "Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
    )

    postcode = fields.Char()

    seller_id = fields.Many2one(
        "res.users",
        string="Salesman",
        default=lambda self: self.env.user,
    )

    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        copy=False,
    )

    tag_ids = fields.Many2many("estate.property.tag", string="Tags")

    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Type",
    )

    property_offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
        string="Offer",
    )

    date_availability = fields.Date(
        string="Available from",
        copy=False,
        default=lambda self: fields.Date.today() + timedelta(weeks=12),
    )

    expected_price = fields.Float(required=True)

    selling_price = fields.Float(readonly=True, copy=False)

    bedrooms = fields.Integer(default=2)

    living_area = fields.Integer()

    facades = fields.Integer()

    garage = fields.Boolean()

    garden = fields.Boolean()

    total_area = fields.Integer(
        string="Total Area (sqm)",
        compute="_compute_total",
    )

    best_price = fields.Float(string="Best Price", compute="_compute_best_price")

    garden_area = fields.Integer(string="Garden Area (sqm)")

    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("east", "East"),
            ("south", "South"),
            ("west", "West"),
        ],
    )

    @api.depends("garden_area", "living_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("property_offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            prices = record.property_offer_ids.mapped("price")
            record.best_price = max(prices) if prices else 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_orientation = "north"
            self.garden_area = 10
        else:
            self.garden_orientation = ""
            self.garden_area = 0
