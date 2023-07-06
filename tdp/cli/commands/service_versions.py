# Copyright 2022 TOSIT.IO
# SPDX-License-Identifier: Apache-2.0

import click
from tabulate import tabulate

from tdp.cli.queries import get_latest_success_component_version_log
from tdp.cli.session import get_session_class
from tdp.cli.utils import database_dsn
from tdp.core.models import ComponentVersionLog


@click.command(
    short_help=(
        "Get the version of deployed services."
        "(If a service has never been deployed, does not show it)"
    )
)
@database_dsn
def service_versions(database_dsn):
    session_class = get_session_class(database_dsn)

    with session_class() as session:
        latest_success_service_version = (
            get_latest_success_component_version_log(session)
        )

        click.echo(
            "Service versions:\n"
            + tabulate(
                latest_success_service_version,
                headers=[
                    ComponentVersionLog.deployment_id.name,
                    ComponentVersionLog.service.name,
                    ComponentVersionLog.component.name,
                    ComponentVersionLog.version.name,
                ],
            )
        )
