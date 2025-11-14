import React, { useState, useEffect, useCallback, createContext, useContext, useMemo } from 'react';
import { 
  Calendar, Film, Users, FileText, Bell, Eye, Lock, Upload, MessageCircle, 
  Camera, Clapperboard, Video, FolderOpen, Clock, CheckCircle, AlertCircle,
  ChevronLeft, ChevronRight, Plus, Grid, List, Filter, Search, Download,
  Edit, Trash2, Share2, Cloud, CloudRain, Sun, Wind, MapPin, Phone,
  Mail, DollarSign, TrendingUp, BarChart2, Image, Layers, Move, Menu,
  X, ArrowRight, ExternalLink, Settings, HelpCircle, LogOut, Home,
  Shield, Key, Database, Activity, Briefcase, Target, FileCheck,
  Palette, ListChecks, Navigation, Thermometer, Droplets, AlertTriangle,
  Coffee, Car, Hospital, ChevronDown, Copy, Printer, Send, Check,
  Timer, Percent, TrendingDown, Award, Zap, Globe, Radio, GitBranch,
  FileVideo, Package, Calculator, WifiOff, Wifi, Volume2, History,
  RefreshCw, PlayCircle, Pause, SkipForward, UserCheck,
  UserX, UserPlus, EyeOff, Info, Smartphone, Monitor, Loader
} from 'lucide-react';

// ==================== SISTEMA PRINCIPAL DEBUGADO ====================
const CineProSystem = () => {
  // Estado de Autenticação
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [currentUser, setCurrentUser] = useState(null);
  
  // Estados da Aplicação
  const [activeModule, setActiveModule] = useState('dashboard');
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [showNotifications, setShowNotifications] = useState(false);
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [notifications, setNotifications] = useState([
    { id: 1, message: 'Nova call sheet disponível', time: 'Há 5 minutos' },
    { id: 2, message: 'Orçamento atualizado no Projeto Eclipse', time: 'Há 1 hora' }
  ]);

  // Mock Data - Usuários para teste
  const mockUsers = [
    {
      id: 'user-001',
      name: 'Sofia Luz',
      email: 'sofia@cinepro.com',
      password: 'demo123', // Em produção seria hash
      role: 'Director',
      department: 'Direction'
    },
    {
      id: 'user-002',
      name: 'Marcus Terra',
      email: 'marcus@cinepro.com',
      password: 'demo123',
      role: 'Producer',
      department: 'Production'
    },
    {
      id: 'user-003',
      name: 'Luna Sombra',
      email: 'luna@cinepro.com',
      password: 'demo123',
      role: 'Director of Photography',
      department: 'Camera'
    }
  ];

  // Mock Data - Projetos
  const mockProjects = [
    {
      id: 'proj-001',
      title: 'Eclipse - O Filme',
      type: 'Feature Film',
      status: 'Production',
      budget: 5000000,
      spent: 3225000,
      startDate: '2024-01-10',
      endDate: '2024-04-15',
      shootingDays: 60,
      completedDays: 38,
      director: 'Sofia Luz',
      producer: 'Marcus Terra',
      dop: 'Luna Sombra',
      description: 'Um épico de ficção científica sobre a última esperança da humanidade.'
    },
    {
      id: 'proj-002',
      title: 'Urban Series',
      type: 'TV Series',
      status: 'Pre-Production',
      budget: 8000000,
      spent: 1200000,
      startDate: '2024-02-01',
      endDate: '2024-06-30',
      shootingDays: 90,
      completedDays: 12,
      director: 'Alex Rivers',
      producer: 'Marcus Terra',
      dop: 'Luna Sombra',
      description: 'Série dramática sobre a vida nas grandes metrópoles.'
    },
    {
      id: 'proj-003',
      title: 'Nexus Campaign',
      type: 'Commercial',
      status: 'Post-Production',
      budget: 2500000,
      spent: 2100000,
      startDate: '2024-01-15',
      endDate: '2024-03-30',
      shootingDays: 45,
      completedDays: 45,
      director: 'Sofia Luz',
      producer: 'Eva Storm',
      dop: 'Chris Light',
      description: 'Campanha publicitária para o lançamento do Nexus 2024.'
    }
  ];

  // Verificar sessão salva ao carregar
  useEffect(() => {
    const savedSession = localStorage.getItem('cinepro_session');
    if (savedSession) {
      try {
        const session = JSON.parse(savedSession);
        if (session.user && session.timestamp && Date.now() - session.timestamp < 86400000) {
          setCurrentUser(session.user);
          setIsAuthenticated(true);
        }
      } catch (error) {
        console.error('Erro ao recuperar sessão:', error);
        localStorage.removeItem('cinepro_session');
      }
    }
  }, []);

  // ==================== COMPONENTE DE LOGIN ====================
  const LoginScreen = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [rememberMe, setRememberMe] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');

    const handleLogin = (e) => {
      e.preventDefault();
      setIsLoading(true);
      setError('');

      // Simular delay de rede
      setTimeout(() => {
        // Validar credenciais
        const user = mockUsers.find(u => u.email === email && u.password === password);
        
        if (user) {
          // Login bem-sucedido
          setCurrentUser(user);
          setIsAuthenticated(true);
          
          // Salvar sessão se "Lembrar de mim" estiver marcado
          if (rememberMe) {
            localStorage.setItem('cinepro_session', JSON.stringify({
              user,
              timestamp: Date.now()
            }));
          }
          
          setError('');
        } else {
          // Login falhou
          setError('Email ou senha inválidos. Use: sofia@cinepro.com / demo123');
        }
        
        setIsLoading(false);
      }, 500);
    };

    const quickLogin = (userEmail, userPassword) => {
      setEmail(userEmail);
      setPassword(userPassword);
      // Auto-submit após preencher
      setTimeout(() => {
        const form = document.getElementById('login-form');
        if (form) {
          form.dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
        }
      }, 100);
    };

    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 via-blue-900 to-gray-900 p-4">
        <div className="w-full max-w-md">
          {/* Logo e Título */}
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-20 h-20 bg-blue-600 rounded-full mb-4 shadow-2xl">
              <Film className="w-10 h-10 text-white" />
            </div>
            <h1 className="text-4xl font-bold text-white mb-2">CineProd Pro</h1>
            <p className="text-gray-300">Sistema de Gestão Cinematográfica</p>
          </div>

          {/* Card de Login */}
          <div className="bg-gray-800 bg-opacity-50 backdrop-blur-lg rounded-2xl shadow-2xl p-8 border border-gray-700">
            <form id="login-form" onSubmit={handleLogin} className="space-y-6">
              {/* Campo Email */}
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Email
                </label>
                <div className="relative">
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="w-full px-4 py-3 bg-gray-900 bg-opacity-50 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors"
                    placeholder="seu@email.com"
                    required
                  />
                  <Mail className="absolute right-3 top-3.5 w-5 h-5 text-gray-400" />
                </div>
              </div>

              {/* Campo Senha */}
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Senha
                </label>
                <div className="relative">
                  <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="w-full px-4 py-3 bg-gray-900 bg-opacity-50 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors"
                    placeholder="••••••••"
                    required
                  />
                  <Lock className="absolute right-3 top-3.5 w-5 h-5 text-gray-400" />
                </div>
              </div>

              {/* Mensagem de Erro */}
              {error && (
                <div className="p-3 bg-red-900 bg-opacity-50 border border-red-500 rounded-lg">
                  <p className="text-sm text-red-300">{error}</p>
                </div>
              )}

              {/* Lembrar de mim */}
              <div className="flex items-center justify-between">
                <label className="flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    checked={rememberMe}
                    onChange={(e) => setRememberMe(e.target.checked)}
                    className="w-4 h-4 bg-gray-900 border-gray-600 rounded text-blue-600 focus:ring-blue-500"
                  />
                  <span className="ml-2 text-sm text-gray-300">Lembrar de mim</span>
                </label>
                <a href="#" className="text-sm text-blue-400 hover:text-blue-300 transition-colors">
                  Esqueceu a senha?
                </a>
              </div>

              {/* Botão de Login */}
              <button
                type="submit"
                disabled={isLoading}
                className="w-full py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-800 disabled:cursor-not-allowed text-white font-semibold rounded-lg transition-colors duration-200 flex items-center justify-center gap-2"
              >
                {isLoading ? (
                  <>
                    <Loader className="w-5 h-5 animate-spin" />
                    <span>Entrando...</span>
                  </>
                ) : (
                  <span>Entrar</span>
                )}
              </button>
            </form>

            {/* Divisor */}
            <div className="mt-6 pt-6 border-t border-gray-700">
              <p className="text-center text-sm text-gray-400 mb-4">
                Acesso rápido para demonstração:
              </p>
              
              {/* Botões de Login Rápido */}
              <div className="grid grid-cols-3 gap-2">
                <button
                  onClick={() => quickLogin('sofia@cinepro.com', 'demo123')}
                  className="px-3 py-2 bg-gray-700 hover:bg-gray-600 text-gray-200 text-xs rounded-lg transition-colors"
                >
                  Diretor
                </button>
                <button
                  onClick={() => quickLogin('marcus@cinepro.com', 'demo123')}
                  className="px-3 py-2 bg-gray-700 hover:bg-gray-600 text-gray-200 text-xs rounded-lg transition-colors"
                >
                  Produtor
                </button>
                <button
                  onClick={() => quickLogin('luna@cinepro.com', 'demo123')}
                  className="px-3 py-2 bg-gray-700 hover:bg-gray-600 text-gray-200 text-xs rounded-lg transition-colors"
                >
                  DP
                </button>
              </div>

              <p className="text-center text-xs text-gray-500 mt-4">
                Senha para todos: <span className="text-gray-400 font-mono">demo123</span>
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  };

  // ==================== COMPONENTE SIDEBAR ====================
  const Sidebar = () => {
    const menuItems = [
      { id: 'dashboard', label: 'Dashboard', icon: Home },
      { id: 'projects', label: 'Projetos', icon: Film },
      { id: 'schedule', label: 'Cronograma', icon: Calendar },
      { id: 'crew', label: 'Equipe', icon: Users },
      { id: 'equipment', label: 'Equipamentos', icon: Camera },
      { id: 'locations', label: 'Locações', icon: MapPin },
      { id: 'documents', label: 'Documentos', icon: FileText },
      { id: 'budget', label: 'Orçamento', icon: DollarSign },
      { id: 'reports', label: 'Relatórios', icon: BarChart2 },
      { id: 'settings', label: 'Configurações', icon: Settings }
    ];

    return (
      <div 
        className={`fixed left-0 top-0 h-full bg-gray-900 border-r border-gray-800 transition-all duration-300 z-40 ${
          sidebarOpen ? 'w-64' : 'w-20'
        }`}
      >
        {/* Header da Sidebar */}
        <div className="flex items-center justify-between p-4 border-b border-gray-800">
          <div className={`flex items-center gap-3 ${!sidebarOpen && 'justify-center'}`}>
            <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
              <Film className="w-6 h-6 text-white" />
            </div>
            {sidebarOpen && <span className="text-xl font-bold text-white">CineProd</span>}
          </div>
          {sidebarOpen && (
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="p-2 hover:bg-gray-800 rounded-lg transition-colors"
            >
              <Menu className="w-5 h-5 text-gray-400" />
            </button>
          )}
        </div>

        {/* Menu Items */}
        <nav className="p-4 space-y-1">
          {menuItems.map((item) => {
            const Icon = item.icon;
            return (
              <button
                key={item.id}
                onClick={() => setActiveModule(item.id)}
                className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200 ${
                  activeModule === item.id
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-400 hover:bg-gray-800 hover:text-white'
                } ${!sidebarOpen && 'justify-center'}`}
                title={!sidebarOpen ? item.label : ''}
              >
                <Icon className="w-5 h-5 flex-shrink-0" />
                {sidebarOpen && <span className="font-medium">{item.label}</span>}
              </button>
            );
          })}
        </nav>

        {/* Botão para expandir sidebar quando fechada */}
        {!sidebarOpen && (
          <button
            onClick={() => setSidebarOpen(true)}
            className="absolute bottom-4 left-1/2 transform -translate-x-1/2 p-2 bg-gray-800 hover:bg-gray-700 rounded-lg transition-colors"
          >
            <ChevronRight className="w-5 h-5 text-gray-400" />
          </button>
        )}
      </div>
    );
  };

  // ==================== COMPONENTE HEADER ====================
  const Header = () => {
    const handleLogout = () => {
      setIsAuthenticated(false);
      setCurrentUser(null);
      localStorage.removeItem('cinepro_session');
      setShowUserMenu(false);
    };

    return (
      <header className="fixed top-0 right-0 left-0 h-16 bg-gray-900 bg-opacity-90 backdrop-blur-md border-b border-gray-800 z-30">
        <div className={`h-full flex items-center justify-between px-6 transition-all duration-300 ${
          sidebarOpen ? 'ml-64' : 'ml-20'
        }`}>
          {/* Search Bar */}
          <div className="flex-1 max-w-xl">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-500" />
              <input
                type="text"
                placeholder="Buscar projetos, pessoas, documentos..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2 bg-gray-800 bg-opacity-50 border border-gray-700 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
              />
            </div>
          </div>

          {/* Actions */}
          <div className="flex items-center gap-4">
            {/* Notifications */}
            <div className="relative">
              <button
                onClick={() => setShowNotifications(!showNotifications)}
                className="relative p-2 hover:bg-gray-800 rounded-lg transition-colors"
              >
                <Bell className="w-5 h-5 text-gray-400" />
                {notifications.length > 0 && (
                  <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
                )}
              </button>

              {/* Dropdown de Notificações */}
              {showNotifications && (
                <div className="absolute right-0 mt-2 w-80 bg-gray-800 rounded-xl shadow-2xl border border-gray-700">
                  <div className="p-4 border-b border-gray-700">
                    <h3 className="font-semibold text-white">Notificações</h3>
                  </div>
                  <div className="max-h-96 overflow-y-auto">
                    {notifications.map((notification) => (
                      <div
                        key={notification.id}
                        className="p-4 hover:bg-gray-700 border-b border-gray-700 last:border-b-0"
                      >
                        <p className="text-sm text-gray-200">{notification.message}</p>
                        <p className="text-xs text-gray-500 mt-1">{notification.time}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* User Menu */}
            <div className="relative">
              <button
                onClick={() => setShowUserMenu(!showUserMenu)}
                className="flex items-center gap-3 p-2 hover:bg-gray-800 rounded-lg transition-colors"
              >
                <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                  <span className="text-sm font-medium text-white">
                    {currentUser?.name?.split(' ').map(n => n[0]).join('') || 'U'}
                  </span>
                </div>
                <div className="text-left hidden md:block">
                  <p className="text-sm font-medium text-white">{currentUser?.name}</p>
                  <p className="text-xs text-gray-500">{currentUser?.role}</p>
                </div>
                <ChevronDown className="w-4 h-4 text-gray-400" />
              </button>

              {/* Dropdown do Usuário */}
              {showUserMenu && (
                <div className="absolute right-0 mt-2 w-56 bg-gray-800 rounded-xl shadow-2xl border border-gray-700">
                  <div className="p-2">
                    <button className="w-full flex items-center gap-3 px-3 py-2 hover:bg-gray-700 rounded-lg text-gray-300 transition-colors">
                      <Users className="w-4 h-4" />
                      <span>Meu Perfil</span>
                    </button>
                    <button className="w-full flex items-center gap-3 px-3 py-2 hover:bg-gray-700 rounded-lg text-gray-300 transition-colors">
                      <Settings className="w-4 h-4" />
                      <span>Configurações</span>
                    </button>
                    <button className="w-full flex items-center gap-3 px-3 py-2 hover:bg-gray-700 rounded-lg text-gray-300 transition-colors">
                      <HelpCircle className="w-4 h-4" />
                      <span>Ajuda</span>
                    </button>
                    <hr className="my-2 border-gray-700" />
                    <button
                      onClick={handleLogout}
                      className="w-full flex items-center gap-3 px-3 py-2 hover:bg-gray-700 rounded-lg text-red-400 transition-colors"
                    >
                      <LogOut className="w-4 h-4" />
                      <span>Sair</span>
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </header>
    );
  };

  // ==================== COMPONENTE DASHBOARD ====================
  const Dashboard = () => {
    const stats = [
      { label: 'Projetos Ativos', value: 3, icon: Film, color: 'blue' },
      { label: 'Equipe Total', value: 47, icon: Users, color: 'green' },
      { label: 'Orçamento Total', value: 'R$ 15.5M', icon: DollarSign, color: 'yellow' },
      { label: 'Dias de Filmagem', value: 195, icon: Calendar, color: 'purple' }
    ];

    return (
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-white mb-2">Dashboard</h1>
          <p className="text-gray-400">Bem-vindo(a), {currentUser?.name}</p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {stats.map((stat) => {
            const Icon = stat.icon;
            return (
              <div
                key={stat.label}
                className="bg-gray-800 bg-opacity-50 backdrop-blur-sm rounded-xl p-6 border border-gray-700 hover:border-blue-500 transition-colors"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-400 text-sm">{stat.label}</p>
                    <p className="text-2xl font-bold text-white mt-1">{stat.value}</p>
                  </div>
                  <div className={`p-3 bg-${stat.color}-600 bg-opacity-20 rounded-lg`}>
                    <Icon className="w-6 h-6 text-blue-400" />
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* Projects List */}
        <div className="bg-gray-800 bg-opacity-50 backdrop-blur-sm rounded-xl p-6 border border-gray-700">
          <h2 className="text-xl font-semibold text-white mb-4">Projetos Recentes</h2>
          <div className="space-y-4">
            {mockProjects.map((project) => (
              <div
                key={project.id}
                className="flex items-center justify-between p-4 bg-gray-900 bg-opacity-50 rounded-lg"
              >
                <div>
                  <h3 className="font-medium text-white">{project.title}</h3>
                  <p className="text-sm text-gray-400">{project.type} • {project.director}</p>
                </div>
                <div className="flex items-center gap-4">
                  <div className="text-right">
                    <p className="text-sm text-gray-400">Progresso</p>
                    <p className="text-lg font-semibold text-white">
                      {Math.round((project.completedDays / project.shootingDays) * 100)}%
                    </p>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                    project.status === 'Production' ? 'bg-green-600 bg-opacity-20 text-green-400' :
                    project.status === 'Pre-Production' ? 'bg-yellow-600 bg-opacity-20 text-yellow-400' :
                    'bg-blue-600 bg-opacity-20 text-blue-400'
                  }`}>
                    {project.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  };

  // ==================== MAIN APP LAYOUT ====================
  const MainLayout = () => {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
        <Sidebar />
        <Header />
        <main className={`pt-20 pb-8 px-6 transition-all duration-300 ${
          sidebarOpen ? 'ml-64' : 'ml-20'
        }`}>
          {activeModule === 'dashboard' && <Dashboard />}
          {activeModule === 'projects' && (
            <div className="text-white">
              <h1 className="text-3xl font-bold mb-4">Projetos</h1>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {mockProjects.map((project) => (
                  <div key={project.id} className="bg-gray-800 bg-opacity-50 backdrop-blur-sm rounded-xl p-6 border border-gray-700">
                    <h3 className="text-xl font-semibold mb-2">{project.title}</h3>
                    <p className="text-gray-400 text-sm mb-4">{project.description}</p>
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-500">{project.type}</span>
                      <button className="px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white text-sm rounded-lg transition-colors">
                        Ver Detalhes
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
          {activeModule !== 'dashboard' && activeModule !== 'projects' && (
            <div className="bg-gray-800 bg-opacity-50 backdrop-blur-sm rounded-xl p-8 border border-gray-700">
              <h1 className="text-2xl font-bold text-white mb-4">
                {activeModule.charAt(0).toUpperCase() + activeModule.slice(1)}
              </h1>
              <p className="text-gray-400">
                Módulo em desenvolvimento. Em breve você poderá acessar todas as funcionalidades.
              </p>
            </div>
          )}
        </main>
      </div>
    );
  };

  // ==================== RENDER CONDICIONAL ====================
  return isAuthenticated ? <MainLayout /> : <LoginScreen />;
};

// Exportar o componente
export default CineProSystem;