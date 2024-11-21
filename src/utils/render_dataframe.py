def render_dataframe(df):
    # Calculate widths
    col_widths = [_calculate_index_width(df)] + _calculate_column_widths(df)

    # Print header
    _print_row(_prepare_header(df), col_widths)

    # Print rows
    for index, row in df.iterrows():
        _print_row([str(index)] + [str(row[col]) for col in df.columns], col_widths)


def _calculate_index_width(df):
    return max(
        len(str(df.index.name) if df.index.name else ""),
        df.index.astype(str).map(len).max(),
    )


def _calculate_column_widths(df):
    return [
        max(len(str(col)), df[col].astype(str).map(len).max()) for col in df.columns
    ]


def _prepare_header(df):
    return [df.index.name or " "] + list(df.columns)


def _print_row(values, widths):
    print(" ".join(f"{values[i]:<{widths[i]}}" for i in range(len(values))))
