from django.shortcuts import render, get_object_or_404
from .models import Course, Submission, Choice, Question

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    selected_choices = request.POST.getlist("choices")

    submission = Submission.objects.create(
        user=request.user,
        course=course
    )

    for choice_id in selected_choices:
        choice = Choice.objects.get(id=choice_id)
        submission.choices.add(choice)

    return show_exam_result(request, submission.id)

def show_exam_result(request, submission_id):
    submission = Submission.objects.get(id=submission_id)
    choices = submission.choices.all()

    selected_ids = [choice.id for choice in choices]

    questions = Question.objects.filter(choice__in=choices).distinct()

    total_score = 0
    possible_score = questions.count()

    for question in questions:
        total_score += question.is_get_score(selected_ids)

    return render(request, 'onlinecourse/result.html', {
        'grade': total_score,
        'possible': possible_score,
        'questions': questions
    })