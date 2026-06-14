import math
import customtkinter as ctk

class HoverTooltip:
    def __init__(self, canvas):
        self.canvas = canvas
        widget = canvas.get_tk_widget()
        self.widget = widget

        self.label = ctk.CTkLabel(
            widget,
            text="",
            fg_color="#2A2A2A",
            text_color="white",
            corner_radius=6,
            font=("Arial", 11),
            justify="left",
            anchor="w"
        )
        self._visible = False

    def show(self, text, x_px, y_px):
        self.label.configure(text=text)
        self.label.place(x=x_px + 15, y=y_px + 15)
        self.label.lift()
        self._visible = True

    def hide(self):
        if self._visible:
            self.label.place_forget()
            self._visible = False

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

def connect_tooltip(canvas, axes, get_tooltip_fn):
    tooltip = HoverTooltip(canvas)
    widget_height = canvas.get_tk_widget().winfo_height()

    def on_hover(event):
        if event.inaxes not in axes or event.xdata is None:
            tooltip.hide()
            return

        text = get_tooltip_fn(event, event.inaxes)
        if text:
            h = canvas.get_tk_widget().winfo_height()
            tooltip.show(text, event.x, h - event.y)
        else:
            tooltip.hide()

    canvas.mpl_connect("motion_notify_event", on_hover)
    canvas.mpl_connect("figure_leave_event", lambda e: tooltip.hide())
    return tooltip


def find_nearest(event, ax, points, threshold_px=10):
    if not points:
        return None

    best_idx = None
    best_dist = float("inf")

    for i, (px, py) in enumerate(points):
        try:
            sx, sy = ax.transData.transform((px, py))
        except Exception:
            continue

        if not math.isfinite(sx) or not math.isfinite(sy):
            continue

        dist = math.hypot(event.x - sx, event.y - sy)
        if dist < best_dist:
            best_dist = dist
            best_idx = i

    return best_idx if best_dist < threshold_px else None