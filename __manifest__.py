{
    'name': "Real Estate",
    'version': '1.0',
    'author': "Aayush Shah",
    "category": "Real Estate/Market", 
    'description': """
    A real estate module in odoo
    """,
    "depends": [
        "base",
        "web",
        "website",
    ],
    "data": [
        "security/real_estate_groups.xml",
        "security/ir.model.access.csv",
        "views/base_template.xml",
        "views/menu.xml",
        "views/estate_property_view.xml",
        "views/estate_property_tag_view.xml",
        "views/estate_property_offer_view.xml",
        "views/estate_property_type_view.xml",
        "views/res_users_view.xml",
        "report/estate_property_reports.xml",
        "report/estate_property_templates.xml",
        "views/web_login.xml",
        # "views/template.xml",
    ],
    "sequence": "-1",
    "installable": True,
    "application": True,
}
