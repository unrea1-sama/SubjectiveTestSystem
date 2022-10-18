import random
from django import template
register = template.Library()


@register.filter
def shuffle(samples):
    """
    随机排列samples。其中不需要打分的样本固定在前面，需要打分的样本乱序放在后面
    """
    original_list = list(samples)
    head = [] # 存储不需要打分的样本
    rand_list = [] # 存储需要打分的样本
    for item in original_list:
        if item.score:
            rand_list.append(item)
        else:
            head.append(item)
    random.shuffle(rand_list)
    return head+rand_list