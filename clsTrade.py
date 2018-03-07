

#Blotter
#user see blotter (trade history)
#read(), write()

#Security List
#from securitylist.csv
#read(), write() security universe




#Trade 
#get yahoo stock quote
#Preview trade with symbol, direction, quantity, and total amount
#trade and return result

from requests import get
from bs4 import BeautifulSoup
import re
import collections
import datetime

Quote = collections.namedtuple('Quote',['Symbol','Status','Bid','Ask','Open','Close'])



#Order type
#Only one action
#Only one symbol
#Multiple units for taxlot
class Order:
    def __init__(self):
        self.id = 0
        self.Units = 0

    @property
    def Action(self):
        return self._action
    @Action.setter
    def Action(self,x):
        self._action = x
                 
    @property
    def Units(self):
        return self._units
    @Units.setter
    def Units(self,x):
        self._units = x         

    @property
    def Symbol(self):
        return self._Symbol
    
    @Symbol.setter
    def Symbol(self, x):
        self._Symbol = x
    
    @property
    def Amount(self):
        return self._amount
    @Amount.setter
    def Amount(self,x):
        self._amount = x
        
    @property
    def ExecPx(self):
        return self._ExecPx
    
    @ExecPx.setter
    def ExecPx(self,x):
        self._ExecPx = x
    
    @property
    def CostBasis(self):
        return self._CostBasis
    @CostBasis.setter
    def CostBasis(self,x):
        self._CostBasis = x
        
    @property
    def ExecDate(self):
        return self._ExecDate
    @ExecDate.setter
    def ExecDate(self,x):
        self._ExecDate = x
    
    @property
    def Status(self):
        return self._status
    @Status.setter
    def Status(self,x):
        self._status = x
        
    @property
    def PurchasedDate(self):
        return self._purchasedDate
    
    @PurchasedDate.setter
    def PurchasedDate(self,x):
        self._purchasedDate = x

class Trade:
    def __init__(self):
        #update user_portfolio data in csv, we can still do vm test file
        self.id = 0
        

    #Enter trade order, return status, exec price, cost basis, save order history
    #cost basis according to the units (not the full original units)
    #PL = difference of Amount and cost basis
    def OrderEntry(self,Action,Symbol,Units,CostBasis,PurchasedDate):
        
        
        #pretent to trade order and save the history
        
        
        #long buy: unit > 0, amount < 0, cost basis = 0, exec date = now, purchased date = ""
        #long sell: unit < 0, amount > 0, cost basis = (sell units/full units) * full cost basis , exec date = now, purchased date = original long exec date
        #   full units > 0 & full cost basis < 0 & cost basis >0
        #Short sell: unit < 0, amount < 0, cost basis = 0, exec date = now, purchased date = ""
        #Cover buy: unit > 0, amount > 0, cost basis = (buy units/full units) * full cost basis, exec date = now, purchased date = original short exec date
        #   full units < 0 & full cost basis < 0 & cost basis > 0
        
        #full cost basis is previous amount
        
        quote = self.GetQuote(Symbol)
        order = Order()
        order.Symbol = Symbol
        order.Action = Action
        order.Units = Units
        order.PurchasedDate = PurchasedDate        
        
        if Action == "BUY":
            
            if quote.Ask == 0:
                order.ExecPx = quote.Close
            else:
                order.ExecPx = quote.Ask
            
            order.Amount = -1* order.ExecPx *  order.Units
        
        if Action == "SELL":

            if quote.Bid == 0:
                order.ExecPx = quote.Close
            else:
                order.ExecPx = quote.Bid
            
            order.Amount = -1* order.ExecPx *  order.Units
        
        
        if Action == "SELL_TO_OPEN":

            if quote.Bid == 0:
                order.ExecPx = quote.Close
            else:
                order.ExecPx = quote.Bid
            
            order.Amount = order.ExecPx *  order.Units
        
        
        if Action == "BUY_TO_CLOSE":
            if quote.Ask == 0:
                order.ExecPx = quote.Close
            else:
                order.ExecPx = quote.Ask
            
            order.Amount = order.ExecPx *  order.Units
        
        
        #buy/short sell have cost basis = 0, sell/cover buy have cost basis
        #value from variable
        order.CostBasis = float(CostBasis) 
        
        
        
        order.ExecDate = str(datetime.datetime.now())
        
        
        order.Status = "Y"
        
        f = open("OrderHistory.csv","a+")
        
        #Action,Symbol,Units,Amount,ExecPx,ExecDate,CostBasis
        f.write(order.Action + "," + order.Symbol + "," + str(order.Units) + "," + str(order.Amount) + "," + str(order.ExecPx) + "," + order.ExecDate + "," + str(order.CostBasis) + "," + PurchasedDate + "\n")
        
        f.close()
        
        return order
    
    
    
    
    def GetQuoteTest(self):
        return self.GetQuote('AAPL')
    
    def GetQuote(self,symbol):
        
        
        BidPx = -1
        AskPx = -1
        OpenPx = -1
        ClosePx = -1
        
        #create url with symbol
        url = 'https://finance.yahoo.com/quote/' + symbol + '/?p=' + symbol
        
        #query page
        response = get(url)
        
        #convert content page to soup object
        soup = BeautifulSoup(response.text, "lxml")
    
        summary_value = ""
    
        #get content with tag id = "quote-summary"
        if soup.find(id="quote-summary"):
            summary_value = soup.find(id="quote-summary").get_text()    
    
        else: #code stop here if id="quote-summary" is not found
            error_q = Quote(symbol,'N',BidPx, AskPx, OpenPx, ClosePx)
            return error_q 
    
        #bid price regular expression
        regex = r'(Bid)[,0-9]*(.)[0-9]*'
    
        #if bid price pattern found
        if re.search(regex,summary_value):
            #get the text of Bid price = Bidxx.xx
            match = re.search(regex,summary_value)
            #extract price and convert to float
            
            BidPx = float(match.group(0).replace('Bid','').replace(',',''))
    
        #ask price regular expression
        regex = r'(Ask)[,0-9]*(.)[0-9]*'
    
        #if bid price pattern found
        if re.search(regex,summary_value):
            #get the text of Bid price = Askxx.xx
            match = re.search(regex,summary_value)
            #extract price and convert to float
            AskPx = float(match.group(0).replace('Ask','').replace(',',''))
    
        #Open price regular expression
        regex = r'(Open)[,0-9]*(.)[0-9]*'
    
        #if Open price pattern found
        if re.search(regex,summary_value):
            #get the text of Open price = Openxx.xx
            match = re.search(regex,summary_value)
            #extract price and convert to float
            OpenPx = float(match.group(0).replace('Open','').replace(',',''))
        
        #Close price regular expression
        regex = r'(Close)[,0-9]*(.)[0-9]*'
    
        #if Close price pattern found
        if re.search(regex,summary_value):
            #get the text of Close price = Closexx.xx
            match = re.search(regex,summary_value)
            #extract price and convert to float
            ClosePx = float(match.group(0).replace('Close','').replace(',',''))
        
    
        #return quote with status = 'N' if fail to retreive price
        if (OpenPx > 0 and ClosePx > 0):        
            q = Quote(symbol,'Y',BidPx, AskPx, OpenPx, ClosePx)
            return q
        else:
            q = Quote(symbol,'N',BidPx, AskPx, OpenPx, ClosePx)
            return q
    
