from reactpy import html, component, run

@component
def App():
    return html.div(
        html.h1("Car Maintenance Tracker"),
        html.p("Welcome! UI coming soon.")
    )

if __name__ == "__main__":
    run(App)
