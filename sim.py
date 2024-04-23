import yfinance as yf

# Get hourly data for last 700 days
data = yf.download('USDCAD=X', period='30d', interval='1h')

openPosition = 0
completedTradeLog = []

print("Buy: 1, Hold: 0, Sell: -1, Exit: 9")

for i in range(len(data)):
    print("Date: ", data.index[i], "Open: ", "{:.4f}".format(data['Open'].iloc[i]), "High: ", "{:.4f}".format(data['High'].iloc[i]), "Low: ", "{:.4f}".format(data['Low'].iloc[i]), "Close: ", "{:.4f}".format(data['Close'].iloc[i]))
    action = input("1: Buy, 0: Hold, -1: Sell, 9: Exit    ")

    if action == '9':
        break

    if action == '1':
        if openPosition == 0: #open long position
            openBuy_price = data['Close'].iloc[i]
            openBuy_date = data.index[i]
            openPosition = 1
            print("Bought at: ", "{:.4f}".format(openBuy_price), "on: ", openBuy_date)

            continue
        else: #close short position
            openPosition = 0
            closeBuy_price = data['Close'].iloc[i]
            closeBuy_date = data.index[i]
            completedTradeLog.append({"Type": "Short", "Open": openSell_price, "Close": closeBuy_price, "Open Date": openSell_date, "Close Date": closeBuy_date, 
                                      "Profit": closeBuy_price - openSell_price, 'Percent Profit': (closeBuy_price - openSell_price) / openSell_price * 100})
            print("Closed short at: ", "{:.4f}".format(closeBuy_price), "on: ", closeBuy_date, "Profit: ", "{:.4f}".format(-(closeBuy_price - openSell_price)))
            continue

    if action == '-1': 
        if openPosition == 0: #open short position
            openSell_price = data['Close'].iloc[i]
            openSell_date = data.index[i]
            openPosition = -1
            print("Sold at: ", "{:.4f}".format(openSell_price), "on: ", openSell_date)

            continue
        else: #close long position
            openPosition = 0
            closeSell_price = data['Close'].iloc[i]
            closeSell_date = data.index[i]
            completedTradeLog.append({"Type": "Long", "Open": openBuy_price, "Close": closeSell_price, "Open Date": openBuy_date, "Close Date": closeSell_date, 
                                      "Profit": closeSell_price - openBuy_price, 'Percent Profit': (closeSell_price - openBuy_price) / openBuy_price * 100})
            print("Closed long at: ", "{:.4f}".format(closeSell_price), "on: ", closeSell_date, "Profit: ", "{:.4f}".format(closeSell_price - openBuy_price))
            continue

    if action == '0':
        continue

print("Completed Trades: ", completedTradeLog)

# Calculate total profit
totalProfit = 0
for trade in completedTradeLog:
    totalProfit += trade["Profit"]

print("Total Profit: ", totalProfit)

# Calculate total percent profit
totalPercentProfit = 0
for trade in completedTradeLog:
    totalPercentProfit += trade["Percent Profit"]

print("Total Percent Profit: ", totalPercentProfit)

# Calculate average percent profit
averagePercentProfit = totalPercentProfit / len(completedTradeLog)
print("Average Percent Profit: ", averagePercentProfit)

# Calculate number of trades
numTrades = len(completedTradeLog)
print("Number of Trades: ", numTrades)

# Calculate win rate
numWins = 0
for trade in completedTradeLog:
    if trade["Profit"] > 0:
        numWins += 1

winRate = numWins / numTrades
print("Win Rate: ", winRate)

# Calculate average profit per trade
averageProfitPerTrade = totalProfit / numTrades
print("Average Profit Per Trade: ", averageProfitPerTrade)
