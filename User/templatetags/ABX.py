from django import template
from User.models import Answer

register = template.Library()


@register.simple_tag
def is_ABX_answer(user, subjective_test, question, value):
    try:
        answer = Answer.objects.get(
            user=user,
            subjective_test=subjective_test,
            question=question,
            sample_id__exact=0,
        )
    except:
        return False
    return answer.answer == int(value)
