import os
import click
import logging

from stactools.jrc_gsw import stac

logger = logging.getLogger(__name__)


def create_jrc_gsw_command(cli):
    """Creates the joint research centre - global surface water command line utility."""

    @cli.group(
        "jrc-gsw",
        short_help=("Commands for working with JRC-GSW data."),
    )
    def jrc_gsw():
        pass

    @jrc_gsw.command(
        "create-collection",
        short_help="Creates STAC collections for JRC-GSW data.",
    )
    @click.option(
        "-d",
        "--destination",
        required=True,
        help="The output directory for the STAC Collection json.",
    )
    def create_collection_command(destination: str):
        """Creates a STAC Collection for each mapped dataset from the European Commission
        Joint Research Centre - Global Surface Water program.

        Args:
            destination (str): Directory used to store the STAC collections.
        Returns:
            Callable
        """
        root_col = stac.create_collection()

        root_col.normalize_hrefs(destination)
        root_col.save()
        root_col.validate()

    @jrc_gsw.command(
        "create-item",
        short_help="Create a STAC item from a given COG.",
    )
    @click.option(
        "-d",
        "--destination",
        required=True,
        help="The output directory for the STAC json.",
    )
    @click.option(
        "-s",
        "--source",
        required=True,
        help="The root data directory.",
    )
    @click.option(
        "-t",
        "--tile_id",
        required=True,
        help="The tile ID to process.",
    )
    @click.option(
        "-y",
        "--year",
        required=True,
        help="Year to process.",
    )
    @click.option(
        "-m",
        "--month",
        required=True,
        help="Month to process.",
    )
    def create_item_command(
        destination: str, source: str, tile_id: str, year: int, month: int
    ):
        """Creates a STAC Item

        Args:
            destination (str): The output directory for the STAC json.
            source (str): The root data directory. Must follow the
                          structure found in:
                          http://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GSWE/
            tile_id (str): The tile ID to process.
            year (int): Year to process.
            month (int): Month to process.
        """
        item = stac.create_item(source, tile_id, year, month)
        item_path = os.path.join(destination, f"{item.id}.json")
        item.set_self_href(item_path)
        item.save_object()

    return jrc_gsw
