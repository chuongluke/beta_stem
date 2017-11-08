# -*- coding: utf-8 -*-

from odoo import models, fields, api

class rec_cu_by_category(models.Model):
    _name = 'rec.cu.by.category'   
    user_id = fields.Many2one('res.users')
    course_id = fields.Many2one('op.course')
    computed_date = fields.Datetime()