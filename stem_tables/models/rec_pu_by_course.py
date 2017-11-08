# -*- coding: utf-8 -*-

from odoo import models, fields, api

class rec_pu_by_course(models.Model):
    _name = 'rec.pu.by.course'  
    user_id= fields.Many2one('res.users')
    blog_post_id = fields.Many2one('blog.post')
    computed_date = fields.Datetime()