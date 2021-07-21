import functools as fct
from cryptofeed import FeedHandler
from cryptofeed.defines import BID, ASK, L2_BOOK
from cryptofeed.exchanges import Kraken
from datetime import datetime
import threading
import asyncio

async def bookfunc(params, price_model, trade_model, orderbooks, feed, symbol, book, timestamp, receipt_timestamp):

    print(5*"_*_")
    dt_object = datetime.fromtimestamp(timestamp)
    print("datetime object: ", dt_object)
    print(f'Timestamp: {timestamp} Cryptofeed Receipt: {receipt_timestamp} Feed: {feed} Symbol: {symbol}'
          f' Book Bid Size is {len(book[BID])} Ask Size is {len(book[ASK])}')

def func():

    # Parameters
    params = {'orderbook': {'depth': 2}, 'price_model':{}, 'trade_model': {}}
    config = {'log': {'filename': 'logs/demo.log', 'level': 'INFO'}}

    orderbooks = {}
    price_model = None
    trade_model = None

    f = FeedHandler(config=config)
    f.add_feed(Kraken(checksum_validation=True, subscription={L2_BOOK: ['BTC-USD', 'ETH-USD', 'LINK-USD', 'LTC-USD', 'ADA-USD']},
                      callbacks={L2_BOOK: fct.partial(bookfunc, params, price_model, trade_model, orderbooks)})) # This way passes the orderbooks inside the callback

    # OnClick Run
    f.run()


def create_loop(func):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.call_soon(lambda: func())
    loop.run_forever()

if __name__ == "__main__":
    thread = threading.Thread(target=create_loop, args=(func, ))
    thread.start()