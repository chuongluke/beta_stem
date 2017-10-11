# -*- coding: utf-8 -*-

from odoo import models, fields, api

class rec_pu_by_faculty_rep(models.Model):
    _name = 'stem.rec_pu_by_faculty_rep'   
    user_id= fields.Many2one('res.users')
    blog_post_id = fields.Many2one('blog.post')
    computed_date = fields.Datetime()