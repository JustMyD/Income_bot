from datetime import datetime as dt
import datetime


if __name__ == '__main__':
    # print(dt.now().day)
    # print(dt.now().utcnow().date() - datetime.timedelta(days=4))
    end_date = 31
    month = [[num for num in list(range(elem, elem+7)) if num <= end_date] for elem in list(range(1, end_date+1, 7))]
    print(month)
