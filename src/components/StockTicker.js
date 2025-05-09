import React from 'react';

const StockTicker = ({ stocks }) => {
  return (
    <div className="bg-gray-100 p-2 overflow-hidden">
      <div className="flex space-x-8 animate-marquee whitespace-nowrap">
        {stocks.map(stock => (
          <div key={stock.id} className="flex items-center">
            <span className="font-bold">{stock.symbol}</span>
            <span className={`ml-2 ${stock.change >= 0 ? 'text-green-600' : 'text-red-600'}`}>
              {stock.price.toFixed(2)} ({stock.change >= 0 ? '+' : ''}{stock.change.toFixed(2)}%)
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default StockTicker;