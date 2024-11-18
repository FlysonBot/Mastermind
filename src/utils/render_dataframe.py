def render_dataframe(df):
    # Include index column in width calculation
    index_width = max(
        len(str(df.index.name) if df.index.name else ""),
        df.index.astype(str).map(len).max(),
    )
    col_widths = [index_width]
    
    # Calculate widths for each DataFrame column
    for col in df.columns:
        col_width = max(len(str(col)), df[col].astype(str).map(len).max())
        col_widths.append(col_width)

    # Prepare header: include index name if it exists, otherwise add a space
    header = [df.index.name or " "]  # Space for index title if none
    header.extend(df.columns)

    # Print the header with dynamic widths
    print(" ".join(f"{header[i]:<{col_widths[i]}}" for i in range(len(header))))

    # Print each row with dynamic widths
    for index, row in df.iterrows():
        row_values = [str(index)] + [str(row[col]) for col in df.columns]
        print(
            " ".join(
                f"{row_values[i]:<{col_widths[i]}}" for i in range(len(row_values))
            )
        )
