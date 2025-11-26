"use client";

import { useEffect, useState } from "react";
import { adminApi } from "@/lib/adminApi";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export default function AnalyticsPage() {
  const [analytics, setAnalytics] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAnalytics();
  }, []);

  const loadAnalytics = async () => {
    try {
      const data = await adminApi.getAnalytics(7);
      setAnalytics(data);
    } catch (error) {
      console.error("Failed to load analytics");
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading analytics...</div>;

  // Format data for Recharts
  const chartData = analytics?.daily_stats?.map((stat: any) => ({
    date: new Date(stat.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
    messages: stat.total_messages || 0,
    documents: stat.total_documents || 0
  })) || [];

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Analytics (Last 7 Days)</h1>
      
      <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 mb-8 h-96">
        <h3 className="text-lg font-semibold mb-4">Activity Overview</h3>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={chartData}
            margin={{
              top: 5,
              right: 30,
              left: 20,
              bottom: 5,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="messages" fill="#8884d8" name="Messages" />
            <Bar dataKey="documents" fill="#82ca9d" name="Documents" />
          </BarChart>
        </ResponsiveContainer>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 text-center">
            <h3 className="text-gray-500 text-sm font-medium uppercase">Total Messages</h3>
            <p className="text-3xl font-bold text-gray-900 mt-2">{analytics?.total_messages || 0}</p>
        </div>
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 text-center">
            <h3 className="text-gray-500 text-sm font-medium uppercase">Total Documents</h3>
            <p className="text-3xl font-bold text-gray-900 mt-2">{analytics?.total_documents || 0}</p>
        </div>
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 text-center">
            <h3 className="text-gray-500 text-sm font-medium uppercase">Total Sessions</h3>
            <p className="text-3xl font-bold text-gray-900 mt-2">{analytics?.total_sessions || 0}</p>
        </div>
      </div>
    </div>
  );
}
