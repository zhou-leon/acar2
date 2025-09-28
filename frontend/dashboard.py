import reactpy
from reactpy import html, component, use_state, use_effect, run
import requests

API_BASE = "http://127.0.0.1:5000"

@component
def Dashboard():
    car_list, set_car_list = use_state([])
    selected_car, set_selected_car = use_state("")
    event_report, set_event_report = use_state("")

    def fetch_car_list():
        try:
            resp = requests.get(f"{API_BASE}/car-list")
            data = resp.json()
            set_car_list(data.get("cars", []))
        except Exception:
            set_car_list([])

    def fetch_event_report(car_name):
        try:
            api_url = f"{API_BASE}/event-report?name={requests.utils.quote(car_name)}"
            resp = requests.get(api_url)
            data = resp.json()
            set_event_report(data.get("report", ""))
        except Exception:
            set_event_report("")

    use_effect(fetch_car_list, [])

    dark_bg = "#181818"
    dark_fg = "#f5f5f5"
    accent = "#222"
    selected_bg = "#333"
    border_color = "#444"

    return html.div({"style": {
        "display": "flex",
        "height": "100vh",
        "background": dark_bg,
        "color": dark_fg,
        "fontFamily": "Inter, Roboto, Segoe UI, Arial, sans-serif"
    }},
        html.div({"style": {"width": "30%", "borderRight": f"2px solid {border_color}", "padding": "1rem", "background": accent, "display": "flex", "flexDirection": "column", "height": "100vh"}},
            html.h2({"style": {"color": dark_fg}}, "Vehicles"),
            html.form({"style": {"marginBottom": "1rem"}},
                [
                    html.label({"key": name, "style": {"display": "block", "marginBottom": "0.5rem", "color": dark_fg}},
                        html.input({
                            "type": "radio",
                            "name": "vehicle",
                            "value": name,
                            "checked": selected_car == name,
                            "on_change": lambda e, n=name: set_selected_car(n),
                            "style": {"marginRight": "0.5rem"}
                        }),
                        name
                    )
                    for name in car_list
                ]
            ),
            html.button({
                "style": {
                    "marginTop": "2rem",
                    "padding": "0.75rem 1.5rem",
                    "background": selected_bg,
                    "color": dark_fg,
                    "border": f"1px solid {border_color}",
                    "borderRadius": "6px",
                    "fontSize": "1rem",
                    "cursor": "pointer",
                    "fontFamily": "inherit"
                },
                "on_click": lambda e: selected_car and fetch_event_report(selected_car)
            }, "Event Report")
        ),
        html.div({"style": {"width": "70%", "padding": "1rem", "background": dark_bg}},
            event_report and html.pre({"style": {"background": accent, "color": dark_fg, "padding": "1rem", "borderRadius": "6px", "marginTop": "1rem", "whiteSpace": "pre-wrap", "fontSize": "0.95rem"}}, event_report)
        )
    )

if __name__ == "__main__":
    run(Dashboard)
