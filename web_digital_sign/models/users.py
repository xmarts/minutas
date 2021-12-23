#-*- coding: utf-8 -*-
from odoo import models, fields


class Users(models.Model):
    _inherit = "res.users"

    digital_signature = fields.Binary(string="Signature")
