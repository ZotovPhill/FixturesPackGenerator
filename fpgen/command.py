import click
import yaml

from fpgen.loader import Loader


@click.command(options_metavar="<options>")
@click.argument("config_path")
@click.option(
    "-s",
    "--skip-interaction",
    "to_skip_interaction",
    is_flag=True,
    default=False,
    metavar="<bool>",
    help=f"WARNING! Pointing this argument consent to the deletion "
         f"of all data and database and applying fixtures.",
)
@click.option(
    "-e",
    "--environment",
    "environment",
    metavar="<str>",
    help=f"Pass environment value to load fixtures",
)
def load_fixtures(config_path: str, environment: str, to_skip_interaction: bool):
    Loader(config_path, environment, to_skip_interaction).load()


@click.command(options_metavar="<options>")
@click.argument("config_path")
def create_config(config_path: str):
    output_data = {
        'fixtures': {
            'base_dir': 'fpgen.example.fixtures.v1',
            'load': {
                '$EntityFaker$': {
                    'module': '$module_name$',
                    'class': '$class_name$',
                    'attributes': {
                        'quantity': '$quantity$'
                    },
                },
                '$EntityCatalog$': {
                    'module': '$module_name$',
                    'class': '$class_name$',
                    'attributes': {
                        'catalog': '$catalog_file_path$'
                    },
                },
            }
        }
    }

    f = open(config_path, 'w+')
    yaml.dump(output_data, f, allow_unicode=True)


@click.command()
@click.confirmation_option(prompt='Are you sure you want to drop the db?')
def drop_db():
    click.echo('Dropped all tables!')


@click.group()
def cli():
    pass


cli.add_command(load_fixtures)
cli.add_command(create_config)
cli.add_command(drop_db)

if __name__ == '__main__':
    cli()
