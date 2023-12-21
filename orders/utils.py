import datetime


def generate_order_numbers(pk):
    current_datetime = datetime.datetime.now().strftime('%Y%m%d%H%M%S') #202311061432 + pk
    order_number = current_datetime + str(pk)
    return order_number