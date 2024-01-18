def extract_filename_from_url(url: str) -> str:
    # Find the index of the last /
    last_slash_index = url.rfind('/')

    # Find the index of the last .
    last_period_index = url.rfind('.')

    # Extract the substring between the last / and .
    extracted_words = url[last_slash_index + 1: last_period_index]

    return extracted_words


def extract_file_from_url(url: str) -> str:
    # Find the index of the last /
    last_slash_index = url.rfind('/')

    # Extract the substring between the last / and .
    extracted_words = url[last_slash_index + 1:]

    return extracted_words
