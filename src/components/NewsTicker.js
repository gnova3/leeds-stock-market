import React, { useState, useEffect } from 'react';

const NewsTicker = ({ news }) => {
  const [currentNewsIndex, setCurrentNewsIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentNewsIndex(prev => (prev + 1) % news.length);
    }, 5000);
    return () => clearInterval(interval);
  }, [news.length]);

  return (
    <div className="bg-blue-900 text-white p-2 text-center">
      <p className="font-medium">{news[currentNewsIndex]}</p>
    </div>
  );
};

export default NewsTicker;