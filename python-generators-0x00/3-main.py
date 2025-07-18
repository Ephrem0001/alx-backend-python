import sys

# Import the lazy_pagination function from 2-lazy_paginate.py
lazy_paginator = __import__('2-lazy_paginate').lazy_pagination

try:
    for page in lazy_paginator(100):  # Fetch users in pages of 100
        for user in page:             # Iterate through users in the page
            print(user)               # Print each user dictionary
except BrokenPipeError:
    sys.stderr.close()
