# -*- coding: utf-8 -*-

from odoo import models, fields, api

class rec_cu_by_faculty(models.Model):
    _name = 'stem.rec_cu_by_faculty'  
    user_id= fields.Many2one('res.users')
    course_id = fields.Many2one('op.course')
    computed_date = fields.Datetime()

class rec_cs_by_faculty(models.Model):
    _name = 'stem.rec_cs_by_faculty'  
    student_id= fields.Many2one('op.student')
    course_id = fields.Many2one('op.course')
    computed_date = fields.Datetime()


class rec_cu_by_gam_chal(models.Model):
    _name = 'stem.rec_cu_by_gam_chal'   
   user_id= fields.Many2one('res.users','user_id')
    course_id = fields.Many2one('op.course', 'course_id')
    computed_date = fields.Datetime()

class rec_cs_by_gam_chal(models.Model):
    _name = 'stem.rec_cs_by_gam_chal'   
    student_id= fields.Many2one('op.student', 'student_id')
    course_id = fields.Many2one('op.course', 'course_id')
    computed_date = fields.Datetime()

 class rec_cu_by_category(models.Model):
    _name = 'stem. rec_cu_by_category'    
    user_id= fields.Many2one('res.users','user_id')
    course_id = fields.Many2one('op.course', 'course_id')
    computed_date = fields.Datetime()

  class rec_cs_by_category(models.Model):
    _name = 'stem. rec_cs_by_category'    
    sstudent_id= fields.Many2one('op.student', 'student_id')
    course_id = fields.Many2one('op.course', 'course_id')
    computed_date = fields.Datetime()


 class reccubysubject(models.Model):
    _name = 'academy.rec_cu_by_subject'    
    user_id= fields.Many2one('res.users','user_id')
    course_id = fields.Many2one('op.course', 'course_id')
    computed_date = fields.Datetime()


 class reccsbysubject(models.Model):
    _name = 'academy.rec_cs_by_subject'
    
    student_id= fields.Many2one('op.student', 'student_id')
    course_id = fields.Many2one('op.course', 'course_id')
    computed_date = fields.Datetime()

 class reccubypredef(models.Model):
    _name = 'academy.rec_cu_by_predef'
    
   user_id= fields.Many2one('res.users','user_id')
    course_id = fields.Many2one('op.course', 'course_id')
    computed_date = fields.Datetime()

 class reccsbypredef(models.Model):
    _name = 'academy.rec_cs_by_predef'    
   student_id= fields.Many2one('op.student', 'student_id')
    course_id = fields.Many2one('op.course', 'course_id')
    computed_date = fields.Datetime()

 class recpubycourse(models.Model):
    _name = 'academy.rec_pu_by_course'  
     user_id= fields.Many2one('res.users','user_id')
    course_id = fields.Many2one('op.course', 'course_id')
    computed_date = fields.Datetime()


  class recpsbycourse(models.Model):
    _name = 'academy.rec_ps_by_course'    
    student_id= fields.Many2one('op.student', 'student_id')
    course_id = fields.Many2one('op.course', 'course_id')
    computed_date = fields.Datetime()

  class recpubyfaculty(models.Model):
    _name = 'academy.rec_pu_by_faculty'   
    user_id= fields.Many2one('res.users','user_id')
    course_id = fields.Many2one('op.course', 'course_id')
    computed_date = fields.Datetime()


   class recpsbyfaculty(models.Model):
    _name = 'academy.rec_ps_by_faculty'   
    student_id= fields.Many2one('op.student', 'student_id')
    course_id = fields.Many2one('op.course', 'course_id')
    computed_date = fields.Datetime()

   
    class recpubyfacultyrep(models.Model):
    _name = 'academy.rec_pu_by_faculty_rep'   
    user_id= fields.Many2one('res.users','user_id')
    course_id = fields.Many2one('op.course', 'course_id')
    computed_date = fields.Datetime()

     class recps_byfacultyrep(models.Model):
    _name = 'academy.rec_ps_by_faculty_rep'
    student_id= fields.Many2one('op.student', 'student_id')
    course_id = fields.Many2one('op.course', 'course_id')
    computed_date = fields.Datetime()