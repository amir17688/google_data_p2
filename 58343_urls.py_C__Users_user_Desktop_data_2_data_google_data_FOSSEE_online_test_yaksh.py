from django.conf.urls import patterns, url
from yaksh import views
from django.contrib.auth.views import password_reset, password_reset_confirm,\
        password_reset_done, password_reset_complete, password_change,\
        password_change_done

urlpatterns = [
    url(r'^forgotpassword/$', password_reset, name="password_reset"),
    url(r'^password_reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        password_reset_confirm, name='password_reset_confirm'),
    url(r'^password_reset/mail_sent/$', password_reset_done,
        name='password_reset_done'),
    url(r'^password_reset/complete/$', password_reset_complete,
        name='password_reset_complete'),
    url(r'^changepassword/$', password_change,
        name='password_change'),
    url(r'^password_change/done/$', password_change_done,
        name='password_change_done'),
]
urlpatterns += [
    url(r'^$', views.index),
    url(r'^login/$', views.user_login),
    url(r'^quizzes/$', views.quizlist_user),
    url(r'^results/$', views.results_user),
    url(r'^start/$', views.start),
    url(r'^start/(?P<questionpaper_id>\d+)/$', views.start),
    url(r'^start/(?P<attempt_num>\d+)/(?P<questionpaper_id>\d+)/$', views.start),
    url(r'^quit/(?P<attempt_num>\d+)/(?P<questionpaper_id>\d+)/$', views.quit),
    url(r'^complete/$', views.complete),
    url(r'^complete/(?P<attempt_num>\d+)/(?P<questionpaper_id>\d+)/$',\
            views.complete),
    url(r'^register/$', views.user_register),
    url(r'^(?P<q_id>\d+)/check/$', views.check),
    url(r'^(?P<q_id>\d+)/check/(?P<attempt_num>\d+)/(?P<questionpaper_id>\d+)/$',\
            views.check),
    url(r'^(?P<q_id>\d+)/skip/(?P<attempt_num>\d+)/(?P<questionpaper_id>\d+)/$',
        views.skip),
    url(r'^(?P<q_id>\d+)/skip/(?P<next_q>\d+)/(?P<attempt_num>\d+)/(?P<questionpaper_id>\d+)/$',
        views.skip),
    url(r'^enroll_request/(?P<course_id>\d+)/$', views.enroll_request),
    url(r'^self_enroll/(?P<course_id>\d+)/$', views.self_enroll),
    url(r'^manage/$', views.prof_manage),
    url(r'^manage/addquestion/$', views.add_question),
    url(r'^manage/addquestion/(?P<question_id>\d+)/$', views.add_question),
    url(r'^manage/addquiz/$', views.add_quiz),
    url(r'^manage/addquiz/(?P<quiz_id>\d+)/$', views.add_quiz),
    url(r'^manage/gradeuser/$', views.show_all_users),
    url(r'^manage/gradeuser/(?P<username>.*)/(?P<questionpaper_id>\d+)/$',
        views.grade_user),
    url(r'^manage/gradeuser/(?P<username>.*)/$', views.grade_user),
    url(r'^manage/questions/$', views.show_all_questions),
    url(r'^manage/monitor/$', views.monitor),
    url(r'^manage/showquestionpapers/$', views.show_all_questionpapers),
    url(r'^manage/showquestionpapers/(?P<questionpaper_id>\d+)/$',\
                                                    views.show_all_questionpapers),
    url(r'^manage/monitor/(?P<questionpaper_id>\d+)/$', views.monitor),
    url(r'^manage/user_data/(?P<username>.*)/(?P<questionpaper_id>\d+)/$',
        views.user_data),
    url(r'^manage/user_data/(?P<username>.*)/$', views.user_data),
    url(r'^manage/designquestionpaper/$', views.design_questionpaper),
    url(r'^manage/designquestionpaper/(?P<questionpaper_id>\d+)/$',\
                                                        views.design_questionpaper),
    url(r'^manage/statistics/question/(?P<questionpaper_id>\d+)/$',
        views.show_statistics),
    url(r'^manage/statistics/question/(?P<questionpaper_id>\d+)/(?P<attempt_number>\d+)/$',
        views.show_statistics),
    url(r'^manage/monitor/download_csv/(?P<questionpaper_id>\d+)/$',
        views.download_csv),
    url(r'manage/courses/$', views.courses),
    url(r'manage/add_course/$', views.add_course),
    url(r'manage/course_detail/(?P<course_id>\d+)/$', views.course_detail),
    url(r'manage/enroll/(?P<course_id>\d+)/(?P<user_id>\d+)/$', views.enroll),
    url(r'manage/enroll/rejected/(?P<course_id>\d+)/(?P<user_id>\d+)/$',
        views.enroll, {'was_rejected': True}),
    url(r'manage/reject/(?P<course_id>\d+)/(?P<user_id>\d+)/$', views.reject),
    url(r'manage/enrolled/reject/(?P<course_id>\d+)/(?P<user_id>\d+)/$',
        views.reject, {'was_enrolled': True}),
    url(r'manage/toggle_status/(?P<course_id>\d+)/$', views.toggle_course_status),
    url(r'^ajax/questionpaper/(?P<query>.+)/$', views.ajax_questionpaper),
    url(r'^ajax/questions/filter/$', views.ajax_questions_filter),
    url(r'^editprofile/$', views.edit_profile),
    url(r'^viewprofile/$', views.view_profile),
    url(r'^manage/enroll/(?P<course_id>\d+)/$', views.enroll),
    url(r'manage/enroll/rejected/(?P<course_id>\d+)/$',
        views.enroll, {'was_rejected': True}),
    url(r'manage/enrolled/reject/(?P<course_id>\d+)/$',
        views.reject, {'was_enrolled': True})
]
