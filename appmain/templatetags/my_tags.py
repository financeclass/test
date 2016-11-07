# coding:utf-8
from django import template

register = template.Library()
def mytag_link_split(value):
    return ('.').join(value.replace('http://',"").
    	replace('https://',"").replace('www.',"").replace('/',"").replace('?',"").split('.')[:2])
register.filter('mytag_link_split',mytag_link_split)