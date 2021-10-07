import importlib
import tracemalloc
from typing import Callable

import click
import yaml

from fpgen.orm.abstract_fixtures_loader import AbstractFixturesLoader


class Loader:
    def __init__(
            self,
            config_path: str,
            environment: str,
            to_skip_interaction: bool = False
    ) -> None:
        self.config_path = config_path
        self.environment = environment
        self.to_skip_interaction = to_skip_interaction

        self.successful_load = 0

    def load(self):
        click.clear()
        if not self.to_skip_interaction:
            click.confirm(
                "This command will generate new fixtures data. "
                "Would you like to continue?",
                abort=True
            )

        try:
            load_fixtures = self.load_fixtures_from_config()
        except (yaml.MarkedYAMLError, KeyError, AttributeError) as exc:
            click.echo(
                click.style(
                    f"Error processing {self.config_path} file: \n {exc}",
                    fg="red"
                )
            )
            return

        tracemalloc.start()

        for fixture in load_fixtures.values():
            self._fill_db(fixture["class"], fixture["attributes"])

        current, peak = tracemalloc.get_traced_memory()
        click.echo(
            click.style(
                f"Successfully loaded {self.successful_load} fixtures!",
                fg="green"
            )
        )
        click.echo(
            click.style(
                f"Current memory usage: {current / 10 ** 3} KB;" 
                f"Peak usage: {peak / 10 ** 3} KB",
                fg="white"
            )
        )

    def _fill_db(self, fixture: Callable[..., AbstractFixturesLoader], attrs: dict) -> None:
        try:
            obj = fixture()
            if attrs:
                if quantity := attrs.get("quantity"):
                    obj.quantity = quantity
                if catalog := attrs.get("catalog"):
                    obj.catalog = catalog
            if self.environment in obj.env_group():
                obj.auto_load() if attrs.get("autoload") else obj.load()
                self.successful_load += 1
                click.echo(
                    click.style(
                        f"{fixture.__name__} fixtures loaded successfully",
                        fg="green"
                    )
                )
        except Exception as e:
            click.echo(
                click.style(
                    f"Error processing {fixture.__name__} fixture: \n {e}",
                    fg="red"
                )
            )
            return

    def load_fixtures_from_config(self) -> dict:
        """Load models that presented in config .yaml file"""
        with open(self.config_path) as config:
            config = yaml.safe_load(config)
            load_fixtures = {}
            fixture_classes = config["fixtures"].get("load", {})
            for fixture in fixture_classes.values():
                module = importlib.import_module(f"{config['fixtures']['base_dir']}.{fixture['module']}")
                load_fixtures[fixture["class"]] = {
                    "class": getattr(module, fixture["class"]),
                    "attributes": fixture.get("attributes", {}),
                }
            return load_fixtures
