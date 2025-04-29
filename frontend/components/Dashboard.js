import React from 'react';
import Link from 'next/link';

function Dashboard() {
    return (
        <div>
            <h1>Trading Dashboard</h1>
            <div>
                <h2>Latest Price</h2>
            </div>
            <div>
                <h2>Current Holding</h2>
            </div>
            <div >
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
                <Link href="/signal-history">Go to Signal History</Link>
            </div>
        </div>
    );
}

export default Dashboard;