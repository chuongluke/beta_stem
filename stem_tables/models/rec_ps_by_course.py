# -*- coding: utf-8 -*-

from odoo import models, fields, api

class rec_ps_by_course(models.Model):
    _name = 'stem.rec_ps_by_course'    
    student_id= fields.Many2one('op.student')
    blog_post_id = fields.Many2one('blog.post')
    computed_date = fields.Datetime()