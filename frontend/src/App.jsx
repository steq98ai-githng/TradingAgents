import React, { useEffect, useRef, useState } from 'react';
import { createChart } from 'lightweight-charts';
import { Activity, Shield, ShoppingCart, AlertCircle } from 'lucide-react';

function App() {
  const chartContainerRef = useRef();
  const chart = useRef();
  const candlestickSeries = useRef();
  const [candles, setCandles] = useState([]);
  const [riskStatus, setRiskStatus] = useState({ dailyPnL: 0, dll: 1000, mll: 2000 });
  const [signals, setSignals] = useState([]);

  useEffect(() => {
    chart.current = createChart(chartContainerRef.current, {
      width: chartContainerRef.current.clientWidth,
      height: 400,
      layout: { backgroundColor: '#111827', textColor: '#d1d5db' },
      grid: { vertLines: { color: '#374151' }, horzLines: { color: '#374151' } },
    });
    candlestickSeries.current = chart.current.addCandlestickSeries({
      upColor: '#10b981', downColor: '#ef4444', borderVisible: false,
      wickUpColor: '#10b981', wickDownColor: '#ef4444',
    });

    // Mock data for initial load
    const initialData = [
      { time: '2023-05-20', open: 18500, high: 18550, low: 18480, close: 18520 },
      { time: '2023-05-21', open: 18520, high: 18580, low: 18510, close: 18560 },
    ];
    candlestickSeries.current.setData(initialData);

    const handleResize = () => {
      chart.current.applyOptions({ width: chartContainerRef.current.clientWidth });
    };
    window.addEventListener('resize', handleResize);

    // WebSocket mock for demo
    const interval = setInterval(() => {
        const lastClose = initialData[initialData.length-1].close;
        const nextClose = lastClose + (Math.random() - 0.5) * 10;
        const newCandle = {
            time: Math.floor(Date.now() / 1000),
            open: lastClose,
            high: Math.max(lastClose, nextClose) + 2,
            low: Math.min(lastClose, nextClose) - 2,
            close: nextClose
        };
        candlestickSeries.current.update(newCandle);
    }, 2000);

    return () => {
      window.removeEventListener('resize', handleResize);
      chart.current.remove();
      clearInterval(interval);
    };
  }, []);

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 p-4 font-sans">
      <header className="flex justify-between items-center mb-6 border-b border-gray-800 pb-4">
        <h1 className="text-2xl font-bold text-blue-400">Futures Trader Support System <span className="text-sm font-normal text-gray-500">(MNQ)</span></h1>
        <div className="flex gap-4">
          <div className="flex items-center gap-2 bg-gray-800 px-3 py-1 rounded">
            <Shield size={18} className="text-green-400" />
            <span>Topstep 50K</span>
          </div>
        </div>
      </header>

      <div className="grid grid-cols-12 gap-4">
        {/* Main Chart */}
        <div className="col-span-12 lg:col-span-8 bg-gray-800 p-4 rounded-lg shadow-lg">
          <div className="flex items-center gap-2 mb-4">
            <Activity size={20} className="text-blue-400" />
            <h2 className="text-lg font-semibold">MNQ 1m Chart</h2>
          </div>
          <div ref={chartContainerRef} className="w-full" />
        </div>

        {/* Side Panel */}
        <div className="col-span-12 lg:col-span-4 flex flex-col gap-4">
          {/* Risk Panel */}
          <div className="bg-gray-800 p-4 rounded-lg shadow-lg border-l-4 border-green-500">
            <h3 className="text-md font-semibold mb-3 flex items-center gap-2">
              <Shield size={18} /> Risk Management
            </h3>
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span>Daily PnL:</span>
                <span className="text-green-400 font-mono">${riskStatus.dailyPnL.toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span>Daily Loss Limit:</span>
                <span className="text-red-400">-${riskStatus.dll}</span>
              </div>
              <div className="w-full bg-gray-700 h-2 rounded-full overflow-hidden">
                <div className="bg-green-500 h-full" style={{width: '100%'}}></div>
              </div>
            </div>
          </div>

          {/* Signals / Manual Order */}
          <div className="bg-gray-800 p-4 rounded-lg shadow-lg flex-grow">
            <h3 className="text-md font-semibold mb-3 flex items-center gap-2">
              <ShoppingCart size={18} /> Trade Signals
            </h3>
            <div className="space-y-3">
              <div className="p-3 bg-gray-700 rounded border border-blue-500">
                <div className="flex justify-between items-center mb-2">
                  <span className="bg-blue-600 text-xs px-2 py-0.5 rounded font-bold uppercase">Buy Signal</span>
                  <span className="text-xs text-gray-400">2 mins ago</span>
                </div>
                <p className="text-sm mb-3">Gemini: Bullish divergence on RSI-5. Potential bounce from 18520 level.</p>
                <div className="flex gap-2">
                  <button className="flex-1 bg-green-600 hover:bg-green-500 py-2 rounded font-bold text-sm transition">Confirm Buy</button>
                  <button className="flex-1 bg-gray-600 hover:bg-gray-500 py-2 rounded font-bold text-sm transition">Dismiss</button>
                </div>
              </div>
            </div>
          </div>

          {/* Notifications */}
          <div className="bg-gray-800 p-4 rounded-lg shadow-lg">
             <h3 className="text-md font-semibold mb-2 flex items-center gap-2">
              <AlertCircle size={18} /> Notifications
            </h3>
            <div className="text-xs text-gray-400 space-y-1">
               <p>• [10:30] Webhook: TV RSI Crosses Above 30</p>
               <p>• [10:25] Risk: Daily PnL at +$250</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
