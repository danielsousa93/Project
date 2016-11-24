from yahoo_finance import Share
from pprint import pprint

share = Share('MMM')



print('get_price:', share.get_price())
'''
This is the price that the company closed at the day before. 
'''


print('get_change:', share.get_change())
'''
Difference between the last day's close price and the day before's close price
For instance, in 23th, get_change would give me Adj_Close/Close(22-21) from 
    get_historical method
'''


print('get_volume:', share.get_volume())
'''
Refers to how many shares traded hands at the day before.
'''


print('get_open:', share.get_open())
'''
the day before's open price.
'''


print('get_avg_daily_volume:', share.get_avg_daily_volume())
'''
Average volume over 3 months. 24th: 1910760.
'''


print('get_stock_exchange:', share.get_stock_exchange())
'''
Stock Exchange where the values come from.
'''


print('get_market_cap:', share.get_market_cap())
'''
Total value of the company.
'''


print('get_book_value:', share.get_book_value())
'''
It would be the amount of money that a holder of a
common share would get if a company were to liquidate.
'''


print('get_ebitda:', share.get_ebitda())
'''
EBITDA is a financial number that measures a company's 
profitability before deductions that are considered somewhat 
superfluous to the business decision-making process. 
These deductions are interest, taxes, deprecation and amortization, 
which are not part of a company's operating costs and although 
important, should be dealt with separately.
'''


print('get_dividend_share:', share.get_dividend_share())
'''
The total amount of the anual dividend
'''


print('get_dividend_yield:', share.get_dividend_yield())
'''
Percentage that gives the dividend
'''


print('get_earnings_share:', share.get_earnings_share())
'''
EPS or, Earnings Per Share is the portion of a company’s 
profit allocated to each outstanding share of common stock.
'''


print('get_days_high:', share.get_days_high())
'''
Highest value of the day
'''


print('get_days_low:', share.get_days_low())
'''
Lowest value of the day
'''


print('get_year_high:', share.get_year_high())
'''
Highest value of the year
'''


print('get_year_low:', share.get_year_low())
'''
Lowest value of the year
'''


print('get_50day_moving_avg:', share.get_50day_moving_avg())
'''
Comparison between last 50 days and a lag of 50 days
'''


print('get_200day_moving_avg:', share.get_200day_moving_avg())
'''
Comparison between last 200 days and a lag of 200 days
'''


print('get_price_earnings_ratio:', share.get_price_earnings_ratio())
'''
suppose that a company is currently trading at $43 a share and its
earnings over the last 12 months were $1.95 per share. 
The P/E ratio for the stock could then be calculated as 43/1.95, or 22.05.
'''


print('get_price_earnings_growth_ratio:', share.get_price_earnings_growth_ratio())
'''
The price/earnings to growth ratio (PEG ratio) is a stock's 
price-to-earnings (P/E) ratio divided by the growth rate of its earnings
for a specified time period. The PEG ratio is used to determine a stock's
value while taking the company's earnings growth into account, and is 
considered to provide a more complete picture than the P/E ratio.
'''


print('get_price_sales:', share.get_price_sales())
'''
A valuation ratio that compares a company’s stock price to its revenues. 
'''


print('get_price_book:', share.get_price_book())
'''
The price-to-book ratio (P/B Ratio) is a ratio used to compare a stock's 
market value to its book value. It is calculated by dividing the current 
closing price of the stock by the latest quarter's book value per share.
A lower P/B ratio could mean that the stock is undervalued. However, it 
could also mean that something is fundamentally wrong with the company. 
As with most ratios, be aware that this varies by industry.

This ratio also gives some idea of whether you're paying too much for 
what would be left if the company went bankrupt immediately.
'''


print('get_short_ratio:', share.get_short_ratio())
'''
Number of shares of a security that investors have sold short divided 
by average daily volume of the security (measured over 30 days or 90 days).
There are various interpretations of this ratio. When people short, it is 
usually (but not always) because they are pessimistic about the security's 
future performance. Shorting involves buying at at some point however. 
Hence, some would interpret a high short ratio as an indicator that there 
will be some buying pressure on the security that would increase its price.
'''


print('get_trade_datetime:', share.get_trade_datetime())
'''
Timestamp of whole values obtained with this script.
'''


print('get_historical:')
pprint(share.get_historical('2016-11-17', '2016-11-24'))
'''
Values form other days.
'''


