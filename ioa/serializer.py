def serialize(row):
    if not row:
        return None
    d = {}
    for column in row.keys():
        d[column] = row[column]

    return d
