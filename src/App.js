import React, { useState, useEffect } from 'react';
import stocksData from './mock/stocks';
import newsData from './mock/news';
import StockTicker from './components/StockTicker';
import NewsTicker from './components/NewsTicker';
import StockCard from './components/StockCard';
import PortfolioTable from './components/PortfolioTable';

const App = () => {
  const [stocks, setStocks] = useState(stocksData);
  const [portfolio, setPortfolio] = useState([]);
  const [balance, setBalance] = useState(10000);
  const [currentPrices, setCurrentPrices] = useState({});

  // Initialize currentPrices once on mount
useEffect(() => {
  const initialPrices = {};
  stocksData.forEach(stock => {
    initialPrices[stock.id] = stock.price;
  });
  setCurrentPrices(initialPrices);
}, []);

// Periodically update stocks and currentPrices
  useEffect(() => {
    const interval = setInterval(() => {
      setStocks(prevStocks => {
        const updatedStocks = prevStocks.map(stock => {
          const change = (Math.random() * 4 - 2);
          const newPrice = stock.price * (1 + change / 100);
          const newChange = ((newPrice - stock.history[0]) / stock.history[0]) * 100;

          return {
            ...stock,
            price: parseFloat(newPrice.toFixed(2)),
            change: parseFloat(newChange.toFixed(2)),
            history: [...stock.history, newPrice].slice(-10),
          };
        });

        // update currentPrices as well
        const newPrices = {};
        updatedStocks.forEach(stock => {
          newPrices[stock.id] = stock.price;
        });
        setCurrentPrices(newPrices);

        return updatedStocks;
      });
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  const handleBuy = (stockId, quantity) => {
    const stock = stocks.find(s => s.id === stockId);
    const totalCost = stock.price * quantity;

    if (balance >= totalCost) {
      setBalance(prev => prev - totalCost);
      
      setPortfolio(prevPortfolio => {
        const existingItem = prevPortfolio.find(item => item.stockId === stockId);
        if (existingItem) {
          const newQuantity = existingItem.quantity + quantity;
          const newAvgPrice = ((existingItem.quantity * existingItem.avgPrice) + totalCost) / newQuantity;
          return prevPortfolio.map(item => 
            item.stockId === stockId 
              ? { ...item, quantity: newQuantity, avgPrice: newAvgPrice }
              : item
          );
        } else {
          return [...prevPortfolio, {
            stockId,
            stockName: stock.name,
            quantity,
            avgPrice: stock.price
          }];
        }
      });
    } else {
      alert("Insufficient funds!");
    }
  };

  const handleSell = (stockId, quantity) => {
    const portfolioItem = portfolio.find(item => item.stockId === stockId);
    if (!portfolioItem || portfolioItem.quantity < quantity) {
      alert("Not enough shares to sell!");
      return;
    }

    const stock = stocks.find(s => s.id === stockId);
    const totalValue = stock.price * quantity;
    setBalance(prev => prev + totalValue);

    setPortfolio(prevPortfolio => {
      if (portfolioItem.quantity === quantity) {
        return prevPortfolio.filter(item => item.stockId !== stockId);
      } else {
        return prevPortfolio.map(item => 
          item.stockId === stockId 
            ? { ...item, quantity: item.quantity - quantity }
            : item
        );
      }
    });
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-blue-800 text-white p-4">
        <h1 className="text-2xl font-bold text-center">Leeds Stock Market</h1>
      </header>

      <NewsTicker news={newsData} />

      <div className="container mx-auto p-4">
        <StockTicker stocks={stocks} />

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-6">
          <div className="md:col-span-2">
            <h2 className="text-xl font-semibold mb-4">Available Stocks</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {stocks.map(stock => (
                <StockCard
                  key={stock.id}
                  stock={stock}
                  onBuy={handleBuy}
                  onSell={handleSell}
                />
              ))}
            </div>
          </div>

          <div>
            <div className="bg-white rounded-lg shadow p-4 mb-6">
              <h2 className="text-xl font-semibold mb-2">Account Summary</h2>
              <p className="text-lg">Balance: <span className="font-bold">${balance.toFixed(2)}</span></p>
            </div>

            <h2 className="text-xl font-semibold mb-4">Your Portfolio</h2>
            {portfolio.length > 0 ? (
              <PortfolioTable portfolio={portfolio} currentPrices={currentPrices} />
            ) : (
              <p className="text-gray-500">Your portfolio is empty. Buy some stocks!</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;

// DONE