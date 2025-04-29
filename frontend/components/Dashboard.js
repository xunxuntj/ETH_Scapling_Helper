import React, { useState, useEffect } from 'react';
import Link from 'next/link';

function Dashboard() {
    const [latestPrice, setLatestPrice] = useState("Loading...");

    const fetchLatestPrice = async () => {
        try {
            const response = await fetch('/api/latest-price');
            const data = await response.json();
            setLatestPrice(data.price);
        } catch (error) {
            console.error("Error fetching latest price:", error);
            setLatestPrice("Error loading price");
        }
    };

    useEffect(() => {
        fetchLatestPrice();
    }, []);

    return (
        <div>
            <h1>Trading Dashboard</h1>
            <div>
                <h2>Latest Price</h2>
                <div>
                    <h3>ETH Price</h3>
                    <div>
                        {latestPrice}
                    </div>
                </div>
            </div>
            <div>
                <h2>Current Holding</h2>
                <div>
                  <h3>Position</h3>
                </div>
                <div>
                  <h3>Size</h3>
                </div>
                <div><h3>Entry Price</h3></div>
                <div><h3>Unrealized PnL</h3></div>
            </div>            
            <div>
                <h2>Signals</h2>
                <div>
                  <h3>MACD</h3>
                </div>
                <div>
                  <h3>RSI</h3>
                </div>
                <div>
                  <h3>Vegas Tunnel</h3>
                </div>
                <div>
                  <h3>EMA Double Cross</h3>
                </div>
                <div>
                  <h3>Candlestick Pattern</h3>
                </div>
                <div>
                    <h3>Fibonacci Support/Resistance</h3>
                </div>
            </div>            
            <div> 
                <h2>Indicators</h2>
                <div>
                  <h3>200 EMA</h3>
                </div>
                <div>
                  <h3>ATR</h3>
                </div>
            </div>
            <div>  
                <h2>Scoring System</h2>
                <h3>Current Score</h3>  
                <h4>Score breakdown:</h4>    
                <p>Details: The score is calculated based on MACD, RSI, Vegas Tunnel, EMA Double Cross, Candlestick Pattern, Fibonacci Support/Resistance.</p>   
            </div>
            <div>
                <h2>Capital Management</h2>
            </div>
            <div>
              <Link href="/signal-history">Go to Signal History</Link>
            </div>
        </div>
    );
}

export default Dashboard;