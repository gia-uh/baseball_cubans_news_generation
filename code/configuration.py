from notice_pipeline import Configuration
from notice_pipeline.date import get_date
import json
import datetime
import os
try:
    MODULE = os.path.dirname(os.path.realpath(__file__))
except:
    MODULE = ""

class Armandobot(Configuration):
    __slots__ = ()

    def _before_run(self, *args, **kwargs):
        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        y = today - oneday

        day = str(y.day)
        month = str(y.month)
        year = str(y.year)

        if len(day) == 1:
            day = '0' + day

        if len(month) == 1:
            month = '0' + month

        name = year + '-' + month + '-' + day
        try:
            past_news = json.load(open('past_news.json'))
        except Exception as e:
            print(e)
            past_news = {}

        if name in past_news:
            with open('UPDATED','w') as f:
                f.write('1')
            return False

        d = get_date()

        if name != d:
            with open('UPDATED','w') as f:
                f.write('1')
            return False

        with open('UPDATED','w') as f:
            f.write('0')
        return True

    def _after_run(self, *args, **kwargs):
        res = kwargs.pop('pipeline_result')
        res["author"] = "Armanbot"
        try:
            past_news = json.load(open('past_news.json'))
        except Exception as e:
            print(e)
            past_news = {}

        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        y = today - oneday

        day = str(y.day)
        month = str(y.month)
        year = str(y.year)

        if len(day) == 1:
            day = '0' + day

        if len(month) == 1:
            month = '0' + month

        name = year + '-' + month + '-' + day

        past_news[name] = res

        json.dump(past_news, open('past_news.json', 'w'), indent=2)

        

        #r.render()

        return (res['title'], res['paragraphs'], res['summary'])

if __name__ == "__main__":
    cfg = Armandobot(config_file=os.path.join(MODULE, 'config.ini'))
    cfg.run()
