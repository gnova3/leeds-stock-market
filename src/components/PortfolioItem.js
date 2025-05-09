import React from 'react';

const PortfolioItem = ({ item, currentPrices }) => {
  const currentPrice = currentPrices[item.stockId] || 0;
  const marketValue = item.quantity * currentPrice;
  const gainLoss = marketValue - (item.quantity * item.avgPrice);
  const gainLossPercent = ((gainLoss / (item.quantity * item.avgPrice)) * 100).toFixed(2);

  return (
    <tr className="border-b">
      <td className="py-2">{item.stockName}</td>
      <td className="py-2">{item.quantity}</td>
      <td className="py-2">${item.avgPrice.toFixed(2)}</td>
      <td className="py-2">${marketValue.toFixed(2)}</td>
      <td className={`py-2 ${gainLoss >= 0 ? 'text-green-600' : 'text-red-600'}`}>
        ${gainLoss.toFixed(2)} ({gainLossPercent}%)
      </td>
    </tr>
  );
};

export default PortfolioItem;