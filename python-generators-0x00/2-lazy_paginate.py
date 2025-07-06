from seed import connect_to_prodev


def paginate_users(page_size, offset):
    """
    Fetch a single page of users from the database.
    """
    connection = connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    # Convert each row to dictionary using column names
    columns = [desc[0] for desc in cursor.description]
    result = [dict(zip(columns, row)) for row in rows]

    cursor.close()
    connection.close()

    return result


def lazy_pagination(page_size):
    """
    Generator that lazily fetches and yields pages of user data.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
