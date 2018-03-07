# -*- coding: utf-8 -*-
"""
Created on Thu Mar 01 22:06:47 2018

@author: John
"""

import clsModelViews

def menuMain():
    menuOption = 0
    

    
    while menuOption != '9':
        print('\n'* 100)
        print('**Main Menu**')
        print('1. Trade')
        print('2. Show Blotter')
        print('3. Show P/L')
        print('9. Quit')
        menuOption = raw_input('Option :').strip()

        #Trade == 1
        if menuOption == '1':
            menuTrade()
        
        #Blotter == 2
        if menuOption == '2':
            menuShowBlotter()
        
        #P/L == 3
        if menuOption == '3':
            menuShowPL()
            
            
def menuTrade():
    subMenuOption = 0
    #create instance for trade model view
    objTradeMV = clsModelViews.TradeModelView()
    while subMenuOption != '9':
        print('\n'*100) #clear screen
        
        objTradeMV.DisplayCurrentHoldings()
        
        print('\n\n**Trade Action**')
        print('1. Buy / Buy To Close (FIFO)')
        print('2. Sell (FIFO) / Sell To Open')

        print('9. Quit')
        subMenuOption = raw_input('Option :').strip()
        
        #Action according to the option:
        if subMenuOption == '1':
            objTradeMV.TradeBuy() 
        if subMenuOption == '2':
            objTradeMV.TradeSell() 
                
        
def menuShowBlotter():
    subMenuOption = 0
    objBlotterMV = clsModelViews.BlotterModelView()
    while subMenuOption != '9':
        print('\n'*100)
        print('**Blotter**')
        objBlotterMV.ReadOrderHistory()
        print('9. Quit')
        subMenuOption = raw_input('Option :').strip()
        

def menuShowPL():
    subMenuOption = 0
    while subMenuOption != '9':
        print('\n'*100)
        print('**P/L**')
        print('9. Quit')
        subMenuOption = raw_input('Option :').strip()
        
    

def main():
    menuMain()

if __name__ == "__main__":
    main()
    