from django import template
from django.urls import resolve, Resolver404
from ..models import MenuItem

register = template.Library()


@register.inclusion_tag('tree_menu/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_path = request.path_info

    # Get all menu items in one query
    menu_items = MenuItem.objects.filter(menu_name=menu_name).select_related('parent')

    # Build the menu tree
    menu_tree = []
    items_dict = {}

    # Create a dictionary of all items
    for item in menu_items.order_by('order'):
        items_dict[item.id] = {
            'item': item,
            'children': [],
            'is_active': item.is_active(current_path),
        }

    # Build the tree structure
    for item_id, item_data in items_dict.items():
        item = item_data['item']
        if item.parent is None:
            menu_tree.append(item_data)
        else:
            parent_id = item.parent.id
            if parent_id in items_dict:
                items_dict[parent_id]['children'].append(item_data)

    # Mark active ancestors
    for item_id, item_data in items_dict.items():
        if item_data['is_active']:
            parent = item_data['item'].parent
            while parent:
                if parent.id in items_dict:
                    items_dict[parent.id]['is_active'] = True
                    parent = parent.parent
                else:
                    break

    return {
        'menu_tree': menu_tree,
        'current_path': current_path,
    }
