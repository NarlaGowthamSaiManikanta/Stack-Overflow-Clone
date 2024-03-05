from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import AskForm, ReviewForm, TagForm, AnswerUploadForm
from .models import Question, Answer, Visit, Tag


# Create your views here.
@login_required(login_url='/user/login/')
def comment_question(request, question_id):
    question = Question.objects.get(pk=question_id)
    comment = request.POST.get('comment')
    if comment is not None and comment != '' and request.user.reputation > 15:
        question.questioncomments_set.create(question=question, user=request.user, comment=request.POST.get('comment'))
    return redirect('questions:question_view', question_id=question_id)


@login_required(login_url='/user/login/')
def comment_answer(request, answer_id):
    answer = Answer.objects.get(pk=answer_id)
    comment = request.POST.get('comment')
    if comment is not None and comment != '' and request.user.reputation > 15:
        answer.answercomments_set.create(answer=answer, user=request.user, comment=request.POST.get('comment'))
    return redirect('questions:question_view', question_id=answer.question.id)


def question_view(request, question_id):
    question = Question.objects.get(pk=question_id)

    if request.user.is_anonymous:
        return render(request, 'questions/question-view.html', {
            'question': question,
            'base_html': 'user/base-no-login.html'
        })

    try:
        Visit.objects.get(question=question, user=request.user)
    except Visit.DoesNotExist:
        Visit.objects.create(question=question, user=request.user)

    try:
        answer = Answer.objects.get(question=question, user=request.user)
    except Answer.DoesNotExist:
        answer = None

    if request.method == 'POST':
        form = AnswerUploadForm(request.POST)
        if form.is_valid():
            if answer is None:
                answer = form.save(commit=False)
                answer.question = question
                answer.user = request.user
                answer.save()
            else:
                answer.content = request.POST['content']
                answer.save()

            form = AnswerUploadForm(instance=answer)
            already_answered = True
        else:
            if answer is not None:
                already_answered = True
            else:
                already_answered = False

        return render(request, 'questions/question-view.html', {
            'question': question,
            'form': form,
            'already_answered': already_answered,
            'base_html': 'user/base.html'
        })

    else:
        if answer is not None:
            already_answered = True
            form = AnswerUploadForm(instance=answer)
        else:
            already_answered = False
            form = AnswerUploadForm()

        return render(request, 'questions/question-view.html', {
            'question': question,
            'form': form,
            'already_answered': already_answered,
            'base_html': 'user/base.html'
        })


@login_required(login_url='/user/login/')
def ask(request):
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            question = review_form.save(commit=False)
            question.user = request.user
            question.save()
            review_form.save_m2m()

            return HttpResponse('Question Asked')
        else:
            if request.POST.get('content') is not None:
                review_form = ReviewForm(request.POST)
                return render(request, 'questions/ask.html', {'review_form': review_form})

            ask_form = AskForm(request.POST)
            if ask_form.is_valid():
                question = ask_form.save(commit=False)
                review_form = ReviewForm(instance=question)
                return render(request, 'questions/ask.html', {'review_form': review_form})
            else:
                return render(request, 'questions/ask.html', {'ask_form': ask_form})
    else:
        ask_form = AskForm(initial={})
        return render(request, 'questions/ask.html', {
            'ask_form': ask_form
        })


@login_required(login_url='/user/login/')
def accept_answer(request, answer_id):
    answer = Answer.objects.get(pk=answer_id)
    if request.user == answer.question.user:
        if answer.accepted_answer_for is not None and answer.question.accepted_answer == answer:
            answer.accepted_answer_for = None
            answer.user.reputation -= (10 + answer.question.bounty_amount)
            answer.user.save()
            answer.save()
        else:
            answer.accepted_answer_for = answer.question
            answer.user.reputation += (10 + answer.question.bounty_amount)
            answer.user.save()
            answer.save()
    return redirect('questions:question_view', question_id=answer.question.id)


@login_required(login_url='/user/login/')
def question_save(request, question_id):
    question = Question.objects.get(pk=question_id)
    if question.saved_by.filter(id=request.user.id):
        question.saved_by.remove(request.user)
    else:
        question.saved_by.add(request.user)
    return redirect('questions:question_view', question_id=question.id)


@login_required(login_url='/user/login/')
def answer_save(request, answer_id):
    answer = Answer.objects.get(pk=answer_id)
    if answer.saved_by.filter(id=request.user.id):
        answer.saved_by.remove(request.user)
    else:
        answer.saved_by.add(request.user)
    return redirect('questions:question_view', question_id=answer.question.id)


@login_required(login_url='/user/login/')
def vote_question(request, question_id, option):
    question = Question.objects.get(pk=question_id)
    if question.up_votes.filter(id=request.user.id):
        question.up_votes.remove(request.user)

    if question.down_votes.filter(id=request.user.id):
        question.down_votes.remove(request.user)

    if option.lower() == 'upvote':
        question.up_votes.add(request.user)
    if option.lower() == 'downvote':
        question.down_votes.add(request.user)

    return redirect('questions:question_view', question_id=question_id)


@login_required(login_url='/user/login/')
def vote_answer(request, answer_id, option):
    answer = Answer.objects.get(pk=answer_id)
    if answer.up_votes.filter(id=request.user.id):
        answer.up_votes.remove(request.user)

    if answer.down_votes.filter(id=request.user.id):
        answer.down_votes.remove(request.user)

    if option.lower() == 'upvote':
        answer.up_votes.add(request.user)
    if option.lower() == 'downvote':
        answer.down_votes.add(request.user)

    return redirect('questions:question_view', question_id=answer.question.id)


def tagged_questions(request, tag):
    if request.user.is_authenticated:
        base_html = 'questions/tagged.html'
    questions = Question.objects.filter(tags__name=tag)
    get_object_or_404(questions)
    return render(request, 'questions/tagged.html', {
        'base_html': 'user/base.html',
        'questions': questions,
        'tag': Tag.objects.get(name=tag),
    })


def tag_upload(request):
    if request.method == 'POST':
        tag_form = TagForm(request.POST)
        if tag_form.is_valid():
            tag_form.save()
        else:
            return render(request, 'questions/ask.html', {'ask_form': tag_form})
    return render(request, 'questions/ask.html', {'ask_form': TagForm()})
