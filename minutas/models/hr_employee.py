# #-*- coding: utf-8 -*-
# from odoo import models, fields


# class hrEmployeeMinutas(models.Model):
#     _name='hr.employee'
#     _inherit='hr.employee'

#     employe_minutas_count = fields.Integer(string="", default=0, compute="count_minutas_employee")

#     def count_minutas_employee(self):
#         cr = self.env.cr
#         sql = "select coalesce(count(distinct mx.id),0) from minutas_xmarts mx inner join minutas_xmarts_asistenciain mxa on mx.id=mxa.minuta_id where mxa.name='"+str(self.id)+"';"
#         cr.execute(sql)
#         minutas = cr.fetchone()
#         self.employe_minutas_count=minutas[0]
