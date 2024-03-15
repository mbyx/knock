from __future__ import annotations

import depict
import simulations
import typer

# TODO: Make a manual for Depict.
# TODO: Fix simulations.

app = typer.Typer()

# Map every class exported by the simulations package to its string name.
simulations: dict[str, object] = {
    simulation.lower(): getattr(simulations, simulation)
    for simulation in simulations.__all__
}


@app.command()
def run(
    simulation_name: str,
    record: bool = False,
    clear: bool = True,
    width: int = 640,
    height: int = 360,
):
    print(f"Running {simulation_name}...")
    depict.Engine(depict.Size(width, height), record=record, clear=clear).run(
        simulations[simulation_name]()
    )


@app.command()
def list(verbose: bool = False) -> None:
    if verbose:
        for i, (simulation_name, simulation) in enumerate(simulations.items()):
            print(f"{i + 1:02}) {simulation_name}: {simulation.__doc__}")
    else:
        for i, simulation in enumerate(simulations):
            print(f"{i + 1:02}) {simulation}")


if __name__ == "__main__":
    app()
