import markdown2


with open('templates/aboutMe.md', 'r') as f:
    text_head = '''{% extends 'base.html' %}

{% block content %}
'''
    text = f.read()
    text_tail = '''{% endblock %}'''
    text = markdown2.markdown(text)
    text = text_head + text + text_tail

with open('templates/me.html', 'w') as f:
    f.write(text)
