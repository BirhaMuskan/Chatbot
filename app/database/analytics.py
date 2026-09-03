from app.database.connection import get_connection

def get_low_stock_items():

    conn = get_connection()

    cursor = conn.cursor()

    query = """
    SELECT
        p.Style,
        p.Colour,
        p.Size,
        i.Distributor,
        i.AvailableQty,
        i.CommittedQty,
        i.InTransitQty
    FROM Products p
    INNER JOIN Inventory i
        ON p.SKU = i.SKU
    WHERE i.AvailableQty < 500
    """

    cursor.execute(query)

    rows = cursor.fetchall()

    result = []

    for row in rows:

        result.append({
            "Style": row[0],
            "Colour": row[1],
            "Size": row[2],
            "Distributor": row[3],
            "AvailableQty": row[4],
            "CommittedQty": row[5],
            "InTransitQty": row[6]
        })

    conn.close()

    return result