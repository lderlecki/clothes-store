from datetime import date


def generate_order_id(id):
    order_date = date.today().strftime('%Y%m%d')
    return f'{order_date}-{str(id).zfill(6)}'
