from django import forms
from django.core.validators import MinLengthValidator
from .models import Question, Tag, Answer
from mdeditor.widgets import MDEditorWidget


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ['title', 'content', 'bounty_amount', 'tags']

        labels = {
            'title': 'Title',
            'content': 'Body',
            'bounty_amount': 'Bounty',
            'tags': 'Tags'
        }

        help_texts = {
            'title': 'Be specific and imagine you’re asking a question to another person.',
            'content': 'The body of your question contains your problem details and results. Minimum 220 characters.',
            'bounty_amount': "Bounty amount if you're interested in rewarding the person answered it.",
            'tags': 'Add up to 5 tags to describe what your question is about. Start typing to see suggestions.'
        }

        widgets = {
            'content': MDEditorWidget,
            'tags': forms.CheckboxSelectMultiple
        }


class AskForm(forms.ModelForm):
    problem_content = forms.CharField(widget=MDEditorWidget, label='What are the details of your problem?',
                                      help_text='Introduce the problem and expand on what you put in the title.' 
                                                'Minimum 20 characters.',
                                      validators=[MinLengthValidator(20,
                                                                     'Requires minimum 20 characters.')]
                                      )

    expected_content = forms.CharField(widget=MDEditorWidget, label='What did you try and what were you expecting?',
                                       help_text='Describe what you tried, what you expected to happen,' 
                                                 'and what actually resulted. Minimum 20 characters.',
                                       validators=[MinLengthValidator(20,
                                                                      'Requires minimum 20 characters.')]
                                       )

    class Meta:
        model = Question
        fields = ['title', 'problem_content', 'expected_content']

        labels = {
            'title': 'Title',
        }

        help_texts = {
            'title': 'Be specific and imagine you’re asking a question to another person.',
        }

    def save(self, commit=False):
        question = super().save(commit=False)
        question.content = self.cleaned_data['problem_content'] + '\n' + self.cleaned_data['expected_content']
        return question


class AnswerUploadForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']

        widgets = {
            'content': MDEditorWidget
        }


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'description']

