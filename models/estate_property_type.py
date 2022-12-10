from odoo import models, fields

class estate_property_type(models.Model):
    _name = "estate.property.type"
    _description = "This model contains the records of property type like bunglow"
    
    _sql_constraints = [
        ("unique_name", "unique(name)", "This Property Type already exists.")
    ]
    _order = "name"

    name = fields.Char("Property Type", required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order the property types")
    property_ids = fields.One2many("estate.property", "property_type_id", string="Property")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Property Offers")
    offer_count = fields.Integer("Offer Count",compute="_compute_offer_count")

    def _compute_offer_count(self):
        for rec in self:
            rec.offer_count = len(self.offer_ids)

    def button_offers_entries(self):
        return {
            'name': "Offer_entries",
            'view_mode': 'tree',
            'res_model': 'estate.property.offer',
            'type': 'ir.actions.act_window',
            'domain': [('property_id', 'in', self.property_ids.mapped('id'))]
        }