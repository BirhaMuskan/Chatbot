from rapidfuzz import process, fuzz
from app.database.connection import get_connection

def get_distinct_values(column_name):
    allowed_columns = {
        "style": "Style",
        "colour": "Colour",
        "size": "Size",
        "distributor": "Distributor"
    }

    if column_name not in allowed_columns:
        return []

    sql_column = allowed_columns[column_name]

    if column_name == "distributor":
        query = f"""
        SELECT DISTINCT {sql_column}
        FROM Inventory
        WHERE {sql_column} IS NOT NULL
        """
    else:
        query = f"""
        SELECT DISTINCT {sql_column}
        FROM Products
        WHERE {sql_column} IS NOT NULL
        """

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)

    values = [str(row[0]).upper() for row in cursor.fetchall()]

    conn.close()

    return values


def fuzzy_match(input_value, column_name):
    if not input_value:
        return None

    choices = get_distinct_values(column_name)

    if not choices:
        return input_value

    cleaned_input = str(input_value).upper().replace(" ", "")

    cleaned_choices = {
        value.replace(" ", ""): value
        for value in choices
    }

    match = process.extractOne(
        cleaned_input,
        list(cleaned_choices.keys()),
        scorer=fuzz.WRatio
    )

    if not match:
        return input_value

    matched_key, score, _ = match

    if score >= 70:
        return cleaned_choices[matched_key]

    return input_value


def normalize_filters(filters):
    filters["style"] = fuzzy_match(filters.get("style"), "style")
    filters["colour"] = fuzzy_match(filters.get("colour"), "colour")
    filters["size"] = fuzzy_match(filters.get("size"), "size")
    filters["distributor"] = fuzzy_match(filters.get("distributor"), "distributor")

    return filters