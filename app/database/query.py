from app.database.connection import get_connection

def search_inventory(style=None, colour=None, size=None, distributor=None):
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
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
    WHERE 1=1
    """

    params = []

    if style:
        sql += " AND p.Style = ?"
        params.append(style)

    if colour:
        sql += " AND p.Colour LIKE ?"
        params.append(f"%{colour}%")

    if size:
        sql += " AND p.Size = ?"
        params.append(size)

    if distributor:
        sql += " AND i.Distributor LIKE ?"
        params.append(f"%{distributor}%")

    cursor.execute(sql, params)

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
            "InTransitQty": row[6],
        })

    conn.close()
    return result