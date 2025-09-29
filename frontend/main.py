from reactpy import html, component, run

@component
def App():
    """Main ReactPy App component for the car maintenance tracker UI."""
    return html.div(
        html.h1("Car Maintenance Tracker"),
        html.p("Welcome! UI coming soon.")
    )

if __name__ == "__main__":
    # Start the ReactPy frontend app
    run(App)
