from django import template

register = template.Library()


def in_category_count(things, category):
    return things.filter(is_seen=category).count()


register.filter('in_category_count', in_category_count)
