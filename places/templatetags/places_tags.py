from django import template

register = template.Library()


@register.filter
def voted_by(place, username):
    return place.voted_by(username)
