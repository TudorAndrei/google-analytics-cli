#!/usr/bin/env python

# Copyright 2025 Google LLC All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Typer-based CLI for Google Analytics APIs."""

import asyncio
import json
from typing import Any, List, Optional

import typer

app = typer.Typer(help="Run Google Analytics Admin and Data API queries.")


def _parse_json_argument(raw: Optional[str], arg_name: str) -> Any:
    if raw is None:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError as error:
        raise typer.BadParameter(
            f"{arg_name} must be valid JSON: {error.msg}"
        ) from error


def _print_json(data: Any) -> None:
    typer.echo(json.dumps(data, indent=2, sort_keys=True))


@app.command()
def account_summaries() -> None:
    """List all account summaries and property summaries."""
    from analytics_cli.tools.admin.info import get_account_summaries

    result = asyncio.run(get_account_summaries())
    _print_json(result)


@app.command()
def property_details(
    property_id: str = typer.Argument(
        ..., help="Property ID like 12345 or properties/12345"
    ),
) -> None:
    """Get metadata details for a property."""
    from analytics_cli.tools.admin.info import get_property_details

    result = asyncio.run(get_property_details(property_id))
    _print_json(result)


@app.command()
def google_ads_links(
    property_id: str = typer.Argument(
        ..., help="Property ID like 12345 or properties/12345"
    ),
) -> None:
    """List Google Ads links for a property."""
    from analytics_cli.tools.admin.info import list_google_ads_links

    result = asyncio.run(list_google_ads_links(property_id))
    _print_json(result)


@app.command()
def property_annotations(
    property_id: str = typer.Argument(
        ..., help="Property ID like 12345 or properties/12345"
    ),
) -> None:
    """List reporting data annotations for a property."""
    from analytics_cli.tools.admin.info import list_property_annotations

    result = asyncio.run(list_property_annotations(property_id))
    _print_json(result)


@app.command()
def custom_dimensions_metrics(
    property_id: str = typer.Argument(
        ..., help="Property ID like 12345 or properties/12345"
    ),
) -> None:
    """List custom dimensions and metrics for a property."""
    from analytics_cli.tools.reporting.metadata import (
        get_custom_dimensions_and_metrics,
    )

    result = asyncio.run(get_custom_dimensions_and_metrics(property_id))
    _print_json(result)


@app.command()
def report(
    property_id: str = typer.Argument(
        ..., help="Property ID like 12345 or properties/12345"
    ),
    date_ranges: str = typer.Option(
        ...,
        "--date-ranges",
        help=(
            "JSON array, for example: "
            '[{"start_date":"7daysAgo","end_date":"yesterday"}]'
        ),
    ),
    dimensions: List[str] = typer.Option(
        ..., "--dimension", help="Repeat to add dimensions"
    ),
    metrics: List[str] = typer.Option(
        ...,
        "--metric",
        help="Repeat to add metrics",
    ),
    dimension_filter: Optional[str] = typer.Option(
        None, help="JSON object for FilterExpression"
    ),
    metric_filter: Optional[str] = typer.Option(
        None, help="JSON object for FilterExpression"
    ),
    order_bys: Optional[str] = typer.Option(
        None,
        help="JSON array of OrderBy objects",
    ),
    limit: Optional[int] = typer.Option(None),
    offset: Optional[int] = typer.Option(None),
    currency_code: Optional[str] = typer.Option(None),
    return_property_quota: bool = typer.Option(False),
) -> None:
    """Run a core Data API report."""
    from analytics_cli.tools.reporting.core import run_report

    result = asyncio.run(
        run_report(
            property_id=property_id,
            date_ranges=_parse_json_argument(date_ranges, "date_ranges"),
            dimensions=dimensions,
            metrics=metrics,
            dimension_filter=_parse_json_argument(dimension_filter, "dimension_filter"),
            metric_filter=_parse_json_argument(metric_filter, "metric_filter"),
            order_bys=_parse_json_argument(order_bys, "order_bys"),
            limit=limit,
            offset=offset,
            currency_code=currency_code,
            return_property_quota=return_property_quota,
        )
    )
    _print_json(result)


@app.command()
def realtime_report(
    property_id: str = typer.Argument(
        ..., help="Property ID like 12345 or properties/12345"
    ),
    dimensions: List[str] = typer.Option(
        ..., "--dimension", help="Repeat to add dimensions"
    ),
    metrics: List[str] = typer.Option(
        ...,
        "--metric",
        help="Repeat to add metrics",
    ),
    dimension_filter: Optional[str] = typer.Option(
        None, help="JSON object for FilterExpression"
    ),
    metric_filter: Optional[str] = typer.Option(
        None, help="JSON object for FilterExpression"
    ),
    order_bys: Optional[str] = typer.Option(
        None,
        help="JSON array of OrderBy objects",
    ),
    limit: Optional[int] = typer.Option(None),
    offset: Optional[int] = typer.Option(None),
    return_property_quota: bool = typer.Option(False),
) -> None:
    """Run a realtime Data API report."""
    from analytics_cli.tools.reporting.realtime import run_realtime_report

    result = asyncio.run(
        run_realtime_report(
            property_id=property_id,
            dimensions=dimensions,
            metrics=metrics,
            dimension_filter=_parse_json_argument(dimension_filter, "dimension_filter"),
            metric_filter=_parse_json_argument(metric_filter, "metric_filter"),
            order_bys=_parse_json_argument(order_bys, "order_bys"),
            limit=limit,
            offset=offset,
            return_property_quota=return_property_quota,
        )
    )
    _print_json(result)


if __name__ == "__main__":
    app()
