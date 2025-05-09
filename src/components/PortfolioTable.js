import React from 'react';
import PortfolioItem from './PortfolioItem';

const PortfolioTable = ({ portfolio, currentPrices }) => {
  return (
    <div className="bg-white rounded-lg shadow overflow-hidden">
      <table className="min-w-full">
        <thead className="bg-gray-100">
          <tr>
            <th className="px-4 py-2 text-left">Stock</th>
            <th className="px-4 py-2 text-left">Qty</th>
            <th className="px-4 py-2 text-left">Avg Price</th>
            <th className="px-4 py-2 text-left">Market Value</th>
            <th className="px-4 py-2 text-left">Gain/Loss</th>
          </tr>
        </thead>
        <tbody>
          {portfolio.map(item => (
            <PortfolioItem 
              key={item.stockId} 
              item={item} 
              currentPrices={currentPrices} 
            />
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default PortfolioTable;