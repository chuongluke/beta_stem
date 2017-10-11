# -*- coding: utf-8 -*-

from odoo import models, fields, api

class rec_cs_by_category(models.Model):
    _name = 'stem.rec_cs_by_category'    
    student_id= fields.Many2one('op.student')
    course_id = fields.Many2one('op.course')
    computed_date = fields.Datetime()