import numpy as np
from datetime import datetime, date

def predictor(const, coef, date_text):
    date_object = datetime.strptime(date_text, '%Y-%m-%d').date()
    dayth = (date_object - date(2010, 7, 19)).days
    dayth = dayth + 561
    log2_pred = np.log2(dayth) * coef + const
    price_pred = 2 ** log2_pred

    return price_pred, log2_pred