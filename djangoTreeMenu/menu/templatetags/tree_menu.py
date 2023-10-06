from django import template
from django.db import connection
from django.core.exceptions import ObjectDoesNotExist

from menu.models import Item


register = template.Library()


@register.inclusion_tag('tree_menu.html', takes_context=True)
def draw_menu(context, menu):
    items = Item.objects.filter(menu__name=menu)
    items_values = items.values()
    primary_item = list(filter(lambda x: x.get('parent_id') is None, items_values))
    selected_item_slug = context['request'].GET.get(menu)
    if selected_item_slug:
        selected_item = list(filter(lambda x: x.get('slug') == selected_item_slug, items_values))[0]
        selected_item_slug_list = get_selected_item_slug_list(
            selected_item, primary_item, selected_item_slug, items_values)

        for item in primary_item:
            if item['slug'] in selected_item_slug_list:
                item['child_items'] = get_child_items(items_values, item['slug'], selected_item_slug_list)
    else:
        pass
    result_dict = {
        'items': primary_item,
        'menu': menu,
        'other_querystring': get_querystring(context, menu)
    }
    return result_dict


def get_querystring(context, menu):
    querystring_args = []
    for key in context['request'].GET:
        if key != menu:
            querystring_args.append(key + '=' + context['request'].GET[key])
    querystring = ('&').join(querystring_args)
    return querystring


def get_child_items(items_values, current_item_slug, selected_item_slug_list):
    current_item_id = list(filter(lambda x: x.get('slug') == current_item_slug, items_values))[0].get('id')
    item_list = list(filter(lambda x: x.get('parent_id') == current_item_id, items_values))
    for item in item_list:
        if item['slug'] in selected_item_slug_list:
            item['child_items'] = get_child_items(items_values, item['slug'], selected_item_slug_list)
    return item_list


def get_selected_item_slug_list(parent, primary_item, selected_item_slug, items_values):
    selected_item_slug_list = []
    parent_id = parent['id']
    while parent_id:
        selected_item_slug_list.append(parent['slug'])
        parent_id = parent['parent_id']
        if parent_id:
            parent = list(filter(lambda x: x.get('id') == parent_id, items_values))[0]
    if not selected_item_slug_list:
        for item in primary_item:
            if item['slug'] == selected_item_slug:
                selected_item_slug_list.append(selected_item_slug)
    return selected_item_slug_list
