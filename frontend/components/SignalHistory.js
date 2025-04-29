import Link from 'next/link';

function SignalHistory() {
  return (
    <div>
      <h2>Signal History</h2>
      <div> {/* Main table container */}
        <div> {/* Header Row */}
          <div>Timestamp</div>          
          <div>Signal Name</div>          
          <div>Signal Value</div>          
          <div>Score</div>
          <div>Open Price</div>
          <div>Close Price</div>
          <div>Result</div>          
        </div>
        <div> {/* Example Row */}
          <div>2024-10-27 10:00:00</div>
          <div>MACD</div>
          <div>Bullish</div>
          <div>8</div>
          <div>1500</div>
          <div>1550</div>
          <div>Success</div>
          
        </div>
         {/* Add more rows here as needed */}
      
      <Link href="/">Go to Dashboard</Link>
      </div>
    </div>
  );
}

export default SignalHistory;