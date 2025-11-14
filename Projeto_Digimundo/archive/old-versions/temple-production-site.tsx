import React, { useState, useEffect, useRef } from 'react';
import { 
  Calendar, Film, Users, FileText, Bell, Eye, Lock, Upload, MessageCircle, 
  Camera, Clapperboard, Video, FolderOpen, Clock, CheckCircle, AlertCircle,
  ChevronLeft, ChevronRight, Plus, Grid, List, Filter, Search, Download,
  Edit, Trash2, Share2, Cloud, CloudRain, Sun, Wind, MapPin, Phone,
  Mail, DollarSign, TrendingUp, BarChart2, Image, Layers, Move, Menu,
  X, ArrowRight, ExternalLink, Settings, HelpCircle, LogOut, Home
} from 'lucide-react';

// CSS Variables do StudioBinder
const cssVariables = `
  :root {
    --btn-primary-color: #5d78ff;
    --btn-primary-color-RGB: 93, 120, 255;
    --btn-primary-color-hover: #384ad7;
    --btn-primary-color-hover-RGB: 56, 74, 215;
    --btn-accent-color: #FA1870;
    --btn-accent-color-RGB: 250, 24, 112;
    --btn-accent-color-hover: #fd1361;
    --btn-accent-color-hover-RGB: 253, 19, 97;
    --link-accent-color: #FA1870;
    --link-accent-color-RGB: 250, 24, 112;
    --link-accent-color-hover: #fd1361;
    --link-accent-color-hover-RGB: 253, 19, 97;
    --link-color: #5d78ff;
    --link-color-RGB: 93, 120, 255;
    --link-color-hover: #384ad7;
    --link-color-hover-RGB: 56, 74, 215;
    --link-nav-bar-color: #A2A3B7;
    --link-nav-bar-color-RGB: 162, 163, 183;
    --link-nav-bar-color-hover: #fff;
    --link-nav-bar-color-hover-RGB: 255, 255, 255;
    --sub-menu-logged-in-bg-color: #1D1E2C;
    --sub-menu-logged-in-bg-color-RGB: 29, 30, 44;
    --sub-menu-logged-in-bg-color-hover: #1b1b28;
    --sub-menu-logged-in-bg-color-hover-RGB: 27, 27, 40;
    --nav-logged-out-bg-color: rgba(255,255,255,0.6);
    --nav-logged-out-bg-color-RGB: 255, 255, 255;
    --link-nav-logged-out-color: #41474d;
    --link-nav-logged-out-color-RGB: 65, 71, 77;
    --link-nav-logged-out-color-hover: #5d78ff;
    --link-nav-logged-out-color-hover-RGB: 93, 120, 255;
    --nav-logged-in-bg-color: #1D1E2C;
    --nav-logged-in-bg-color-RGB: 29, 30, 44;
    --nav-logged-in-bg-color-hover: #1b1b28;
    --nav-logged-in-bg-color-hover-RGB: 27, 27, 40;
    --link-sidebar-color: #5d78ff;
    --link-sidebar-color-RGB: 93, 120, 255;
    --link-sidebar-color-hover: #384ad7;
    --link-sidebar-color-hover-RGB: 56, 74, 215;
    --checkbox-color: #5d78ff;
    --checkbox-color-RGB: 93, 120, 255;
    --input-border-color: #D8E0E6;
    --input-border-color-RGB: 216, 224, 230;
    --font-size: 13px;
    --line-height: 18px;
    --body-color: #1B1C21;
    --input-height-base: 36px;
  }
  
  * {
    box-sizing: border-box;
  }
  
  body {
    font-size: var(--font-size);
    line-height: var(--line-height);
    color: var(--body-color);
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  }
`;

// Loading Animation Component (Simulating Lottie)
const LoadingSpinner = () => {
  return (
    <div className="app-loading" style={{
      position: 'relative',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      height: '100%',
      backgroundColor: '#f8f9fa'
    }}>
      <div className="spinner" style={{
        height: '74px',
        width: '74px',
        position: 'absolute',
        top: 0,
        bottom: 0,
        left: 0,
        right: 0,
        margin: 'auto'
      }}>
        <div style={{
          width: '74px',
          height: '74px',
          borderRadius: '50%',
          border: '3px solid transparent',
          borderTopColor: 'var(--btn-primary-color)',
          animation: 'spin 1s linear infinite'
        }}></div>
        <div style={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          width: '20px',
          height: '20px',
          backgroundColor: 'var(--btn-primary-color)',
          borderRadius: '50%',
          animation: 'bounce 1s ease-in-out infinite'
        }}></div>
      </div>
    </div>
  );
};

const StudioBinderClone = () => {
  const [currentUser, setCurrentUser] = useState(null);
  const [activeSection, setActiveSection] = useState('dashboard');
  const [loading, setLoading] = useState(true);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [notifications, setNotifications] = useState([]);
  const [showUserMenu, setShowUserMenu] = useState(false);

  // Simulate loading
  useEffect(() => {
    const timer = setTimeout(() => setLoading(false), 1500);
    return () => clearTimeout(timer);
  }, []);

  // Users data
  const users = {
    diretor: { 
      name: "Sofia Luz", 
      role: "Director", 
      department: "Creative", 
      avatar: "SL",
      email: "sofia@studiobinder.com",
      projects: 3
    },
    produtor: { 
      name: "Marcus Terra", 
      role: "Producer", 
      department: "Production", 
      avatar: "MT",
      email: "marcus@studiobinder.com",
      projects: 5
    },
    foto: { 
      name: "Luna Sombra", 
      role: "DP", 
      department: "Photography", 
      avatar: "LS",
      email: "luna@studiobinder.com",
      projects: 2
    },
    ator: { 
      name: "Rio Vento", 
      role: "Talent", 
      department: "Cast", 
      avatar: "RV",
      email: "rio@studiobinder.com",
      projects: 1
    }
  };

  // Login Component with StudioBinder styling
  const Login = () => {
    return (
      <div className="min-h-screen flex items-center justify-center" style={{
        backgroundColor: '#f8f9fa',
        backgroundImage: 'linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)'
      }}>
        <style dangerouslySetInnerHTML={{ __html: cssVariables }} />
        <style dangerouslySetInnerHTML={{ __html: `
          @keyframes spin {
            to { transform: rotate(360deg); }
          }
          @keyframes bounce {
            0%, 100% { transform: translate(-50%, -50%) scale(1); }
            50% { transform: translate(-50%, -50%) scale(1.2); }
          }
          .user-card {
            transition: all 0.2s ease;
            cursor: pointer;
          }
          .user-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
          }
          .sb-btn-primary {
            background-color: var(--btn-primary-color);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            transition: background-color 0.2s ease;
          }
          .sb-btn-primary:hover {
            background-color: var(--btn-primary-color-hover);
          }
          .sb-input {
            height: var(--input-height-base);
            border: 1px solid var(--input-border-color);
            border-radius: 4px;
            padding: 0 12px;
            font-size: var(--font-size);
            transition: border-color 0.2s ease;
          }
          .sb-input:focus {
            outline: none;
            border-color: var(--btn-primary-color);
          }
        `}} />
        
        <div className="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
          {/* Logo/Brand */}
          <div className="text-center mb-8">
            <div className="flex justify-center mb-4">
              <div style={{
                width: '60px',
                height: '60px',
                backgroundColor: 'var(--btn-primary-color)',
                borderRadius: '12px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}>
                <Film className="w-8 h-8 text-white" />
              </div>
            </div>
            <h1 className="text-2xl font-bold mb-2" style={{ color: 'var(--body-color)' }}>
              StudioBinder
            </h1>
            <p className="text-gray-600">
              Film & TV Production Management Software
            </p>
          </div>

          {/* User Selection */}
          <div className="space-y-3">
            <p className="text-sm text-gray-600 text-center mb-4">Select your profile to continue</p>
            {Object.entries(users).map(([key, user]) => (
              <div
                key={key}
                onClick={() => {
                  setCurrentUser(user);
                  setNotifications([{
                    id: Date.now(),
                    message: `Welcome back, ${user.name}! You have ${user.projects} active projects.`,
                    type: 'info',
                    unread: true
                  }]);
                }}
                className="user-card flex items-center p-4 bg-white border rounded-lg"
                style={{ borderColor: 'var(--input-border-color)' }}
              >
                <div style={{
                  width: '48px',
                  height: '48px',
                  backgroundColor: 'var(--btn-primary-color)',
                  color: 'white',
                  borderRadius: '50%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '18px',
                  fontWeight: '600',
                  marginRight: '16px'
                }}>
                  {user.avatar}
                </div>
                <div className="flex-1">
                  <div className="font-semibold" style={{ color: 'var(--body-color)' }}>
                    {user.name}
                  </div>
                  <div className="text-sm text-gray-600">{user.role}</div>
                  <div className="text-xs text-gray-500">{user.department}</div>
                </div>
                <ArrowRight className="w-5 h-5 text-gray-400" />
              </div>
            ))}
          </div>

          {/* Footer */}
          <div className="mt-8 text-center">
            <p className="text-xs text-gray-500">
              Powered by StudioBinder Inc. © 2024
            </p>
          </div>
        </div>
      </div>
    );
  };

  // Sidebar Component (StudioBinder style)
  const Sidebar = () => {
    const menuItems = [
      { id: 'dashboard', label: 'Dashboard', icon: Home },
      { id: 'projects', label: 'Projects', icon: Film },
      { id: 'calendar', label: 'Calendar', icon: Calendar },
      { id: 'documents', label: 'Documents', icon: FolderOpen },
      { id: 'tasks', label: 'Tasks', icon: CheckCircle },
      { id: 'contacts', label: 'Contacts', icon: Users },
      { id: 'callsheets', label: 'Call Sheets', icon: Clapperboard },
      { id: 'schedule', label: 'Schedule', icon: Clock },
      { id: 'breakdown', label: 'Breakdown', icon: Layers },
      { id: 'reports', label: 'Reports', icon: BarChart2 }
    ];

    return (
      <div style={{
        width: sidebarOpen ? '240px' : '60px',
        backgroundColor: 'var(--nav-logged-in-bg-color)',
        height: '100vh',
        position: 'fixed',
        left: 0,
        top: 0,
        transition: 'width 0.3s ease',
        zIndex: 1000,
        display: 'flex',
        flexDirection: 'column'
      }}>
        {/* Logo Area */}
        <div style={{
          height: '60px',
          padding: '0 20px',
          display: 'flex',
          alignItems: 'center',
          borderBottom: '1px solid rgba(255,255,255,0.1)'
        }}>
          {sidebarOpen ? (
            <div className="flex items-center">
              <div style={{
                width: '32px',
                height: '32px',
                backgroundColor: 'var(--btn-primary-color)',
                borderRadius: '8px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                marginRight: '12px'
              }}>
                <Film className="w-5 h-5 text-white" />
              </div>
              <span className="text-white font-semibold">StudioBinder</span>
            </div>
          ) : (
            <div style={{
              width: '32px',
              height: '32px',
              backgroundColor: 'var(--btn-primary-color)',
              borderRadius: '8px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              margin: '0 auto'
            }}>
              <Film className="w-5 h-5 text-white" />
            </div>
          )}
        </div>

        {/* Navigation */}
        <nav className="flex-1 py-4">
          {menuItems.map(item => {
            const Icon = item.icon;
            const isActive = activeSection === item.id;
            
            return (
              <button
                key={item.id}
                onClick={() => setActiveSection(item.id)}
                style={{
                  width: '100%',
                  padding: '12px 20px',
                  display: 'flex',
                  alignItems: 'center',
                  border: 'none',
                  backgroundColor: isActive ? 'rgba(93, 120, 255, 0.1)' : 'transparent',
                  color: isActive ? 'var(--link-sidebar-color)' : 'var(--link-nav-bar-color)',
                  borderLeft: isActive ? '3px solid var(--link-sidebar-color)' : '3px solid transparent',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease',
                  fontSize: '14px'
                }}
                className="hover:bg-opacity-5 hover:bg-white"
              >
                <Icon className="w-5 h-5 flex-shrink-0" />
                {sidebarOpen && (
                  <span className="ml-3">{item.label}</span>
                )}
              </button>
            );
          })}
        </nav>

        {/* Bottom Actions */}
        <div style={{
          padding: '20px',
          borderTop: '1px solid rgba(255,255,255,0.1)'
        }}>
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            style={{
              width: '100%',
              padding: '8px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              border: 'none',
              backgroundColor: 'rgba(255,255,255,0.05)',
              color: 'var(--link-nav-bar-color)',
              borderRadius: '4px',
              cursor: 'pointer',
              transition: 'all 0.2s ease'
            }}
            className="hover:bg-opacity-10 hover:bg-white"
          >
            <Menu className="w-5 h-5" />
          </button>
        </div>
      </div>
    );
  };

  // Top Bar Component
  const TopBar = () => {
    return (
      <div style={{
        height: '60px',
        backgroundColor: 'white',
        borderBottom: '1px solid var(--input-border-color)',
        position: 'fixed',
        top: 0,
        left: sidebarOpen ? '240px' : '60px',
        right: 0,
        zIndex: 999,
        display: 'flex',
        alignItems: 'center',
        padding: '0 24px',
        transition: 'left 0.3s ease'
      }}>
        {/* Search */}
        <div className="flex-1 max-w-xl">
          <div className="relative">
            <Search className="w-5 h-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
            <input
              type="text"
              placeholder="Search projects, contacts, documents..."
              className="sb-input w-full pl-10"
              style={{ fontSize: '14px' }}
            />
          </div>
        </div>

        {/* Right Actions */}
        <div className="flex items-center space-x-4 ml-auto">
          {/* Notifications */}
          <button className="relative p-2 hover:bg-gray-100 rounded-lg transition-colors">
            <Bell className="w-5 h-5 text-gray-600" />
            {notifications.filter(n => n.unread).length > 0 && (
              <span style={{
                position: 'absolute',
                top: '6px',
                right: '6px',
                width: '8px',
                height: '8px',
                backgroundColor: 'var(--btn-accent-color)',
                borderRadius: '50%'
              }}></span>
            )}
          </button>

          {/* Help */}
          <button className="p-2 hover:bg-gray-100 rounded-lg transition-colors">
            <HelpCircle className="w-5 h-5 text-gray-600" />
          </button>

          {/* User Menu */}
          <div className="relative">
            <button
              onClick={() => setShowUserMenu(!showUserMenu)}
              className="flex items-center space-x-3 p-2 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <div style={{
                width: '32px',
                height: '32px',
                backgroundColor: 'var(--btn-primary-color)',
                color: 'white',
                borderRadius: '50%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '14px',
                fontWeight: '600'
              }}>
                {currentUser.avatar}
              </div>
              <div className="text-left hidden md:block">
                <div className="text-sm font-medium" style={{ color: 'var(--body-color)' }}>
                  {currentUser.name}
                </div>
                <div className="text-xs text-gray-500">{currentUser.role}</div>
              </div>
            </button>

            {/* User Dropdown */}
            {showUserMenu && (
              <div style={{
                position: 'absolute',
                right: 0,
                top: '100%',
                marginTop: '8px',
                width: '240px',
                backgroundColor: 'white',
                borderRadius: '8px',
                boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
                border: '1px solid var(--input-border-color)',
                zIndex: 1000
              }}>
                <div className="p-4 border-b" style={{ borderColor: 'var(--input-border-color)' }}>
                  <div className="font-medium" style={{ color: 'var(--body-color)' }}>
                    {currentUser.name}
                  </div>
                  <div className="text-sm text-gray-500">{currentUser.email}</div>
                </div>
                <div className="py-2">
                  <button className="w-full px-4 py-2 text-left hover:bg-gray-50 flex items-center space-x-3">
                    <Settings className="w-4 h-4 text-gray-500" />
                    <span className="text-sm">Account Settings</span>
                  </button>
                  <button className="w-full px-4 py-2 text-left hover:bg-gray-50 flex items-center space-x-3">
                    <HelpCircle className="w-4 h-4 text-gray-500" />
                    <span className="text-sm">Help & Support</span>
                  </button>
                  <hr className="my-2" style={{ borderColor: 'var(--input-border-color)' }} />
                  <button 
                    onClick={() => setCurrentUser(null)}
                    className="w-full px-4 py-2 text-left hover:bg-gray-50 flex items-center space-x-3"
                  >
                    <LogOut className="w-4 h-4 text-gray-500" />
                    <span className="text-sm">Log Out</span>
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    );
  };

  // Dashboard Component
  const Dashboard = () => {
    const stats = [
      { label: 'Active Projects', value: currentUser.projects, icon: Film, color: 'var(--btn-primary-color)' },
      { label: 'Call Sheets', value: 12, icon: Clapperboard, color: 'var(--btn-accent-color)' },
      { label: 'Tasks Due', value: 5, icon: CheckCircle, color: '#f59e0b' },
      { label: 'Team Members', value: 24, icon: Users, color: '#10b981' }
    ];

    const recentProjects = [
      { id: 1, name: 'Summer Campaign 2024', status: 'In Production', progress: 65, updated: '2 hours ago' },
      { id: 2, name: 'Documentary Series', status: 'Pre-Production', progress: 30, updated: '1 day ago' },
      { id: 3, name: 'Brand Commercial', status: 'Post-Production', progress: 85, updated: '3 days ago' }
    ];

    return (
      <div>
        {/* Welcome Section */}
        <div className="mb-8">
          <h1 className="text-2xl font-bold mb-2" style={{ color: 'var(--body-color)' }}>
            Welcome back, {currentUser.name}
          </h1>
          <p className="text-gray-600">
            Here's what's happening with your projects today.
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {stats.map((stat, index) => {
            const Icon = stat.icon;
            return (
              <div key={index} className="bg-white rounded-lg shadow-sm p-6" style={{
                border: '1px solid var(--input-border-color)'
              }}>
                <div className="flex items-center justify-between mb-4">
                  <div style={{
                    width: '48px',
                    height: '48px',
                    backgroundColor: `${stat.color}20`,
                    borderRadius: '12px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center'
                  }}>
                    <Icon className="w-6 h-6" style={{ color: stat.color }} />
                  </div>
                  <span className="text-2xl font-bold" style={{ color: 'var(--body-color)' }}>
                    {stat.value}
                  </span>
                </div>
                <h3 className="text-sm text-gray-600">{stat.label}</h3>
              </div>
            );
          })}
        </div>

        {/* Recent Projects */}
        <div className="bg-white rounded-lg shadow-sm" style={{
          border: '1px solid var(--input-border-color)'
        }}>
          <div className="p-6 border-b" style={{ borderColor: 'var(--input-border-color)' }}>
            <h2 className="text-lg font-semibold" style={{ color: 'var(--body-color)' }}>
              Recent Projects
            </h2>
          </div>
          <div className="p-6">
            <div className="space-y-4">
              {recentProjects.map(project => (
                <div key={project.id} className="flex items-center justify-between p-4 rounded-lg hover:bg-gray-50 transition-colors">
                  <div className="flex items-center space-x-4">
                    <div style={{
                      width: '40px',
                      height: '40px',
                      backgroundColor: 'var(--btn-primary-color)',
                      borderRadius: '8px',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center'
                    }}>
                      <Film className="w-5 h-5 text-white" />
                    </div>
                    <div>
                      <h3 className="font-medium" style={{ color: 'var(--body-color)' }}>
                        {project.name}
                      </h3>
                      <p className="text-sm text-gray-500">{project.status}</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-4">
                    <div className="text-right">
                      <div className="text-sm font-medium" style={{ color: 'var(--body-color)' }}>
                        {project.progress}%
                      </div>
                      <div className="text-xs text-gray-500">{project.updated}</div>
                    </div>
                    <button className="p-2 hover:bg-gray-100 rounded-lg transition-colors">
                      <ArrowRight className="w-5 h-5 text-gray-400" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  };

  // Calendar Component (Simplified)
  const CalendarView = () => {
    const events = [
      { id: 1, title: 'Call Time - Main Unit', time: '06:00 AM', type: 'call', location: 'Studio A' },
      { id: 2, title: 'Production Meeting', time: '10:00 AM', type: 'meeting', location: 'Conference Room' },
      { id: 3, title: 'Location Scout', time: '02:00 PM', type: 'scout', location: 'Downtown' }
    ];

    return (
      <div>
        <div className="mb-8">
          <h1 className="text-2xl font-bold mb-2" style={{ color: 'var(--body-color)' }}>
            Production Calendar
          </h1>
          <p className="text-gray-600">
            Manage your shooting schedule and events
          </p>
        </div>

        <div className="bg-white rounded-lg shadow-sm p-6" style={{
          border: '1px solid var(--input-border-color)'
        }}>
          {/* Calendar Header */}
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center space-x-4">
              <button className="p-2 hover:bg-gray-100 rounded-lg transition-colors">
                <ChevronLeft className="w-5 h-5 text-gray-600" />
              </button>
              <h2 className="text-lg font-semibold" style={{ color: 'var(--body-color)' }}>
                January 2024
              </h2>
              <button className="p-2 hover:bg-gray-100 rounded-lg transition-colors">
                <ChevronRight className="w-5 h-5 text-gray-600" />
              </button>
            </div>
            <button className="sb-btn-primary flex items-center space-x-2">
              <Plus className="w-4 h-4" />
              <span>Add Event</span>
            </button>
          </div>

          {/* Today's Events */}
          <div className="space-y-3">
            <h3 className="font-medium text-gray-700 mb-3">Today's Schedule</h3>
            {events.map(event => (
              <div key={event.id} className="flex items-center space-x-4 p-4 rounded-lg" style={{
                backgroundColor: 'rgba(93, 120, 255, 0.05)',
                border: '1px solid rgba(93, 120, 255, 0.1)'
              }}>
                <div className="flex-shrink-0">
                  <div className="text-sm font-medium" style={{ color: 'var(--btn-primary-color)' }}>
                    {event.time}
                  </div>
                </div>
                <div className="flex-1">
                  <h4 className="font-medium" style={{ color: 'var(--body-color)' }}>
                    {event.title}
                  </h4>
                  <p className="text-sm text-gray-500 flex items-center mt-1">
                    <MapPin className="w-3 h-3 mr-1" />
                    {event.location}
                  </p>
                </div>
                <button className="p-2 hover:bg-gray-100 rounded-lg transition-colors">
                  <Edit className="w-4 h-4 text-gray-400" />
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  };

  // Main Layout
  const MainLayout = () => {
    return (
      <div className="min-h-screen" style={{ backgroundColor: '#f8f9fa' }}>
        <style dangerouslySetInnerHTML={{ __html: cssVariables }} />
        <style dangerouslySetInnerHTML={{ __html: `
          @keyframes spin {
            to { transform: rotate(360deg); }
          }
          @keyframes bounce {
            0%, 100% { transform: translate(-50%, -50%) scale(1); }
            50% { transform: translate(-50%, -50%) scale(1.2); }
          }
          .sb-btn-primary {
            background-color: var(--btn-primary-color);
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            transition: background-color 0.2s ease;
            display: inline-flex;
            align-items: center;
          }
          .sb-btn-primary:hover {
            background-color: var(--btn-primary-color-hover);
          }
          .sb-input {
            height: var(--input-height-base);
            border: 1px solid var(--input-border-color);
            border-radius: 4px;
            padding: 0 12px;
            font-size: var(--font-size);
            transition: border-color 0.2s ease;
            background-color: white;
          }
          .sb-input:focus {
            outline: none;
            border-color: var(--btn-primary-color);
          }
        `}} />
        
        <Sidebar />
        <TopBar />
        
        <main style={{
          marginLeft: sidebarOpen ? '240px' : '60px',
          marginTop: '60px',
          padding: '24px',
          transition: 'margin-left 0.3s ease',
          minHeight: 'calc(100vh - 60px)'
        }}>
          {activeSection === 'dashboard' && <Dashboard />}
          {activeSection === 'calendar' && <CalendarView />}
          {activeSection === 'projects' && (
            <div className="bg-white rounded-lg shadow-sm p-6" style={{
              border: '1px solid var(--input-border-color)'
            }}>
              <h2 className="text-xl font-semibold mb-4" style={{ color: 'var(--body-color)' }}>
                Projects
              </h2>
              <p className="text-gray-600">Project management coming soon...</p>
            </div>
          )}
          {/* Add more sections as needed */}
        </main>
      </div>
    );
  };

  // Show loading spinner initially
  if (loading) {
    return <LoadingSpinner />;
  }

  // Show login if no user
  if (!currentUser) {
    return <Login />;
  }

  // Show main app
  return <MainLayout />;
};

export default StudioBinderClone;