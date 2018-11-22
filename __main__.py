import sys
sys.path.append('./')

from display import display
from search import search
from send import send
import os
import schedule
import time
os.chdir(os.path.dirname(__file__))

def job(target):
    result = search(target)
    #display(result)
    send(result)

if __name__ == '__main__':
    right_input = False

    while right_input is False:
        use_schedule = input('DO YOU WANT TO CHECK A PRODUCT IN EVERY FIVE MINUTES?(Y/N)')
        if use_schedule.lower() == 'y':
            right_input = True
            target = input('SEARCH A PRODUCT NAME OR CATEGORY:')
            print('START TO CHECK {} IN EVERY FIVE MINUTES.'.format(target))
            schedule.every(5).minutes.do(job, target)

            while True:
                schedule.run_pending()
                time.sleep(1)

        elif use_schedule.lower() =='n':
            right_input = True
            target = input('SEARCH A PRODUCT NAME OR CATEGORY:')
            result = search(target)
            display(result)
        else:
            print('PLRASE ENTER Y OR N !!!')
