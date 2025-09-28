import reactpy
from reactpy import html, component, use_state, use_effect, run
import requests
import datetime

API_BASE = "http://127.0.0.1:5000"

@component
def Dashboard():
    import re
    def extract_tags(report):
        tags = set()
        # Find all lines with 'tags:' and extract comma-separated values
        fields = ["tags:", "notes:"]
        for line in report.splitlines():
            for field in fields:
                m = re.match(fr"{field}\s*(.*)", line, re.IGNORECASE)
                if m:
                    tags.update([t.strip() for t in m.group(1).split(",") if t.strip()])
        return list(tags)

    def amazon_url(tag):
        return f"https://www.amazon.com/s?k={requests.utils.quote(tag)}"

    # product_tags will be calculated after event_report is defined
    car_list, set_car_list = use_state([])
    selected_car, set_selected_car = use_state("")
    event_report, set_event_report = use_state("")
    car_info, set_car_info = use_state(None)
    show_event_form, set_show_event_form = use_state(False)
    today_str = datetime.date.today().isoformat()
    event_form_data, set_event_form_data = use_state({"date": today_str})
    event_submit_status, set_event_submit_status = use_state("")

    subtype_keys = [
        "A/C System", "Accident", "Air Filter", "Alternator", "Battery", "Belts", "Body/Chassis",
        "Brake Fluid", "Brakes, Front", "Brakes, Rear", "Cabin Air Filter", "Car Wash",
        "Clutch Hydraulic Fluid", "Clutch Hydraulic System", "Cooling System", "Diesel Exhaust Fluid",
        "Differential Fluid", "Doors", "Engine Antifreeze", "Engine Oil", "Exhaust System", "Fine",
        "Fuel Filter", "Fuel Lines & Pipes", "Fuel Pump", "Fuel System", "Glass/Mirrors",
        "Heating System", "Horns", "Induction", "Inspection", "Insurance", "Lights",
        "Lubricate Chain", "MOT", "New Tires", "Oil Filter", "Parking", "Payment",
        "Power Steering Fluid", "Radiator", "Registration", "Rust Module", "Safety Devices",
        "Spark Plugs", "Steering System", "Suspension System", "Tax", "Timing Belt", "Tire A",
        "Tire B", "Tire C", "Tire D", "Tire Pressure", "Tire Rotation", "Tires", "Toll", "Tow",
        "Transmission Fluid", "Water Pump", "Wheel Alignment", "Windshield Washer Fluid",
        "Windshield Wipers"
    ]

    def handle_event_form_change(field, value):
        if field == "subtypes":
            subtypes = event_form_data.get("subtypes", {})
            subtypes[value[0]] = value[1]
            set_event_form_data({**event_form_data, "subtypes": subtypes})
        else:
            set_event_form_data({**event_form_data, field: value})

    def submit_event_form():
        payload = {**event_form_data, "car-name": selected_car}
        # Ensure all fields are present
        for f in [
            "type", "date", "notes", "odometer-reading", "payment-type", "tags", "total-cost",
            "place-name", "place-full-address", "place-street", "place-city", "place-state",
            "place-country", "place-postal-code", "place-google-places-id", "place-longitude",
            "place-latitude", "device-longitude", "device-latitude", "subtypes"
        ]:
            if f not in payload:
                payload[f] = "" if f != "subtypes" else {k: False for k in subtype_keys}
        try:
            resp = requests.post(f"{API_BASE}/add-event", json=payload)
            if resp.status_code == 200:
                set_event_submit_status("Event added successfully!")
                set_show_event_form(False)
                set_event_form_data({})
            else:
                set_event_submit_status(f"Error: {resp.json().get('error', 'Unknown error')}")
        except Exception as e:
            set_event_submit_status(f"Error: {str(e)}")

    def fetch_car_info(car_name):
        try:
            api_url = f"{API_BASE}/car-info?name={requests.utils.quote(car_name)}"
            resp = requests.get(api_url)
            data = resp.json()
            set_car_info(data.get("info", {}))
        except Exception:
            set_car_info("")

    def fetch_car_list():
        try:
            resp = requests.get(f"{API_BASE}/car-list")
            data = resp.json()
            cars = data.get("cars", [])
            set_car_list(cars)
            if cars:
                set_selected_car(cars[0])
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

    product_tags = extract_tags(event_report) if 'event_report' in locals() and event_report else []
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
                html.div({"style": {"display": "flex", "flexDirection": "column", "gap": "1rem", "marginBottom": "2rem"}}, [
                    html.button({
                        "style": {
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
                        "on_click": lambda e: set_show_event_form(True)
                    }, "Add Event"),
                    html.button({
                        "style": {
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
                        "on_click": lambda e: (set_event_report("") or (selected_car and fetch_car_info(selected_car)))
                    }, "Information"),
                    html.button({
                        "style": {
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
                        "on_click": lambda e: (set_car_info(None) or (selected_car and fetch_event_report(selected_car)))
                    }, "Event Report")
                ]),
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
                ),
                product_tags and html.div({"style": {"marginTop": "2rem", "marginBottom": "2rem"}}, [
                    html.h4({"style": {"color": selected_bg, "fontWeight": "600", "marginBottom": "0.7rem"}}, "Related Products (Amazon):"),
                    html.ul({"style": {"listStyle": "none", "padding": 0, "margin": 0}}, [
                        html.li({"style": {"marginBottom": "0.5rem"}},
                            html.a({
                                "href": amazon_url(tag),
                                "target": "_blank",
                                "style": {"color": selected_bg, "textDecoration": "underline", "fontWeight": "500"}
                            }, tag)
                        ) for tag in product_tags
                    ])
                ])
            ),
            html.div({"style": {
                "width": "70%",
                "padding": "2.5rem 3rem 2.5rem 2.5rem",
                "background": dark_bg,
                "display": "flex",
                "flexDirection": "column",
                "alignItems": "flex-start"
            }},
                html.div({"style": {"width": "100%", "maxWidth": "900px", "marginTop": "1rem"}},
                    html.form({"style": {
                        "background": card_bg,
                        "color": dark_fg,
                        "padding": "2rem 2.5rem 2rem 2.5rem",
                        "borderRadius": "14px",
                        "marginTop": "1rem",
                        "boxShadow": card_shadow,
                        "width": "100%",
                        "maxWidth": "900px",
                        "border": f"1.5px solid {selected_bg}",
                        "display": "none" if not show_event_form else "flex",
                        "flexDirection": "column",
                        "gap": "1.2rem"
                    }}, [
                        html.div({"style": {"display": "flex", "gap": "1rem", "marginBottom": "1.5rem"}}, [
                            html.button({
                                "type": "button",
                                "style": {
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
                                "on_click": lambda e: submit_event_form()
                            }, "Submit"),
                            html.button({
                                "type": "button",
                                "style": {
                                    "padding": "1rem 2.2rem",
                                    "background": border_color,
                                    "color": dark_fg,
                                    "border": f"1px solid {selected_bg}",
                                    "borderRadius": "12px",
                                    "fontSize": "1.15rem",
                                    "cursor": "pointer",
                                    "fontFamily": "inherit",
                                    "fontWeight": "700",
                                    "boxShadow": "0 6px 24px rgba(58,175,169,0.10)",
                                    "letterSpacing": "0.03em",
                                    "transition": "background 0.2s, box-shadow 0.2s"
                                },
                                "on_click": lambda e: set_show_event_form(False)
                            }, "Cancel")
                        ]),
                        # ...existing code...
                        html.h3({"style": {"marginBottom": "1.2rem", "fontWeight": "600", "fontSize": "1.3rem", "color": selected_bg}}, "Add Event"),
                        # ...existing code...
                        html.h3({"style": {"marginBottom": "1.2rem", "fontWeight": "600", "fontSize": "1.3rem", "color": selected_bg}}, "Add Event"),
                        *[
                            html.div({"style": {"display": "flex", "flexDirection": "column", "marginBottom": "0.7rem"}}, [
                                html.label({"style": {"fontWeight": "600", "marginBottom": "0.3rem"}}, f),
                                html.input({
                                    "type": "text" if f != "date" else "date",
                                    "value": event_form_data.get(f, today_str if f == "date" else ""),
                                    "on_change": lambda e, field=f: handle_event_form_change(field, e['target']['value']),
                                    "style": {"padding": "0.7rem", "borderRadius": "8px", "border": f"1px solid {selected_bg}", "fontSize": "1rem", "background": glass, "color": dark_fg}
                                })
                            ])
                            for f in [
                                "type", "date", "notes", "odometer-reading", "payment-type", "tags", "total-cost",
                                "place-name", "place-full-address", "place-street", "place-city", "place-state",
                                "place-country", "place-postal-code", "place-google-places-id", "place-longitude",
                                "place-latitude", "device-longitude", "device-latitude"
                            ]
                        ],
                        html.div({"style": {"marginTop": "1.2rem"}}, [
                            html.label({"style": {"fontWeight": "600", "marginBottom": "0.5rem", "fontSize": "1.1rem"}}, "Subtypes"),
                            html.div({"style": {"display": "grid", "gridTemplateColumns": "repeat(3, 1fr)", "gap": "0.5rem"}}, [
                                html.label({"style": {"display": "flex", "alignItems": "center", "gap": "0.4rem"}}, [
                                    html.input({
                                        "type": "checkbox",
                                        "checked": event_form_data.get("subtypes", {}).get(subtype, False),
                                        "on_change": lambda e, s=subtype: handle_event_form_change("subtypes", (s, e['target']['checked'])),
                                        "style": {"accentColor": selected_bg}
                                    }),
                                    html.span({}, subtype)
                                ])
                                for subtype in subtype_keys
                            ])
                        ]),
                        event_submit_status and html.div({"style": {"marginTop": "1rem", "color": selected_bg, "fontWeight": "600"}}, event_submit_status),
                        html.div({"style": {"display": "flex", "gap": "1rem", "marginTop": "1.5rem"}}, [
                            html.button({
                                "type": "button",
                                "style": {
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
                                "on_click": lambda e: submit_event_form()
                            }, "Submit"),
                            html.button({
                                "type": "button",
                                "style": {
                                    "padding": "1rem 2.2rem",
                                    "background": border_color,
                                    "color": dark_fg,
                                    "border": f"1px solid {selected_bg}",
                                    "borderRadius": "12px",
                                    "fontSize": "1.15rem",
                                    "cursor": "pointer",
                                    "fontFamily": "inherit",
                                    "fontWeight": "700",
                                    "boxShadow": "0 6px 24px rgba(58,175,169,0.10)",
                                    "letterSpacing": "0.03em",
                                    "transition": "background 0.2s, box-shadow 0.2s"
                                },
                                "on_click": lambda e: set_show_event_form(False)
                            }, "Cancel")
                        ])
                    ])
                ),
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
                ,
                car_info and html.div({"style": {"width": "100%", "maxWidth": "900px", "marginTop": "1rem"}},
                    html.div({"style": {
                        "background": card_bg,
                        "color": dark_fg,
                        "padding": "1.5rem 2rem 1.2rem 2rem",
                        "borderRadius": "12px",
                        "marginBottom": "1.5rem",
                        "boxShadow": card_shadow,
                        "borderLeft": f"6px solid {selected_bg}",
                        "fontSize": "1.08rem",
                        "whiteSpace": "normal",
                        "transition": "box-shadow 0.2s",
                        "overflow": "hidden"
                    }}, [
                        html.h3({"style": {"marginBottom": "1.2rem", "fontWeight": "600", "fontSize": "1.3rem", "color": selected_bg}}, "Car Information"),
                        html.ul({"style": {"listStyle": "none", "padding": 0, "margin": 0}}, [
                            html.li({"style": {"marginBottom": "0.8rem", "padding": 0}}, [
                                html.span({"style": {"fontWeight": "600", "color": selected_bg, "marginRight": "0.7rem"}}, f"{key}:") ,
                                html.span({"style": {"fontWeight": "400", "color": dark_fg}}, f" {value}")
                            ])
                            for key, value in car_info.items() if value not in [None, ""]
                        ])
                    ])
                )
            )
        )
    )

if __name__ == "__main__":
    run(Dashboard)
