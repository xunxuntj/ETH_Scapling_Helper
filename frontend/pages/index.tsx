import React, { useState, useEffect } from 'react';
import Head from 'next/head';

export default function Home() {
  const [signals, setSignals] = useState<any>([]);
  const [autoAdjust, setAutoAdjust] = useState<boolean>(true);

  useEffect(() => {
    // Fetch signals from backend API
    const fetchSignals = async () => {
      try {
        const response = await fetch('/api/signals');
        const data = await response.json();
        setSignals(data);
      } catch (error) {
        console.error("Error fetching signals:", error);
      }
    };

    fetchSignals();
  }, []);

  const handleAutoAdjustToggle = () => {
    setAutoAdjust(!autoAdjust);
  };

  return (
    <div>
      <Head>
        <title>ETH Scalping Assistant</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="container mx-auto py-4">
        <h1 className="text-2xl font-bold mb-4">ETH Scalping Assistant Dashboard</h1>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {/* Key Metrics */}
          <div className="bg-white shadow-md rounded-md p-4">
            <h2 className="text-lg font-semibold mb-2">Key Metrics</h2>
            <p>Account Balance: $0.00</p>
            <p>Open Positions: 0</p>
            <p>Total Profit: $0.00</p>
          </div>

          {/* Current Signals */}
          <div className="bg-white shadow-md rounded-md p-4">
            <h2 className="text-lg font-semibold mb-2">Current Signals</h2>
            {signals ? (
              <p>{signals.message}</p>
            ) : (
              <p>Loading signals...</p>
            )}
          </div>

          {/* Position Information */}
          <div className="bg-white shadow-md rounded-md p-4">
            <h2 className="text-lg font-semibold mb-2">Position Information</h2>
            <p>Trading Pair: ETHUSDT</p>
            <p>Side: Long/Short</p>
            <p>Entry Price: $0.00</p>
          </div>
        </div>

        {/* Auto Adjust Toggle */}
        <div className="mt-4">
          <label className="inline-flex items-center">
            <input
              type="checkbox"
              className="form-checkbox h-5 w-5 text-blue-600"
              checked={autoAdjust}
              onChange={handleAutoAdjustToggle}
            />
            <span className="ml-2 text-gray-700">Auto Adjust Stop Loss/Take Profit</span>
          </label>
        </div>
      </main>
    </div>
  );
}
