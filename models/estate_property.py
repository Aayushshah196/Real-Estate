from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import date
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"

    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price > 0)",
            "The expected price must be greater than 0",
        )
    ]

    def _default_date_availability(self):
        return date.today() + relativedelta(months=3)

    # Fields or columns in the database table
    name = fields.Char("Title", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Post Code")
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float(
        "Selling Price", copy=False, required=True, read_only=True
    )
    best_offer = fields.Float("Best Offer", compute="_compute_best_offer")

    date_availability = fields.Date(
        "Date Availability From",
        copy=False,
        default=lambda self: self._default_date_availability(),
    )
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage Space")
    garden = fields.Boolean("Garden")
    garden_area = fields.Float("Garden Area")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[("N", "North"), ("S", "South"), ("E", "East"), ("W", "West")],
    )
    total_area = fields.Float("Total Area sq m", compute="_compute_total_area")
    active = fields.Boolean("Active", default=True)
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        string="Status",
        default="new",
    )

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one(
        "res.partner", string="Buyer", read_only=True, copy=False
    )
    seller_id = fields.Many2one(
        "res.users", string="Salesman", default=lambda self: self.env.user
    )
    property_tag_ids = fields.Many2many("estate.property.tag", string="Property Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    def _compute_best_offer(self):
        for rec in self:
            rec.best_offer = (
                max(rec.offer_ids.mapped("price")) if rec.offer_ids else 0.0
            )

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "N"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.constrains("selling_price")
    def _constraint_selling_price(self):
        if self.selling_price < self.expected_price * 0.9:
            raise UserError(
                "Selling price can not be below 90 percent of expected price"
            )

    # @api.ondelete(at_uninstall=False)
    # def _unlink_except_new_canceled(self):
    #     if self.state not in ("new", "canceled"):
    #         raise UserError("Property not in new or canceled can not be deleted")

    def unlink(self):
        for rec in self:
            if rec.state not in ("new", "canceled"):
                raise UserError("Property not in new or canceled can not be deleted")
        super(EstateProperty, self).unlink()

    def action_on_sold(self):
        if self.state == "canceled":
            raise UserError("Cannot sell a canceled property")
        return self.write({"state": "sold"})

    def action_on_cancel(self):
        if self.state == "sold":
            raise UserError("Cannot cancel a sold property")
        self.state = "canceled"
        return True

    @api.model
    def get_view_mode(self):
        return self.env["estate.property"].search([])
