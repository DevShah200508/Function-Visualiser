def handle_error(window, error):
    window.error_label.configure(text=error, image=window.error_icon)

def reset_error_box(window):
    window.error_label.configure(text='', image='')