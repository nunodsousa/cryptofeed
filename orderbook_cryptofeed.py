################################################################################
# Very simple Cryptofeed example where we maintain a structured orderbook.
# The major difference between this and and the demo.py presented as an example of the library
# is the use of a orderbook defined in the main function.
#
# Nuno de Sousa
# June 2021
################################################################################

import functools as fct
from cryptofeed import FeedHandler
from cryptofeed.defines import BID, ASK, L2_BOOK
from cryptofeed.exchanges import Kraken
from datetime import datetime
import threading
import asyncio


def filter_orderbook(orderbooks, book, symbol, depth = 10):
    orderbook = {}
    orderbook[BID] = dict(zip(list(book[BID].keys())[-depth:], list(book[BID].values()[-depth:])))
    orderbook[ASK] = dict(zip(list(book[ASK].keys())[:depth], list(book[BID].values()[:depth])))
    orderbooks[symbol] = orderbook
    return orderbooks

async def bookfunc(params, orderbooks, feed, symbol, book, timestamp, receipt_timestamp):

    print(5*"_*")
    dt_object = datetime.fromtimestamp(timestamp)
    print("datetime object: ", dt_object)
    print(f'Timestamp: {timestamp} Cryptofeed Receipt: {receipt_timestamp} Feed: {feed} Symbol: {symbol}'
          f' Book Bid Size is {len(book[BID])} Ask Size is {len(book[ASK])}')
    orderbooks = filter_orderbook(orderbooks, book, symbol, params['orderbook']['depth'])
    print(orderbooks)


def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Parameters
    params = {'orderbook': {'depth': 2}, 'price_model':{}, 'trade_model': {}}
    config = {'uvloop': False, 'log': {'filename': 'demo.log', 'level': 'INFO'}}

    orderbooks = {}

    f = FeedHandler(config=config)
    l2_book = ['BTC-USD', 'ETH-USD', 'LINK-USD', 'LTC-USD', 'ADA-USD']
    f.add_feed(Kraken(checksum_validation=True, subscription={L2_BOOK: l2_book},
                      callbacks={L2_BOOK: fct.partial(bookfunc, params, orderbooks)})) # This way passes the orderbooks inside the callback

    # OnClick Run
    f.run(install_signal_handlers=False)

    # OnClick Stop
    #f.stop()

if __name__ == '__main__':
    thread = threading.Thread(target=main)
    thread.start()
    thread.join()