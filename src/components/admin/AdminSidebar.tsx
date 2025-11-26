"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { LayoutDashboard, Users, FileText, BarChart2, LogOut } from "lucide-react";

export default function AdminSidebar() {
  const pathname = usePathname();
  const router = useRouter();

  const handleLogout = () => {
    localStorage.removeItem("adminToken");
    router.push("/admin/login");
  };

  const isActive = (path: string) => pathname === path;

  return (
    <div className="w-64 bg-gray-900 text-white h-screen flex flex-col">
      <div className="p-6 border-b border-gray-800">
        <h1 className="text-xl font-bold">Admin Dashboard</h1>
      </div>
      
      <nav className="flex-1 p-4 space-y-2">
        <Link href="/admin" className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${isActive("/admin") ? "bg-blue-600" : "hover:bg-gray-800"}`}>
          <LayoutDashboard size={20} />
          <span>Overview</span>
        </Link>
        
        <Link href="/admin/sessions" className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${isActive("/admin/sessions") ? "bg-blue-600" : "hover:bg-gray-800"}`}>
          <Users size={20} />
          <span>Sessions</span>
        </Link>
        
        <Link href="/admin/documents" className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${isActive("/admin/documents") ? "bg-blue-600" : "hover:bg-gray-800"}`}>
          <FileText size={20} />
          <span>Documents</span>
        </Link>
        
        <Link href="/admin/analytics" className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${isActive("/admin/analytics") ? "bg-blue-600" : "hover:bg-gray-800"}`}>
          <BarChart2 size={20} />
          <span>Analytics</span>
        </Link>
      </nav>
      
      <div className="p-4 border-t border-gray-800">
        <button onClick={handleLogout} className="flex items-center space-x-3 px-4 py-3 rounded-lg hover:bg-red-600 text-gray-400 hover:text-white w-full transition-colors">
          <LogOut size={20} />
          <span>Logout</span>
        </button>
      </div>
    </div>
  );
}
