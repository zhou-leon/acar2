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

    dark_bg = "linear-gradient(135deg, #232526 0%, #414345 100%)"
    dark_fg = "#f8fafd"
    accent = "rgba(34, 40, 49, 0.85)"
    selected_bg = "#3aafa9"
    border_color = "#222831"
    card_bg = "rgba(44, 62, 80, 0.7)"
    card_shadow = "0 4px 24px rgba(0,0,0,0.18)"
    glass = "rgba(255,255,255,0.08)"

    return html.div({"style": {
        "display": "flex",
        "flexDirection": "column",
        "minHeight": "100vh",
        "background": dark_bg,
        "color": dark_fg,
        "fontFamily": "Inter, Roboto, Segoe UI, Arial, sans-serif"
    }},
        # Sticky header
        html.div({"style": {
            "width": "100%",
            "padding": "1.2rem 2.5rem 1.2rem 2.5rem",
            "background": glass,
            "backdropFilter": "blur(8px)",
            "borderBottom": f"1px solid {border_color}",
            "position": "sticky",
            "top": "0",
            "zIndex": 10,
            "display": "flex",
            "alignItems": "center",
            "boxShadow": "0 2px 12px rgba(0,0,0,0.10)"
        }},
            html.span({"style": {"fontWeight": "700", "fontSize": "2.1rem", "letterSpacing": "0.04em", "color": selected_bg}}, "Car Maintenance Dashboard"),
        ),
        html.div({"style": {
            "display": "flex",
            "flex": "1 1 auto",
            "height": "100%"
        }},
            html.div({"style": {
                "width": "30%",
                "borderRight": f"2px solid {border_color}",
                "padding": "2rem 1.5rem 1.5rem 2rem",
                "background": glass,
                "backdropFilter": "blur(14px)",
                "WebkitBackdropFilter": "blur(14px)",
                "boxShadow": "0 8px 32px 0 rgba(31, 38, 135, 0.18)",
                "display": "flex",
                "flexDirection": "column",
                "height": "100%"
            }},
                html.button({
                    "style": {
                        "marginBottom": "2rem",
                        "padding": "1rem 2.2rem",
                        "background": selected_bg,
                        "color": dark_fg,
                        "border": f"1px solid {border_color}",
                        "borderRadius": "12px",
                        "fontSize": "1.15rem",
                        "cursor": "pointer",
                        "fontFamily": "inherit",
                        "fontWeight": "700",
                        "boxShadow": "0 6px 24px rgba(58,175,169,0.15)",
                        "letterSpacing": "0.03em",
                        "transition": "background 0.2s, box-shadow 0.2s"
                    },
                    "on_mouse_over": lambda e: e['target'].update({"background": "#2b7a78"}),
                    "on_mouse_out": lambda e: e['target'].update({"background": selected_bg}),
                    "on_click": lambda e: selected_car and fetch_event_report(selected_car)
                }, "Event Report"),
                html.h2({"style": {"color": dark_fg, "marginBottom": "2rem", "fontWeight": "600", "fontSize": "2rem", "letterSpacing": "0.02em"}}, "Vehicles"),
                html.form({"style": {"marginBottom": "2rem"}},
                    [
                        html.label({"key": name, "style": {
                            "display": "flex",
                            "alignItems": "center",
                            "marginBottom": "1rem",
                            "background": card_bg,
                            "boxShadow": card_shadow,
                            "borderRadius": "12px",
                            "padding": "1rem 1.2rem",
                            "cursor": "pointer",
                            "transition": "background 0.2s, box-shadow 0.2s",
                            "border": selected_car == name and f"2px solid {selected_bg}" or f"1px solid {border_color}",
                            "boxShadow": selected_car == name and "0 6px 24px rgba(58,175,169,0.15)" or card_shadow,
                            "background": selected_car == name and "rgba(58,175,169,0.18)" or card_bg
                        }},
                            html.input({
                                "type": "radio",
                                "name": "vehicle",
                                "value": name,
                                "checked": selected_car == name,
                                "on_change": lambda e, n=name: set_selected_car(n),
                                "style": {"marginRight": "0.75rem", "accentColor": selected_bg}
                            }),
                            html.span({"style": {"fontWeight": "500", "fontSize": "1.1rem"}}, name)
                        )
                        for name in car_list
                    ]
                )
            ),
            html.div({"style": {
                "width": "70%",
                "padding": "2.5rem 3rem 2.5rem 2.5rem",
                "background": dark_bg,
                "display": "flex",
                "flexDirection": "column",
                "alignItems": "flex-start"
            }},
                event_report and html.div({"style": {"width": "100%", "maxWidth": "900px", "marginTop": "1rem"}}, [
                    # Split report by separator and render each event as a card
                    *[
                        (lambda cleaned: cleaned and html.div({"style": {
                            "background": card_bg,
                            "color": dark_fg,
                            "padding": "1.5rem 2rem 1.2rem 2rem",
                            "borderRadius": "12px",
                            "marginBottom": "1.5rem",
                            "boxShadow": card_shadow,
                            "borderLeft": f"6px solid {selected_bg}",
                            "fontSize": "1.08rem",
                            "whiteSpace": "pre-wrap",
                            "transition": "box-shadow 0.2s",
                            "overflow": "hidden"
                        }}, cleaned) or None)
                        (
                            "\n".join([
                                line for line in event.strip().splitlines()
                                if line.strip() and not line.strip().startswith("==")
                            ]).rstrip()
                        )
                        for event in event_report.split("========") if event.strip()
                    ]
                ])
            )
        )
    )

if __name__ == "__main__":
    run(Dashboard)
