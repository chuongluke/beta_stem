# -*- coding: utf-8 -*-

from odoo import models, fields, api

class rec_cs_by_subject(models.Model):
    _name = 'rec.cs.by.subject'
    student_id= fields.Many2one('op.student')
    course_id = fields.Many2one('op.course')
    computed_date = fields.Datetime()