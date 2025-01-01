import pandas as pd


def render_dataframe(df: pd.DataFrame) -> list[str]:
    """
    Returns the Pandas DataFrame in a human-readable format as a list of strings.

    Args:
        df (pandas.DataFrame): The DataFrame to be rendered.

    Returns:
        list: A list of strings representing the DataFrame.
    """
    # Calculate widths
    col_widths: list[int] = [_calculate_index_width(df)] + _calculate_column_widths(df)

    # Prepare header
    header: list[str] = _prepare_header(df)
    output: list[str] = [_format_row(header, col_widths)]
    # Prepare rows
    for index, row in df.iterrows():  # type: ignore
        row_values = [str(index)] + [str(row[col]) for col in df.columns]  # type: ignore
        output.append(_format_row(row_values, col_widths))  # type: ignore

    return output


def _calculate_index_width(df: pd.DataFrame) -> int:
    """
    Calculates the width of the index column.

    Args:
        df (pandas.DataFrame): The DataFrame to be analyzed.

    Returns:
        int: The width of the index column.
    """
    return max(
        len(str(df.index.name) if df.index.name else ""),  # type: ignore
        df.index.astype(str).map(len).max(),  # type: ignore
    )


def _calculate_column_widths(df: pd.DataFrame) -> list[int]:
    """
    Calculates the width of each column in the DataFrame.

    Args:
        df (pandas.DataFrame): The DataFrame to be analyzed.

    Returns:
        list: A list of column widths.
    """
    return [
        max(len(str(col)), df[col].astype(str).map(len).max())  # type: ignore
        for col in df.columns
    ]


def _prepare_header(df: pd.DataFrame) -> list[str]:
    """
    Prepares the header row for the DataFrame.

    Args:
        df (pandas.DataFrame): The DataFrame to be analyzed.

    Returns:
        list: A list of header values.
    """
    return [df.index.name or " "] + list(df.columns)  # type: ignore


def _format_row(values: list[str], widths: list[int]) -> str:
    """
    Formats a single row of the DataFrame as a string.

    Args:
        values (list): A list of values to be formatted in the row.
        widths (list): A list of column widths.

    Returns:
        str: A formatted string representing the row.
    """
    return " ".join(f"{values[i]:<{widths[i]}}" for i in range(len(values)))
