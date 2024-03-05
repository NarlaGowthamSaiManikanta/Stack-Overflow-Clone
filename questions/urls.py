from django.urls import path
from . import views


app_name = 'questions'
urlpatterns = [
    path('ask/', views.ask, name='ask'),
    path('tag/', views.tag_upload, name='tag'),
    path('<int:question_id>/', views.question_view, name='question_view'),
    path('comment/question/<int:question_id>/', views.comment_question, name='comment_question'),
    path('comment/answer/<int:answer_id>/', views.comment_answer, name='comment_answer'),
    path('accept_answers/<int:answer_id>/', views.accept_answer, name='accept_answer'),
    path('save/question/<int:question_id>/', views.question_save, name='question_save'),
    path('save/answer/<int:answer_id>/', views.answer_save, name='answer_save'),
    path('vote/question/<int:question_id>/<str:option>', views.vote_question, name='vote_question'),
    path('vote/answer/<int:answer_id>/<str:option>', views.vote_answer, name='vote_answer')
]
