def prepare_text(title, description):
    text = title + ' ' + description
    return text.lower()

def check_list_in_text(text, search_list):
    if any(ext in text for ext in search_list):
        return True
    else:
        return False

def read_page(page_file):
    try:
        with open(page_file, 'r') as f_page:
            page = int(f_page.read())
    except:
        page = 1

def set_page(page_file, page):
    with open('page_google.txt', 'w') as f_page:
        f_page.write(str(page))
    page += 1
    return page