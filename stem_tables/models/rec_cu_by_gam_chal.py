# -*- coding: utf-8 -*-

from odoo import models, fields, api

class rec_cu_by_gam_chal(models.Model):
    _name = 'stem.rec_cu_by_gam_chal'   
    user_id= fields.Many2one('res.users')
    course_id = fields.Many2one('op.course')
    computed_date = fields.Datetime()