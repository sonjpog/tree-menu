from django import template
from django.urls import resolve, Resolver404
from menu.models import MenuItem

register = template.Library()


@register.inclusion_tag('menu/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_path = request.path_info

    # Получаем все пункты меню одним запросом
    menu_items = MenuItem.objects.filter(menu_name=menu_name).select_related('parent')

    # Строим дерево меню
    menu_tree = []
    nodes = {item.id: {'item': item, 'children': []} for item in menu_items}

    for item in menu_items:
        if item.parent_id:
            nodes[item.parent_id]['children'].append(nodes[item.id])
        else:
            menu_tree.append(nodes[item.id])

    # Находим активный пункт
    active_items = []
    for item in menu_items:
        if item.is_active(current_path):
            active_items.append(item)

    # Определяем, какие ветки нужно раскрыть
    expanded_items = set()
    for item in active_items:
        # Добавляем всех родителей активного пункта
        parent = item.parent
        while parent:
            expanded_items.add(parent.id)
            parent = parent.parent

    return {
        'menu_tree': menu_tree,
        'current_path': current_path,
        'expanded_items': expanded_items,
        'active_items': [item.id for item in active_items],
    }
