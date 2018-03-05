# -*- coding: utf-8 -*-
"""
Created on Sun Mar 04 17:25:37 2018

@author: John
"""

import clsTrade
import clsPortfolio

import csv




        
        
StockList = ['AAPL','AMZN','INTC', 'MSFT', 'SNAP']

class TradeModelView:
    def __init__(self):
        self.objTrade = clsTrade.Trade()
        self.objPortfolio = clsPortfolio.Portfolio()    
        self.dict_stockBidPx = {}
        self.dict_stockAskPx = {}
        self.dict_stockOpenPx = {}
        self.dict_stockClosePx = {}        
        self.dict_stockStatusPx = {} #Y = good data, N =bad data
        
    #return records for holdings    
    def DisplayCurrentHoldings(self):
        print("Current Cash: " + str(self.objPortfolio.GetCash()))
        currentHoldings = self.objPortfolio.GetPositions()
        
        dict_symbolaggHld = {}
        
        #aggreate holdings (lot level, different by trade time)
        for h in currentHoldings:
            if dict_symbolaggHld.has_key(h.Symbol):
                dict_symbolaggHld[h.Symbol] = dict_symbolaggHld[h.Symbol] + h.Units
            else:
                dict_symbolaggHld[h.Symbol] = h.Units
       
        self.RefreshPrice()
        
        print("Current Holdings:")
        #display sorted holdings
        print("Symbol | Units | Price | Market Value")
        for h_key in sorted(dict_symbolaggHld.keys()):
            current_price = (self.dict_stockAskPx[h_key] + self.dict_stockBidPx[h_key])/2 #usually curretn price = (bid + ask)/2
            market_value = dict_symbolaggHld[h_key]*current_price # market value for position = units * current price           
            print(h_key + "   " + str(dict_symbolaggHld[h_key]) + "   " + str(current_price) + "   " + str(market_value) )
    
    def RefreshPrice(self):
        print("Refreshing price...")
        
        for sym in StockList:
            stock_quote = clsTrade.Quote #create new instance
            stock_quote = self.objTrade.GetQuote(sym) #get stock quote
            
            #add or update stock bid price
            self.dict_stockBidPx[sym] = stock_quote.Bid
            self.dict_stockAskPx[sym] = stock_quote.Ask
            self.dict_stockOpenPx[sym] = stock_quote.Open
            self.dict_stockClosePx[sym] = stock_quote.Close 
            self.dict_stockStatusPx[sym] = stock_quote.Status                   
    
    def TradeBuy(self):
        
       
        
        self.RefreshPrice()
        
        #once it is done, clear the screen
        print("\n"*100)
        self.DisplayCurrentHoldings()
        
        print("Stock | Bid | Ask | Open | Close | Quote Status")
        for sym in StockList:
            print(sym + "  " + str(self.dict_stockBidPx[sym]) + " " +  str(self.dict_stockAskPx[sym]) + " " +  str(self.dict_stockOpenPx[sym]) + " " +  str(self.dict_stockClosePx[sym]) + " " +  str(self.dict_stockStatusPx[sym]))

        print("Action: Buy")
        input_sym = raw_input("Enter the stock symbol:").strip()
        input_units = raw_input("Enter units:").strip()
        
        input_sym = input_sym.upper() #converrt symbol to uppper class
        
        int_units = 0
        
        if input_units.isdigit(): #convert to digit for input
            int_units = int(input_units)    
        
        
        print("Buy " + str(int_units) + " shares of " + str(input_sym))
        
        input_confirm = raw_input("Confirm (Y/N):").strip().upper()
        
        
        if input_confirm == "Y":
            if self.dict_stockBidPx.has_key(input_sym) and input_units.isdigit():
                if int_units > 0: #buy units > 0
                
                    #Cash control that prevent account in debt, use ask for buy
                    if int_units * self.dict_stockAskPx[input_sym] < self.objPortfolio.GetCash():
                        order = self.objTrade.OrderEntry("BUY",input_sym,int_units,0,"")
                        self.objPortfolio.UpdatePosition(order)
                    else:
                        print("Not Enough Cash to cover your order.  Order is cancelled.")
        else:    
            print("Cancel!")
        
        input_pause = raw_input("Enter to Continue...").strip()
        
    def TradeSell(self):
        
        
        
        self.RefreshPrice()
        
        #once it is done, clear the screen
        print("\n"*100)
        self.DisplayCurrentHoldings()
        
        print("Stock | Bid | Ask | Open | Close | Quote Status")
        for sym in StockList:
            print(sym + "  " + str(self.dict_stockBidPx[sym]) + " " +  str(self.dict_stockAskPx[sym]) + " " +  str(self.dict_stockOpenPx[sym]) + " " +  str(self.dict_stockClosePx[sym]) + " " +  str(self.dict_stockStatusPx[sym]))

        print("Action: Sell")
        input_sym = raw_input("Enter the stock symbol:").strip()
        input_units = raw_input("Enter units:").strip()
        
        input_sym = input_sym.upper() #converrt symbol to uppper class
        
        int_units = 0
        
        if input_units.isdigit(): #convert to digit for input
            int_units = abs(int(input_units))    
        
        
        print("Sell " + str(int_units) + " shares of " + str(input_sym))
        
        input_confirm = raw_input("Confirm (Y/N):").strip().upper()
        
        
        if input_confirm == "Y":
            if self.dict_stockBidPx.has_key(input_sym) and input_units.isdigit():
                if int_units > 0: # units > 0
                
                    #Security Sell control that prevent account oversold
                    sym_pos = self.objPortfolio.GetPositionsBySym(input_sym)
                    sym_pos = sorted(sym_pos, key = lambda pos: (pos.PurchasedDate))
                    
                    sym_pos_agg = 0
                    for p in sym_pos:
                        sym_pos_agg = sym_pos_agg + p.Units
                    
                    
                    if int_units <= sym_pos_agg: #regular sell
                        
                        agg_sell_amount = int_units
                        
                        for pos in sym_pos:
                            if agg_sell_amount >= pos.Units: #sell the whole lot
                                    order = self.objTrade.OrderEntry("SELL",input_sym,pos.Units,pos.CostBasis,pos.PurchasedDate)
                                    self.objPortfolio.UpdatePosition(order)
                                    
                                    agg_sell_amount = agg_sell_amount - pos.Units #reduce the sell amount
                                    
                            else: #current pos is enough to cover
                            #sell partial lot, update cost basis for remained position
                                agg_sell_costBasis =  (float(agg_sell_amount)/float(pos.Units) * float(pos.CostBasis)
                                order = self.objTrade.OrderEntry("SELL",input_sym,agg_sell_amount,agg_sell_costBasis,pos.PurchasedDate)
                                self.objPortfolio.UpdatePosition(order)
                                    
                    else: #shorting
                        print("Not Enough Cash to cover your order.  Order is cancelled.")
        else:    
            print("Cancel!")
        
        input_pause = raw_input("Enter to Continue...").strip()

class BlotterModelView:
    def ReadOrderHistory(self):
        
        f = open("OrderHistory.csv",'rb')
        csvReader = csv.reader(f)
        print("Action | Symbol | Units | Amount | ExecPx | ExecDate | CostBasis | LotPurchasedDate(sell)")
        for row in csvReader:
            if len(row) > 3:
                if(row[0]!='Action'): #skip the header line
                    #create object to store position
                    
                    print(row[0] + "," + row[1] + "," + row[2] + "," + row[3] + "," + row[4] + "," + row[5]  + "," + row[6] + "," + row[7] )
                
        f.close()
    
