def render_dataframe(df):
    """
    Prints the Pandas DataFrame in a human-readable format.

    Args:
        df (pandas.DataFrame): The DataFrame to be rendered.
    """
    # Calculate widths
    col_widths = [_calculate_index_width(df)] + _calculate_column_widths(df)

    # Print header
    _print_row(_prepare_header(df), col_widths)

    # Print rows
    for index, row in df.iterrows():
        _print_row([str(index)] + [str(row[col]) for col in df.columns], col_widths)


def _calculate_index_width(df):
    """
    Calculates the width of the index column.

    Args:
        df (pandas.DataFrame): The DataFrame to be analyzed.

    Returns:
        int: The width of the index column.
    """
    return max(
        len(str(df.index.name) if df.index.name else ""),
        df.index.astype(str).map(len).max(),
    )


def _calculate_column_widths(df):
    """
    Calculates the width of each column in the DataFrame.

    Args:
        df (pandas.DataFrame): The DataFrame to be analyzed.

    Returns:
        list: A list of column widths.
    """
    return [
        max(len(str(col)), df[col].astype(str).map(len).max()) for col in df.columns
    ]


def _prepare_header(df):
    """
    Prepares the header row for the DataFrame.

    Args:
        df (pandas.DataFrame): The DataFrame to be analyzed.

    Returns:
        list: A list of header values.
    """
    return [df.index.name or " "] + list(df.columns)


def _print_row(values, widths):
    """
    Prints a single row of the DataFrame.

    Args:
        values (list): A list of values to be printed in the row.
        widths (list): A list of column widths.
    """
    print(" ".join(f"{values[i]:<{widths[i]}}" for i in range(len(values))))
