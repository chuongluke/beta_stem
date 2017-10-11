# -*- coding: utf-8 -*-
import json
import werkzeug.utils
import base64
import logging
import random
from datetime import datetime, timedelta

from odoo import _, http, fields
from odoo.addons.website.controllers.main import Website
from odoo.addons.web.controllers.main import Home
from odoo.addons.auth_signup.controllers.main import AuthSignupHome

_logger = logging.getLogger(__name__)

try:
    from validate_email import validate_email
except ImportError:
    _logger.debug("Cannot import `validate_email`.")

class Stem(http.Controller):
    def get_menu_data(self):
        parent = http.request.env['op.parent'].sudo().search([('name', '=', http.request.env.user.partner_id.id)], limit=1)
        return {
            'parent': parent
        }

    @http.route('/home', auth='user', website=True)
    def home(self, **kw):
        data = self.get_menu_data()

        #online_free_courses
        online_free_courses = http.request.env['op.course'].sudo().search(
            [('online_course', '=', True), ('type', '=', 'free')], limit=3, order='create_date desc')
        data['online_free_courses'] = online_free_courses
        #populor course
        course_porpular = http.request.env['stem.rec_cu_by_predef'].sudo().search([('user_id', '=', http.request.env.uid)], limit=9, order='computed_date desc')
        data['course_porpular'] = course_porpular

        #my courses
        enrollments = http.request.env['op.course.enrollment'].sudo().search(
            [('user_id', '=', http.request.env.uid),
            ('state', 'in', ['in_progress', 'done'])])
        if enrollments:
            data.update(self.my_course_details(enrollments))
        #my courses
        
        return http.request.render('stem_frontend_theme.stem_profile', data)

    @http.route('/googleb90fcbde0047b306.html', auth='public')
    def google_html(self):
        return 'google-site-verification: googleb90fcbde0047b306.html'


    @http.route('/home/my-courses', auth='user', website=True)
    def my_courses(self, **kw):
        data = self.get_menu_data()

        enrollments = http.request.env['op.course.enrollment'].sudo().search(
            [('user_id', '=', http.request.env.uid),
            ('state', 'in', ['in_progress', 'done'])])
        if enrollments:
            data.update(self.my_course_details(enrollments))

        return http.request.render('stem_frontend_theme.stem_my_courses', data)

    def my_course_details(self, enrollments):
        courses = []
        for en in enrollments:
            completed_percentage = 0
            if en and en.course_id.training_material > 0:
                viewed_material = http.request.env[
                    'op.course.enrollment.material'].sudo().search_count([   
                        ('completed', '=', True),
                        ('course_id', '=', en.course_id.id),
                        ('enrollment_id', '=', en.id)
                    ])
                completed_percentage = (viewed_material * 100) / en.course_id.training_material
            courses.append({
                'course': en.course_id,
                'enrolled': en.state in ['in_progress', 'done'] and True or False,
                'completed_percentage': completed_percentage, 
            })
        return {
            'my_courses': courses
        }

    @http.route('/home/register_teacher', auth='user', methods=['POST'], website=True)
    def register_teacher(self, **post):
        name = post.get('name')
        middle_name = post.get('middle_name')
        last_name = post.get('last_name')
        gender = post.get('gender')
        phone = post.get('phone')
        email = post.get('email')
        birth_date = post.get('birth_date')
        
        #birth_date = birth_date.strftime('%Y-%m-%d')
        
        faculty = http.request.env['op.faculty'].search([('user_id', '=', http.request.env.uid)])
        if not faculty:
            fac = http.request.env['op.faculty'].sudo().create({
                'partner_id': http.request.env.user.partner_id.id,
                'last_name': last_name,
                'gender': gender,
                'phone': phone,
                'email': email,
                'birth_date': birth_date,
                'status': 'unapprove'
            })

            if fac:
                vals = {
                    'name': name + ' ' + (middle_name or '') +
                    ' ' + last_name,
                    'country_id': fac.nationality.id,
                    'gender': gender,
                    'address_home_id': fac.partner_id.id
                }
                emp_id = http.request.env['hr.employee'].sudo().create(vals)
                fac.write({'emp_id': emp_id.id})
                fac.partner_id.write({'user_id': http.request.env.uid, 'supplier': True, 'employee': True})

        return http.request.render('stem_frontend_theme.stem_alert', {
            'message': 'Đăng ký thành công, vui lòng chờ xác nhận của quản lý hệ.',
            'type': 'success'
        })

    def random_token(self):
        # the token has an entropy of about 120 bits (6 bits/char * 20 chars)
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
        return ''.join(random.SystemRandom().choice(chars) for i in xrange(20))

    def now(self, **kwargs):
        dt = datetime.now() + timedelta(**kwargs)
        return fields.Datetime.to_string(dt)

    @http.route('/register/parent', type='http', auth="user", methods=['POST'], website=True)
    def register_parent(self, **kw):
        sids = kw.get('student_ids')

        if sids:
            student_ids = [int(i) for i in sids.split(',')]
            template = http.request.env.ref('stem_frontend_theme.register_parent_template')

            for student_id in student_ids:
                token = self.random_token()
                parent_id = http.request.env.user.partner_id.id
                expiration = self.now(days=+1)
                student_child_id = student_id

                registered = http.request.env['stem.register_parent'].sudo().create({
                    'token': token,
                    'parent_id': parent_id,
                    'expiration': expiration,
                    'student_child_id': student_id
                })

                http.request.env['mail.template'].sudo().browse(template.id).send_mail(registered.id, force_send=True)
        return http.request.render('stem_frontend_theme.stem_alert', {
            'message': 'Đăng ký thành công',
            'type': 'success'
        })

            # res = http.request.env['op.parent'].sudo().create({
            #     'name': http.request.env.user.partner_id.id,
            #     'student_ids': [(6, 0, student_ids)]
            # })

        #return http.request.redirect('/home')

    @http.route('/confirm/parent', type='http', auth='public', website=True)
    def confirm_parent(self, **kw):
        token = kw.get('token')
        message = 'Mã xác thực đã hết hạn hoặc không tồn tại'
        alert_type ='danger'
        if token:
            registered = http.request.env['stem.register_parent'].sudo().search([('token', '=', token)], limit=1)
            dt = self.now()
            if registered and token == registered.token and dt <= registered.expiration:
                parent = http.request.env['op.parent'].sudo().search([('name', '=', registered.parent_id.id)], limit=1)
                if parent:
                    parent.write({
                        'student_ids': [(4, registered.student_child_id.id, 0)]
                    })
                else:
                    http.request.env['op.parent'].sudo().create({
                        'name': registered.parent_id.id,
                        'student_ids': [(6, 0, [registered.student_child_id.id])]
                    })
                message = 'Xác nhận thành công'
                alert_type = 'success'

        return http.request.render('stem_frontend_theme.stem_alert', {
            'message': message,
            'type': alert_type
        })
            
        
    @http.route('/home/my-blogs', auth='user', website=True)
    def my_blogs(self, **kw):
        data = self.get_menu_data()
        return http.request.render('stem_frontend_theme.stem_my_blogs', data)

    @http.route('/home/my-mes', auth='user', website=True)
    def my_mes(self, **kw):
        data = self.get_menu_data()
        my_channels = http.request.env['mail.channel'].sudo().search(
            [('channel_partner_ids', 'in', [http.request.env.user.partner_id.id])],limit=10, order='__last_update asc')
        #_logger.info("my_channels len: " + str(len(my_channels)))
        #for c in my_channels:
        #    _logger.info("my_channels: " + c.public)
        data['partner_id'] = http.request.env.user.partner_id.id
        data['my_channels'] = my_channels
        # for c in data['my_channels']:
        #     body = c.message_ids[0].body
        #     body = self.replaceTag(body)
        #     c['first_body'] = body
        #     _logger.info("body: " + body+"--c['first_body']--"+c['first_body'])

        return http.request.render('stem_frontend_theme.stem_my_mes', data)

    def replaceTag(self, enrollments):
        num = re.sub(r"(<([^>]+)>)", '', enrollments)
        return num

    @http.route('/home/get_student', auth='public', type='http', csrf=False, website=True)
    def get_student(self, **kw):
        start = int(kw.get('start'))
        length = int(kw.get('length'))
        search = kw.get('search[value]')

        total_count = http.request.env['op.student'].sudo().search_count([])
        filtered_count = http.request.env['op.student'].sudo().search_count(['|', ('partner_id.email', 'ilike', search), ('partner_id.name', 'ilike', search)])
        students = http.request.env['op.student'].sudo().search(['|', ('partner_id.email', 'ilike', search), ('partner_id.name', 'ilike', search)], offset=start, limit=length)

        data = []
        for student in students:
            data.append({
                'DT_RowId': student.id,
                'action': '<input type="checkbox"/>',
                'email': student.partner_id.email,
                'name': student.name
            })

        result = {
            'recordsTotal': total_count,
            'recordsFiltered': filtered_count,
            'data': data
        }

        return str(json.dumps(result))

    @http.route('/home/my-child/<int:student_id>', auth='user', website=True)
    def my_child(self, student_id=0):
        data = self.get_menu_data()
        parent = data['parent']
        if parent:
            student_ids = [s for s in parent.student_ids if s.id == student_id]
            if student_ids:
                child = student_ids[0]
                student_user = http.request.env['res.users'].sudo().search([('partner_id', '=', child.partner_id.id)], limit=1)
                student_user_id = student_user.id

                enrollments = http.request.env['op.course.enrollment'].sudo().search(
                    [('user_id', '=', student_user_id),
                    ('state', 'in', ['in_progress', 'done'])])
                if enrollments:
                    data.update(self.my_course_details(enrollments))

                data['child'] = child

                return http.request.render('stem_frontend_theme.stem_my_child_courses', data)
            else:
                return http.request.redirect('/home')
        else:
            return http.request.redirect('/home')

    @http.route('/home/get_messages_by_channel', auth='public', type='http', csrf=False, website=True)
    def get_messages_by_channel(self, **kw):
        channel_id = int(kw.get('channel_id'))

        messages = http.request.env['mail.message'].sudo().search([('res_id', '=', channel_id), ('model', '=', 'mail.channel')], order='create_date desc')
        #result = []
        # for m in messages:
        #     result.append({
        #         'id': m.id,
        #         'body': m.body,
        #         'author_name': m.author_id.name
        #     })

        return http.request.render('stem_frontend_theme.stem_my_mes_detail',  {
            'messages': messages
        })


    @http.route(['''/course/register-course/<model("op.course"):course>'''],
                type='http', auth="user", website=True)
    def register_course(self, course, **kwargs):
        course = http.request.env['op.course'].sudo().browse([course.id])
        faculty = http.request.env['op.faculty'].search([('user_id', '=', http.request.env.uid)])
        if course and faculty:
            course.write({'faculty_ids': [(4, faculty.id, 0)]})

        sections = http.request.env['op.course.section'].sudo().search(
            [('course_id', '=', course.id)], order='sequence asc')

        enrollment = http.request.env['op.course.enrollment'].sudo().search(
            [('user_id', '=', http.request.env.uid),
             ('course_id', '=', course.id),
             ('state', 'in', ['in_progress', 'done'])])

        completed_percentage = enrollment and enrollment.completed_percentage or 0

        ratings = http.request.env['rating.rating'].sudo().search(
            [('message_id', 'in', course.website_message_ids.ids)])
        rating_message_values = dict(
            [(record.message_id.id, record.rating) for record in ratings])
        rating_course = course.rating_get_stats()
        values = {
            'course': course,
            'enrolled': enrollment and True or False,
            'completed_percentage': completed_percentage,
            'sections': sections,
            'user': http.request.env.user,
            'is_public_user': http.request.env.user == http.request.website.user_id,
            'rating_message_values': rating_message_values,
            'rating_course': rating_course,
            'message': 'Đăng ký thành công.'
        }
        return http.request.render('openeducat_lms.course_detail', values)




class Website(Website):
    @http.route(auth='public')
    def index(self, data={}, **kw):
        super(Website, self).index(**kw)

        if http.request.session.uid:                        
            online_free_courses = http.request.env['op.course'].sudo().search(                
                [('online_course', '=', True), ('type', '=', 'free')], limit=3, order='create_date desc')

            course_porpular = http.request.env['stem.rec_cu_by_predef'].sudo().search([('user_id', '=', http.request.env.uid)], limit=9, order='computed_date desc')

            return http.request.render('stem_frontend_theme.stem_home', {'online_free_courses': online_free_courses, 'course_porpular': course_porpular})        
        else:

            try:   
                providers = http.request.env['auth.oauth.provider'].sudo().search_read([('enabled', '=', True)])
            except Exception:   
                providers = []  
            for provider in providers:   
                return_url = http.request.httprequest.url_root + 'auth_oauth/signin'

                redirect = http.request.params.get('redirect') or 'home'
                if not redirect.startswith(('//', 'http://', 'https://')):
                    redirect = '%s%s' % (http.request.httprequest.url_root, redirect[1:] if redirect[0] == '/' else redirect)
                state = dict(
                    d=http.request.session.db,
                    p=provider['id'],
                    r=werkzeug.url_quote_plus(redirect),
                )
                token = http.request.params.get('token')
                if token:
                    state['t'] = token

                params = dict(    
                    response_type='token',    
                    client_id=provider['client_id'],    
                    redirect_uri=return_url,    
                    scope=provider['scope'],    
                    state=json.dumps(state),   
                )   
                provider['auth_link'] = "%s?%s" % (provider['auth_endpoint'], werkzeug.url_encode(params))

            online_free_courses = http.request.env['op.course'].sudo().search(
                [], limit=5, order='create_date desc')

            all_users = http.request.env['res.users'].sudo().search([])    
            count_all_users = len(all_users)
            all_courses = http.request.env['op.course'].sudo().search([])
            count_all_courses = len(all_courses)
            all_blog_posts = http.request.env['blog.post'].sudo().search([])
            count_all_blog_posts = len(all_blog_posts)


            data = { 
                'online_free_courses': online_free_courses,
                'providers': providers,
                'count_all_users': count_all_users,
                'count_all_courses': count_all_courses, 
                'count_all_blog_posts': count_all_blog_posts
            }

            return http.request.render('stem_frontend_theme.stem_homepage', data)


class AuthSignupHomeTwo(Home):    
    def do_signup(self, qcontext):                
        """ Shared helper that creates a res.partner out of a token """                
        values = { key: qcontext.get(key) for key in ('login', 'name', 'password') }

        if qcontext.get('gender'):
            values['gender'] = qcontext.get('gender')

        if qcontext.get('bd_year') and qcontext.get('bd_month') and qcontext.get('bd_date'):
            values['birthday'] = qcontext.get('bd_year') + '-' + qcontext.get('bd_month') + '-' + qcontext.get('bd_date')       
        assert values.values(), "The form was not properly filled in. "                
        assert values.get('password') == qcontext.get('confirm_password'), "Passwords do not match; please retype them."                
        supported_langs = [lang['code'] for lang in http.request.env['res.lang'].sudo().search_read([], ['code'])]                
        if http.request.lang in supported_langs:                        
            values['lang'] = http.request.lang
        self._signup_with_values(qcontext.get('token'), values)                
        http.request.env.cr.commit()



class SignupVerifyEmail(AuthSignupHome):
    @http.route()
    def web_auth_signup(self, *args, **kw):
        if (http.request.params.get("login") and http.request.params.get("password")):
            return self.passwordless_signup(http.request.params)
        else:
            return super(SignupVerifyEmail, self).web_auth_signup(*args, **kw)

    def passwordless_signup(self, values):
        qcontext = self.get_auth_signup_qcontext()

        try:   
            providers = http.request.env['auth.oauth.provider'].sudo().search_read([('enabled', '=', True)])
        except Exception:   
            providers = []  
        for provider in providers:   
            return_url = http.request.httprequest.url_root + 'auth_oauth/signin'

            redirect = http.request.params.get('redirect') or ''
            if not redirect.startswith(('//', 'http://', 'https://')):
                redirect = '%s%s' % (http.request.httprequest.url_root, redirect[1:] if redirect[0] == '/' else redirect)
            state = dict(
                d=http.request.session.db,
                p=provider['id'],
                r=werkzeug.url_quote_plus(redirect),
            )
            token = http.request.params.get('token')
            if token:
                state['t'] = token

            params = dict(    
                response_type='token',    
                client_id=provider['client_id'],    
                redirect_uri=return_url,    
                scope=provider['scope'],    
                state=json.dumps(state),   
            )   
            provider['auth_link'] = "%s?%s" % (provider['auth_endpoint'], werkzeug.url_encode(params))

        online_free_courses = http.request.env['op.course'].sudo().search(
            [], limit=5, order='create_date desc')

        all_users = http.request.env['res.users'].sudo().search([])    
        count_all_users = len(all_users)
        all_courses = http.request.env['op.course'].sudo().search([])
        count_all_courses = len(all_courses)
        all_blog_posts = http.request.env['blog.post'].sudo().search([])
        count_all_blog_posts = len(all_blog_posts)


        qcontext['online_free_courses'] =  online_free_courses
        qcontext['providers'] = providers
        qcontext['count_all_users'] = count_all_users
        qcontext['count_all_courses'] = count_all_courses 
        qcontext['count_all_blog_posts'] = count_all_blog_posts


        """ Shared helper that creates a res.partner out of a token """                
        values = { key: qcontext.get(key) for key in ('login', 'name', 'password') }
        

        if qcontext.get('gender'):
            values['gender'] = qcontext.get('gender')

        if qcontext.get('bd_year') and qcontext.get('bd_month') and qcontext.get('bd_date'):
            values['birthday'] = qcontext.get('bd_year') + '-' + qcontext.get('bd_month') + '-' + qcontext.get('bd_date')       
        assert values.values(), "The form was not properly filled in. "                
        assert values.get('password') == qcontext.get('confirm_password'), "Passwords do not match; please retype them."                
        supported_langs = [lang['code'] for lang in http.request.env['res.lang'].sudo().search_read([], ['code'])]                
        if http.request.lang in supported_langs:                        
            values['lang'] = http.request.lang

        # Check good format of e-mail
        if not validate_email(values.get("login", "")):
            qcontext["error"] = _("That does not seem to be an email address.")
            return http.request.render("stem_frontend_theme.stem_homepage", qcontext)
        elif not values.get("email"):
            values["email"] = values.get("login")

        if http.request.env["res.users"].sudo().search([("login", "=", values.get("login"))]):
            qcontext["error"] = _("Một người dùng khác đã được đăng ký sử dụng địa chỉ email này.")
            return http.request.render("stem_frontend_theme.stem_homepage", qcontext)

        # Remove password
        values["password"] = ""

        
        sudo_users = (http.request.env["res.users"]
                      .with_context(create_user=True).sudo())

        try:
            with http.request.cr.savepoint():
                sudo_users.signup(values, qcontext.get("token"))
                sudo_users.reset_password(values.get("login"))
        except Exception as error:
            # Duplicate key or wrong SMTP settings, probably
            _logger.exception(error)
            # Agnostic message for security
            qcontext["error"] = _(
                "Đã xảy ra sự cố, vui lòng thử lại sau hoặc liên hệ với chúng tôi.")
            return http.request.render("stem_frontend_theme.stem_homepage", qcontext)

        qcontext["message"] = _("Kiểm tra email của bạn để kích hoạt tài khoản của bạn!")
        return http.request.render("auth_signup.reset_password", qcontext)