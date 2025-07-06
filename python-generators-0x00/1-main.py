from itertools import islice
stream_users = __import__('0-stream_users').stream_users

# Fetch and print first 6 rows
for user in islice(stream_users(), 6):
    print(user)
