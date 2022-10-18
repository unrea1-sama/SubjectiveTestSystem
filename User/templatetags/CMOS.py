from django import template
from User.models import Answer

register = template.Library()


@register.simple_tag
def is_CMOS_answer(user, subjective_test, question, sample, value):
    try:
        answer = Answer.objects.get(
            user=user,
            subjective_test=subjective_test,
            question=question,
            sample_id__exact=sample.id,
        )
    except:
        return False
    return answer.answer == int(value)
