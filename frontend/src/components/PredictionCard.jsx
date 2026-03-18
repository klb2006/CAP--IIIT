import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { TrendingUp, AlertCircle } from 'lucide-react';
import { API_ENDPOINTS } from '../api/config';

const PredictionCard = ({ sensorData, isConnected }) => {
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handlePredict = async () => {
    if (!sensorData) {
      setError('No sensor data available');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const now = new Date();
      const minute = now.getMinutes();
      const hour = now.getHours();

      const response = await fetch(API_ENDPOINTS.PREDICT_WATER, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          distance: parseFloat(sensorData.distance) || 0,
          temperature: parseFloat(sensorData.temperature) || 0,
          water_percent: parseFloat(sensorData.waterPercentage) || 0,
          minute: minute,
          hour: hour,
          node_id: 'node-1',
        }),
      });

      const result = await response.json();

      if (response.ok && result.status === 'success') {
        setPrediction({
          value: result.predicted_water_percent,
          timestamp: new Date().toLocaleTimeString(),
        });
      } else {
        setError(result.message || 'Prediction failed');
      }
    } catch (err) {
      setError('Unable to get prediction');
      console.error('Prediction error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white dark:bg-slate-800 rounded-lg border border-slate-200 dark:border-slate-700 p-6 shadow-sm"
    >
      <div className="flex items-center gap-3 mb-4">
        <TrendingUp className="w-6 h-6 text-purple-600 dark:text-purple-400" />
        <h3 className="text-lg font-semibold text-slate-900 dark:text-white">
          ML Water Level Prediction
        </h3>
      </div>

      {prediction ? (
        <motion.div
          initial={{ scale: 0.95 }}
          animate={{ scale: 1 }}
          className="mb-4 p-4 bg-purple-50 dark:bg-purple-900/30 rounded-lg border border-purple-200 dark:border-purple-700"
        >
          <div className="text-center">
            <div className="text-4xl font-bold text-purple-600 dark:text-purple-400">
              {prediction.value.toFixed(1)}%
            </div>
            <p className="text-sm text-slate-600 dark:text-slate-400 mt-2">
              Predicted water level (Next cycle)
            </p>
            <p className="text-xs text-slate-500 dark:text-slate-500 mt-1">
              Predicted at: {prediction.timestamp}
            </p>
          </div>
          
          <div className="mt-3 p-2 bg-yellow-50 dark:bg-yellow-900/20 rounded border border-yellow-200 dark:border-yellow-700">
            <p className="text-xs text-yellow-700 dark:text-yellow-300">
              ⚠️ <strong>Note:</strong> If water level stays the same for 2+ minutes, the motor might not be running. In that case, the prediction may be inaccurate because the model expects water movement.
            </p>
          </div>
        </motion.div>
      ) : null}

      {error && (
        <div className="mb-4 p-3 bg-red-50 dark:bg-red-900/30 rounded-lg border border-red-200 dark:border-red-700 flex gap-2">
          <AlertCircle className="w-5 h-5 text-red-600 dark:text-red-400 flex-shrink-0" />
          <p className="text-sm text-red-700 dark:text-red-300">{error}</p>
        </div>
      )}

      <button
        onClick={handlePredict}
        disabled={loading || !isConnected}
        className={`w-full py-2 px-4 rounded-lg font-medium transition-all ${
          loading || !isConnected
            ? 'bg-slate-300 dark:bg-slate-600 text-slate-600 dark:text-slate-400 cursor-not-allowed'
            : 'bg-purple-600 hover:bg-purple-700 text-white shadow-sm hover:shadow-md'
        }`}
      >
        {loading ? (
          <span className="flex items-center justify-center gap-2">
            <span className="animate-spin">⚙️</span> Predicting...
          </span>
        ) : (
          'Get Prediction Now'
        )}
      </button>

      <p className="text-xs text-slate-500 dark:text-slate-400 mt-3">
        🤖 LSTM model predicts next water level based on: distance, temperature, current water %, time of day. Accuracy depends on active motor/system changes.
      </p>
    </motion.div>
  );
};

export default PredictionCard;
