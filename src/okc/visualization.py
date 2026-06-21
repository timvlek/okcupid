def change_width(ax, new_value) :
    for patch in ax.patches :
        current_width = patch.get_height()
        diff = current_width - new_value
        patch.set_height(new_value)
        patch.set_y(patch.get_y() + diff * .5)