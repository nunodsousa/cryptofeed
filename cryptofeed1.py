
from decimal import Decimal
import functools as fct
from cryptofeed import FeedHandler
from cryptofeed.defines import BID, ASK, L2_BOOK
from cryptofeed.exchanges import Kraken

async def bookfunc(params, orderbooks, feed, symbol, book, timestamp, receipt_timestamp):

    print(5*"_*")
    print(f'Timestamp: {timestamp} Cryptofeed Receipt: {receipt_timestamp} Feed: {feed} Symbol: {symbol}'
          f' Book Bid Size is {len(book[BID])} Ask Size is {len(book[ASK])}')
    orderbooks = filter_orderbook(orderbooks, book, symbol, params['orderbook']['depth'])
    print(orderbooks)

def main():

    # Parameters
    params = {'orderbook': {'depth': 2}, 'price_model':{}, 'trade_model': {}}
    config = {'log': {'filename': 'demo.log', 'level': 'INFO'}}

    orderbooks = {}

    f = FeedHandler(config=config)
    f.add_feed(Kraken(checksum_validation=True, subscription={L2_BOOK: ['BTC-USD', 'ETH-USD']},
                      callbacks={L2_BOOK: fct.partial(bookfunc, params, orderbooks)})) # This way passes the orderbooks inside the callback

    # OnClick Run
    f.run()

    # OnClick Stop
    #f.stop()

if __name__ == '__main__':
    main()