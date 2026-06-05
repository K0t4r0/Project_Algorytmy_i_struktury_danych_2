def on_scroll(event, ax, canvas):
    if event.xdata is None or event.ydata is None:
        return

    x_min, x_max = ax.get_xlim()
    y_min, y_max = ax.get_ylim()

    scale = 0.9 if event.button == "up" else 1.1

    ax.set_xlim(
        event.xdata + (x_min - event.xdata) * scale,
        event.xdata + (x_max - event.xdata) * scale
    )
    ax.set_ylim(
        event.ydata + (y_min - event.ydata) * scale,
        event.ydata + (y_max - event.ydata) * scale
    )

    canvas.draw_idle()


def on_press(event, state):
    if event.inaxes is None:
        return

    state["drag_start"] = (
        event.x,
        event.y,
        event.inaxes.get_xlim(),
        event.inaxes.get_ylim(),
        event.inaxes
    )


def on_motion(event, state, canvas):
    if state["drag_start"] is None:
        return

    x0_px, y0_px, xlim, ylim, ax = state["drag_start"]

    dx_px = event.x - x0_px
    dy_px = event.y - y0_px

    ax_width_px  = ax.get_window_extent().width
    ax_height_px = ax.get_window_extent().height

    x_range = xlim[1] - xlim[0]
    y_range = ylim[1] - ylim[0]

    dx = dx_px * x_range / ax_width_px
    dy = dy_px * y_range / ax_height_px

    ax.set_xlim(xlim[0] - dx, xlim[1] - dx)
    ax.set_ylim(ylim[0] - dy, ylim[1] - dy) 

    canvas.draw_idle()


def on_release(event, state):
    state["drag_start"] = None

def get_state_for_event(event, ax_state_map: dict):
    return ax_state_map.get(event.inaxes, None)


def on_motion_multi(event, states: list, canvas):
    for state in states:
        if state["drag_start"] is not None:
            on_motion(event, state, canvas)
            return


def connect_navigation(canvas, ax_state_map: dict):
    states = list(ax_state_map.values())

    canvas.mpl_connect("scroll_event",
        lambda e: on_scroll(e, e.inaxes, canvas) if e.inaxes else None)

    canvas.mpl_connect("button_press_event",
        lambda e: on_press(e, get_state_for_event(e, ax_state_map))
        if get_state_for_event(e, ax_state_map) is not None else None)

    canvas.mpl_connect("motion_notify_event",
        lambda e: on_motion_multi(e, states, canvas))

    canvas.mpl_connect("button_release_event",
        lambda e: [on_release(e, s) for s in states])