import React, { useState } from 'react';

const StockCard = ({ stock, onBuy, onSell }) => {
  const [quantity, setQuantity] = useState(1);

  const handleQuantityChange = (e) => {
    const value = parseInt(e.target.value);
    if (!isNaN(value) && value > 0) {
      setQuantity(value);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow p-4">
      <div className="flex justify-between items-center mb-2">
        <h3 className="font-bold text-lg">{stock.name} ({stock.symbol})</h3>
        <span className={`text-lg font-semibold ${stock.change >= 0 ? 'text-green-600' : 'text-red-600'}`}>
          ${stock.price.toFixed(2)}
        </span>
      </div>
      <div className="flex justify-between text-sm text-gray-600 mb-4">
        <span>Change: {stock.change >= 0 ? '+' : ''}{stock.change.toFixed(2)}%</span>
      </div>
      <div className="flex space-x-2">
        <input
          type="number"
          min="1"
          value={quantity}
          onChange={handleQuantityChange}
          className="border rounded px-2 py-1 w-20"
        />
        <button
          onClick={() => onBuy(stock.id, quantity)}
          className="bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700"
        >
          Buy
        </button>
        <button
          onClick={() => onSell(stock.id, quantity)}
          className="bg-red-600 text-white px-3 py-1 rounded hover:bg-red-700"
        >
          Sell
        </button>
      </div>
    </div>
  );
};

export default StockCard;