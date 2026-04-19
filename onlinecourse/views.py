from django.shortcuts import render, get_object_or_404
from .models import Course, Submission, Choice

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    if request.method == "POST":
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

    correct = 0
    total = submission.choices.count()

    for choice in submission.choices.all():
        if choice.is_correct:
            correct += 1

    score = (correct / total) * 100 if total > 0 else 0

    return render(request, "onlinecourse/result.html", {
        "score": score,
        "correct": correct,
        "total": total
    })