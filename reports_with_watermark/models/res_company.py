# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ResCompany(models.Model):

    _inherit = "res.company"
    _description = "Report add Company Logo ,Company Name & Background Image"

    upload_image = fields.Binary("Upload Image",
                                 attachment=True,
                                 help="This field holds the image used for" +
                                 "the badge, limited to 256x256")
    rotate_image = fields.Boolean(string='Rotate')
    watermark = fields.Boolean(string='Watermark')
    watermark_option = fields.Selection([
                                        ('logo', 'Company Logo'),
                                        ('name', 'Company Name'),
                                        ('backgroundimage', 'Background Image'
                                         )],
                                        default='logo', string="Watermark " +
                                        "Option")
    rotate_angle = fields.Char(string='Rotate Angle')

    font_size = fields.Char(string='Font Size', default=20)
    font_color = fields.Char(string="Font Color")

    @api.onchange('watermark')
    def onchange_watermark(self):
        if self.watermark:
            self.watermark_option = ""
            self.font_size = ""
            self.rotate_angle = ""
            self.font_size = ""
            self.font_color = ""
            self.upload_image = 0
            self.rotate_image = ""

    @api.onchange('watermark_option')
    def onchange_watermark_option(self):
        if self.watermark_option == 'backgroundimage':
            self.upload_image = 0
        if self.watermark_option == 'name':
            self.rotate_image = ""
            self.rotate_angle = ""
            self.font_size = ""
            self.font_color = ""
