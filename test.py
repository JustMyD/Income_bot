from datetime import datetime as dt
import datetime


if __name__ == '__main__':
    print(dt.now().date())
    print(dt.now().utcnow().date() - datetime.timedelta(days=4))
