"use client";

import { useEffect, useState } from "react";
import StatCard from "@/components/admin/StatCard";
import { Users, FileText, MessageSquare, HardDrive } from "lucide-react";
import { adminApi } from "@/lib/adminApi";
import { useRouter } from "next/navigation";

export default function AdminDashboard() {
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const data = await adminApi.getStats();
      setStats(data);
    } catch (error) {
      console.error("Failed to load stats:", error);
      // If 401, redirect to login
      // router.push("/admin/login");
    } finally {
      setLoading(false);
    }
  };

  const handleCleanup = async () => {
    if (!confirm("Are you sure you want to run manual cleanup?")) return;
    try {
      await adminApi.runCleanup();
      alert("Cleanup started successfully");
    } catch (error) {
      alert("Failed to start cleanup");
    }
  };

  if (loading) return <div>Loading stats...</div>;
  if (!stats) return <div>Error loading stats</div>;

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Dashboard Overview</h1>
          <p className="text-gray-500">Welcome back, Admin</p>
        </div>
        <button
          onClick={handleCleanup}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          Run Cleanup
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard
          title="Total Sessions"
          value={stats.total_sessions}
          icon={Users}
          color="blue"
        />
        <StatCard
          title="Total Documents"
          value={stats.total_documents}
          icon={FileText}
          color="green"
        />
        <StatCard
          title="Total Messages"
          value={stats.total_messages}
          icon={MessageSquare}
          color="purple"
        />
        <StatCard
          title="Storage Used"
          value="450 MB" // Placeholder as API needs update for real storage
          icon={HardDrive}
          color="orange"
        />
      </div>

      {/* Recent Activity or Charts could go here */}
      <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
        <h2 className="text-lg font-semibold mb-4">System Status</h2>
        <div className="space-y-4">
          <div className="flex justify-between items-center p-4 bg-gray-50 rounded-lg">
            <div>
              <p className="font-medium">Background Scheduler</p>
              <p className="text-sm text-gray-500">Running hourly cleanup tasks</p>
            </div>
            <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm font-medium">
              Active
            </span>
          </div>
          <div className="flex justify-between items-center p-4 bg-gray-50 rounded-lg">
            <div>
              <p className="font-medium">Vector Database</p>
              <p className="text-sm text-gray-500">Qdrant Cloud Connection</p>
            </div>
            <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm font-medium">
              Connected
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
