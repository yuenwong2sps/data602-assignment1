# -*- coding: utf-8 -*-
"""
Created on Sat Mar 03 18:44:56 2018

@author: John
"""

#Portfolio     
#from portfolio.csv
#portfolio, cash, security, price, quantity
#read(), write()


import csv
import clsTrade

portfolioFile = "Portfolio.csv"


class Position:
    def __init__(self):
        self.Symbol = ""
        self.Units = "" #positive for long, negative for short
        self.PurchasedPx = 0
        self.PurchasedDate = 1900/01/01
    
    @property
    def Symbol(self):
        return self._Symbol
    @Symbol.setter
    def Symbol(self, x):
        self._Symbol = x
    
    @property
    def Units(self):
        return self._Units
    @Units.setter
    def Units(self,x):
        self._Units = x
    
    @property    
    def PurchasedPx(self):
        return self._PurchasedPx
    @PurchasedPx.setter
    def PurchasedPx(self,x):
        self._PurchasedPx = x
    
    @property    
    def PurchasedDate(self):
        return self._PurchasedDate
    @PurchasedDate.setter
    def PurchasedDate(self,x):
        self._PurchasedDate = x
    
    @property
    def CostBasis(self):
        return self._CostBasis
    @CostBasis.setter
    def CostBasis(self,x):
        self._CostBasis = x
        

class Portfolio:
    def __init__(self):
        self.Cash = 0
        self.Positions = []
        self.ReadHoldings()
    
    def ReadHoldings(self):
        #read latest portfolio
        del self.Positions [:]
        
        f = open(portfolioFile,'rb')
        csvReader = csv.reader(f)
        for row in csvReader:
            if len(row) > 3:
                if(row[0]!='Symbol'): #skip the header line
                    #create object to store position
                    p = Position()
                
                    p.Symbol = row[0]
                    p.Units = float(row[1])
                    p.PurchasedPx = float(row[2])
                    p.PurchasedDate = row[3]
                    p.CostBasis = row[4]
                    
                    if p.Symbol == "CASH-1":  #for cash, keep in cash variable
                        self.Cash = p.Units
                    else:
                        self.Positions.append(p) #for security, add to holdings list
                        
                
                
        f.close()
    

    #Update the changes to the csv file (just like saving data in database)

    def CommitChangesHoldings(self):
        f = open(portfolioFile,"w+")
        f.write("Symbol,Units,PurchasedPx,PurchasedDate,CostBasis\n")
        f.write("CASH-1," + str(self.Cash) + ",1,1/1/9999,0\n")
        for pos in self.Positions:
            f.write(pos.Symbol + "," + str(pos.Units) + "," + str(pos.PurchasedPx) + "," + pos.PurchasedDate + "," + str(pos.CostBasis) +  "\n")
        f.close()
        


        
    #if it is buy, add position with symbol and date
    #if it is sell, sell with symbol with purchased date (taxlot)
    #read all orders, update holdings, write back to file
    #update current cash -= trade amount 
    #Assume given "order" is executed with sufficient cash
    def UpdatePosition(self, order):
        self.ReadHoldings()
        
        IsChanged = False 
        
        #Long action
        if order.Action == "SELL":
            for p in self.Positions:
                if p.PurchasedDate == order.PurchasedDate and p.Symbol == order.Symbol:
                    if p.Units == order.Units: #sell the whole lot
                        p.Units = 0
                        p.CostBasis = 0
                    else:
                        adj_costBasis = 1 - (order.Units/p.Units)*p.CostBasis #update cost basis due to partail sell
                        p.Units = p.Units - order.Units
                        p.CostBasis = adj_costBasis
                    #after sell, add cash
                    self.Cash = self.Cash + order.Amount
                    
                    IsChanged = True #flip the sign to the change
                    
          
            
        #Long action
        if order.Action == "BUY":
            
            
            #append new traded ordered to current holdings
            p = Position()
            p.Symbol = order.Symbol
            p.Units = order.Units
            p.PurchasedPx = order.ExecPx
            p.PurchasedDate = order.ExecDate
            p.CostBasis = order.Amount
            
            self.Cash = self.Cash - order.Amount
            self.Positions.append(p)
            IsChanged = True #flip the sign to the change

        


        #Short action    
        if order.Action == "SELL_TO_OPEN":
            print("Sell to open")
            
        #Short action
        if order.Action == "BUY_TO_CLOSE":    
            print("buy to close")
            
            
        #if there is any change, update    
        if IsChanged == True:
            self.CommitChangesHoldings()
            
        
    #check postion before selling
    #shorting create new position with date, it is different than selling 
    def IsPositionExist(self,order): #sum of the order units
        isExist = False
        for p in self.Positions:
            if p.Symbol == order.Symbol and p.Units == order.Units:
                isExist = True
                break
            
        return isExist
    
    
    def GetPositions(self): #memory only
        return self.Positions
    
    def GetPositionsBySym(self,sym):
        sym_pos = []
        for p in self.Positions:
            if p.Symbol == sym:
                sym_pos.append(p)
        
        if not sym_pos: #is empty list
            dummyP = Position()
            return dummyP
        else:
            return sym_pos
    
    def GetCash(self): #memory only
        return self.Cash

    def GetRows(self):
        
        return len(self.Positions)





