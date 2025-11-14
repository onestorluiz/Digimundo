import React, { useState, useEffect, useCallback, createContext, useContext } from 'react';
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
  UserX, UserPlus, EyeOff, Info, Smartphone, Monitor,
  Megaphone, Headphones, Mic, MicOff, VideoOff, MoreVertical, Star,
  Building2, FileBarChart, Moon, User, Save, PlusCircle,
  FileDown, FilePlus, ChevronUp, MessageSquare, Paperclip, 
  Bookmark, Archive, Link, Inbox, Hash, AtSign, Tag, Flag
} from 'lucide-react';

// CSS Variables do StudioBinder + Custom Styles
const cssVariables = \`
  :root {
    --btn-primary-color: #5d78ff;
    --btn-primary-color-RGB: 93, 120, 255;
    --btn-primary-color-hover: #384ad7;
    --btn-accent-color: #FA1870;
    --link-color: #5d78ff;
    --link-nav-bar-color: #A2A3B7;
    --link-nav-bar-color-hover: #fff;
    --nav-logged-in-bg-color: #1D1E2C;
    --nav-logged-in-bg-color-hover: #1b1b28;
    --link-sidebar-color: #5d78ff;
    --input-border-color: #D8E0E6;
    --font-size: 13px;
    --body-color: #1B1C21;
    --input-height-base: 36px;
  }
  
  * {
    box-sizing: border-box;
  }
  
  @keyframes fade-in {
    from { opacity: 0; }
    to { opacity: 1; }
  }
  
  @keyframes scale-in {
    from { opacity: 0; transform: scale(0.95); }
    to { opacity: 1; transform: scale(1); }
  }
  
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
  
  @keyframes bounce {
    0%, 100% { transform: translate(-50%, -50%) scale(1); }
    50% { transform: translate(-50%, -50%) scale(1.2); }
  }
  
  .animate-fade-in { animation: fade-in 0.3s ease-out; }
  .animate-scale-in { animation: scale-in 0.3s ease-out; }
  
  .sb-btn-primary {
    background-color: var(--btn-primary-color);
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
  }
  .sb-btn-primary:hover {
    background-color: var(--btn-primary-color-hover);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(93, 120, 255, 0.3);
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
    box-shadow: 0 0 0 3px rgba(93, 120, 255, 0.1);
  }
  
  .user-card {
    transition: all 0.2s ease;
    cursor: pointer;
  }
  .user-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  }
\`;

// Injetar estilos
if (typeof document !== 'undefined') {
  const styleElement = document.createElement('style');
  styleElement.textContent = cssVariables;
  document.head.appendChild(styleElement);
}

// Contextos
const ModalContext = createContext(null);

// Modal Provider
const ModalProvider = ({ children }) => {
  const [modals, setModals] = useState([]);

  const openModal = useCallback((content, options = {}) => {
    const id = Date.now() + Math.random();
    setModals(prev => [...prev, { id, content, options }]);
    return id;
  }, []);

  const closeModal = useCallback((id) => {
    setModals(prev => prev.filter(modal => modal.id !== id));
  }, []);

  const closeAllModals = useCallback(() => {
    setModals([]);
  }, []);

  return (
    <ModalContext.Provider value={{ openModal, closeModal, closeAllModals }}>
      {children}
      {modals.map(modal => (
        <div key={modal.id} className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4 animate-fade-in">
          <div className="bg-white rounded-lg shadow-xl max-w-lg w-full max-h-[90vh] overflow-auto animate-scale-in">
            {modal.content(modal.id)}
          </div>
        </div>
      ))}
    </ModalContext.Provider>
  );
};

// Hook para Modal
const useModal = () => {
  const context = useContext(ModalContext);
  if (!context) throw new Error('useModal must be used within ModalProvider');
  return context;
};

// Sistema Principal
const CineProductionSystem = () => {
  // Estados Globais
  const [appState, setAppState] = useState(() => {
    const savedSession = localStorage.getItem('cineprod_session');
    if (savedSession) {
      try {
        const session = JSON.parse(savedSession);
        if (session.timestamp && Date.now() - session.timestamp < 24 * 60 * 60 * 1000) {
          return {
            language: 'pt',
            theme: 'light',
            currentUser: session.currentUser,
            isAuthenticated: true,
            authToken: session.authToken,
            rememberMe: session.rememberMe,
            savedEmail: session.savedEmail || ''
          };
        }
      } catch (e) {
        console.error('Erro ao carregar sessão:', e);
      }
    }
    
    return {
      language: 'pt',
      theme: 'light',
      currentUser: null,
      isAuthenticated: false,
      authToken: null,
      rememberMe: false,
      savedEmail: localStorage.getItem('cineprod_saved_email') || ''
    };
  });
  
  const [activeModule, setActiveModule] = useState('dashboard');
  const [loading, setLoading] = useState(true);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [notifications, setNotifications] = useState([]);
  const [currentProject, setCurrentProject] = useState(null);
  const [globalSearch, setGlobalSearch] = useState('');
  const [notificationsOpen, setNotificationsOpen] = useState(false);
  const [userMenuOpen, setUserMenuOpen] = useState(false);
  const { openModal, closeModal } = useModal();

  // Banco de dados de usuários
  const usersDatabase = [
    {
      id: 1,
      name: 'Sofia Luz',
      email: 'sofia@cineprod.com',
      password: 'director123',
      role: 'Director',
      department: 'Creative',
      avatar: 'SL',
      projects: 3,
      twoFactorEnabled: false
    },
    {
      id: 2,
      name: 'Marcus Terra',
      email: 'marcus@cineprod.com',
      password: 'producer123',
      role: 'Producer',
      department: 'Production',
      avatar: 'MT',
      projects: 5,
      twoFactorEnabled: false
    },
    {
      id: 3,
      name: 'Luna Sombra',
      email: 'luna@cineprod.com',
      password: 'dp123',
      role: 'DP',
      department: 'Photography',
      avatar: 'LS',
      projects: 2,
      twoFactorEnabled: false
    },
    {
      id: 4,
      name: 'Rio Vento',
      email: 'rio@cineprod.com',
      password: 'talent123',
      role: 'Talent',
      department: 'Cast',
      avatar: 'RV',
      projects: 1,
      twoFactorEnabled: false
    },
    {
      id: 5,
      name: 'Admin Sistema',
      email: 'admin@cineprod.com',
      password: 'admin123',
      role: 'Administrator',
      department: 'Management',
      avatar: 'AD',
      projects: 10,
      twoFactorEnabled: true
    }
  ];

  // Dados de produção
  const [productionData, setProductionData] = useState({
    projects: [
      {
        id: 1,
        title: 'Projeto Eclipse',
        type: 'Feature Film',
        budget: 5000000,
        spent: 3225000,
        startDate: '2024-01-10',
        endDate: '2024-04-15',
        shootingDays: 60,
        completedDays: 38,
        director: 'Sofia Luz',
        producer: 'Marcus Terra',
        dop: 'Luna Sombra',
        status: 'In Production',
        progress: 63
      }
    ],
    callSheets: [
      {
        id: 1,
        date: '2024-01-20',
        day: 5,
        callTime: '06:00',
        wrap: '18:00',
        location: 'Studio A - São Paulo',
        scenes: ['1A', '2', '3B'],
        status: 'distributed',
        weather: { temp: 28, condition: 'sunny', sunrise: '05:45', sunset: '19:30' }
      }
    ],
    crew: [
      { id: 1, name: 'Sofia Luz', role: 'Director', department: 'Direction', phone: '+55 11 99999-0001', email: 'sofia@prod.com', dayRate: 5000, union: 'DGA', daysWorked: 29 }
    ],
    tasks: [
      { id: 1, title: 'Review script changes Scene 5', assignee: 'Sofia Luz', due: '2024-01-22', priority: 'high', status: 'pending', department: 'Direction' }
    ]
  });

  // Traduções
  const translations = {
    pt: {
      appName: 'CineProd Systems',
      tagline: 'Gestão Profissional de Produção Cinematográfica',
      welcome: 'Bem-vindo de volta',
      login: 'Entrar',
      email: 'Email',
      password: 'Senha',
      rememberMe: 'Lembrar de mim',
      forgotPassword: 'Esqueceu a senha?',
      selectProfile: 'Selecione seu perfil para continuar',
      loading: 'Carregando sistema...',
      logout: 'Sair',
      myProfile: 'Meu Perfil',
      accountSettings: 'Configurações da Conta',
      help: 'Ajuda',
      notifications: 'Notificações',
      search: 'Buscar',
      modules: {
        dashboard: 'Dashboard',
        projects: 'Projetos',
        calendar: 'Calendário',
        callsheets: 'Folhas de Chamada',
        schedule: 'Cronograma',
        breakdown: 'Decupagem',
        crew: 'Elenco e Equipe',
        documents: 'Documentos',
        tasks: 'Tarefas',
        budget: 'Orçamento',
        reports: 'Relatórios',
        contacts: 'Contatos',
        stripboard: 'Stripboard',
        communication: 'Comunicação',
        postproduction: 'Pós-produção'
      },
      productionDay: 'Dia de Produção',
      of: 'de',
      dailyBurnRate: 'Gasto Diário',
      pagesPerDay: 'Páginas/Dia',
      crewAttendance: 'Presença da Equipe',
      scriptCoverage: 'Cobertura do Roteiro',
      newCallSheet: 'Nova Folha',
      viewReports: 'Ver Relatórios',
      manageCrew: 'Gerenciar Equipe',
      viewSchedule: 'Ver Cronograma'
    },
    en: {
      appName: 'CineProd Systems',
      tagline: 'Professional Film Production Management',
      welcome: 'Welcome back',
      login: 'Login',
      email: 'Email',
      password: 'Password',
      rememberMe: 'Remember me',
      forgotPassword: 'Forgot password?',
      selectProfile: 'Select your profile to continue',
      loading: 'Loading system...',
      logout: 'Logout',
      myProfile: 'My Profile',
      accountSettings: 'Account Settings',
      help: 'Help',
      notifications: 'Notifications',
      search: 'Search',
      modules: {
        dashboard: 'Dashboard',
        projects: 'Projects',
        calendar: 'Calendar',
        callsheets: 'Call Sheets',
        schedule: 'Schedule',
        breakdown: 'Script Breakdown',
        crew: 'Cast & Crew',
        documents: 'Documents',
        tasks: 'Tasks',
        budget: 'Budget',
        reports: 'Reports',
        contacts: 'Contacts',
        stripboard: 'Stripboard',
        communication: 'Communication',
        postproduction: 'Post-production'
      },
      productionDay: 'Production Day',
      of: 'of',
      dailyBurnRate: 'Daily Burn Rate',
      pagesPerDay: 'Pages/Day',
      crewAttendance: 'Crew Attendance',
      scriptCoverage: 'Script Coverage',
      newCallSheet: 'New Call Sheet',
      viewReports: 'View Reports',
      manageCrew: 'Manage Crew',
      viewSchedule: 'View Schedule'
    }
  };

  const t = useCallback((key) => {
    const keys = key.split('.');
    let value = translations[appState.language];
    for (const k of keys) {
      value = value?.[k];
    }
    return value || key;
  }, [appState.language]);

  // Effects
  useEffect(() => {
    const timer = setTimeout(() => {
      setLoading(false);
      if (appState.isAuthenticated && !currentProject) {
        setCurrentProject(productionData.projects[0]);
      }
    }, 800);
    return () => clearTimeout(timer);
  }, [appState.isAuthenticated, currentProject, productionData.projects]);

  useEffect(() => {
    if (appState.isAuthenticated && appState.currentUser) {
      const session = {
        currentUser: appState.currentUser,
        authToken: appState.authToken,
        rememberMe: appState.rememberMe,
        savedEmail: appState.savedEmail,
        timestamp: Date.now()
      };
      localStorage.setItem('cineprod_session', JSON.stringify(session));
    }
  }, [appState.isAuthenticated, appState.currentUser, appState.authToken, appState.rememberMe, appState.savedEmail]);

  useEffect(() => {
    const handleResize = () => {
      setSidebarOpen(window.innerWidth > 768);
    };
    handleResize();
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Funções auxiliares
  const addNotification = useCallback((notification) => {
    const newNotif = {
      id: Date.now() + Math.random(),
      ...notification,
      timestamp: new Date(),
      unread: true
    };
    setNotifications(prev => [newNotif, ...prev].slice(0, 50));
  }, []);

  const markNotificationAsRead = useCallback((id) => {
    setNotifications(prev => 
      prev.map(n => n.id === id ? { ...n, unread: false } : n)
    );
  }, []);

  const clearAllNotifications = useCallback(() => {
    setNotifications([]);
  }, []);

  const updateAppState = useCallback((updates) => {
    setAppState(prev => ({ ...prev, ...updates }));
  }, []);

  const handleLogout = useCallback(() => {
    localStorage.removeItem('cineprod_session');
    setAppState({
      language: 'pt',
      theme: 'light',
      currentUser: null,
      isAuthenticated: false,
      authToken: null,
      rememberMe: false,
      savedEmail: localStorage.getItem('cineprod_saved_email') || ''
    });
    setCurrentProject(null);
    setNotifications([]);
  }, []);

  // Loading Screen
  const LoadingScreen = () => (
    <div className="min-h-screen flex items-center justify-center" style={{ backgroundColor: '#f8f9fa' }}>
      <div className="text-center">
        <div className="relative w-24 h-24 mx-auto mb-6">
          <div className="absolute inset-0 border-4 border-blue-200 rounded-full animate-pulse"></div>
          <div className="absolute inset-0 border-4 border-transparent border-t-blue-600 rounded-full animate-spin" style={{ animation: 'spin 1s linear infinite' }}></div>
          <Film className="absolute inset-0 m-auto w-10 h-10 text-blue-600" />
        </div>
        <h2 className="text-xl font-semibold text-gray-800 mb-2">{t('loading')}</h2>
      </div>
    </div>
  );

  // Login Screen
  const LoginScreen = () => {
    const [email, setEmail] = useState(appState.savedEmail || '');
    const [password, setPassword] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const [rememberMe, setRememberMe] = useState(appState.rememberMe);
    const [errors, setErrors] = useState({});
    const [isLoading, setIsLoading] = useState(false);
    const [showDemoInfo, setShowDemoInfo] = useState(true);

    const validateEmail = (email) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

    const handleLogin = async (e) => {
      e?.preventDefault();
      setErrors({});
      setIsLoading(true);

      const newErrors = {};
      if (!email) newErrors.email = 'Email é obrigatório';
      else if (!validateEmail(email)) newErrors.email = 'Email inválido';
      if (!password) newErrors.password = 'Senha é obrigatória';

      if (Object.keys(newErrors).length > 0) {
        setErrors(newErrors);
        setIsLoading(false);
        return;
      }

      try {
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        const user = usersDatabase.find(u => u.email === email && u.password === password);
        
        if (!user) {
          throw new Error('Email ou senha inválidos');
        }
        
        const token = Math.random().toString(36).substring(2) + Date.now().toString(36);
        
        updateAppState({
          currentUser: user,
          isAuthenticated: true,
          authToken: token,
          rememberMe: rememberMe,
          savedEmail: rememberMe ? email : ''
        });
        
        setCurrentProject(productionData.projects[0]);
        
        addNotification({
          message: \`\${t('welcome')}, \${user.name}!\`,
          type: 'success',
          priority: 'high'
        });
      } catch (error) {
        setErrors({ general: error.message });
      } finally {
        setIsLoading(false);
      }
    };

    // Quick Login Function
    const quickLogin = (userKey) => {
      const user = usersDatabase.find(u => u.email === userKey + '@cineprod.com');
      if (user) {
        setEmail(user.email);
        setPassword(user.password);
        setTimeout(() => handleLogin(), 100);
      }
    };

    return (
      <div className="min-h-screen flex items-center justify-center" style={{
        backgroundColor: '#f8f9fa',
        backgroundImage: 'linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)'
      }}>
        <div className="bg-white p-8 rounded-lg shadow-xl w-full max-w-md">
          {/* Logo */}
          <div className="text-center mb-8">
            <div className="flex justify-center mb-4">
              <div style={{
                width: '60px',
                height: '60px',
                backgroundColor: 'var(--btn-primary-color)',
                borderRadius: '12px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                boxShadow: '0 4px 12px rgba(93, 120, 255, 0.3)'
              }}>
                <Film className="w-8 h-8 text-white" />
              </div>
            </div>
            <h1 className="text-2xl font-bold mb-2" style={{ color: 'var(--body-color)' }}>
              {t('appName')}
            </h1>
            <p className="text-gray-600">{t('tagline')}</p>
          </div>

          {/* Error Message */}
          {errors.general && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm flex items-start">
              <AlertCircle className="w-5 h-5 mr-2 flex-shrink-0 mt-0.5" />
              <span>{errors.general}</span>
            </div>
          )}

          {/* Quick Access Profiles */}
          <div className="mb-6">
            <p className="text-sm text-gray-600 mb-3 text-center">{t('selectProfile')}</p>
            <div className="grid grid-cols-2 gap-3">
              {Object.keys(usersDatabase).slice(0, 4).map((key) => {
                const user = usersDatabase[key];
                return (
                  <div
                    key={user.id}
                    onClick={() => quickLogin(user.email.split('@')[0])}
                    className="user-card flex items-center p-3 border rounded-lg hover:border-blue-500"
                  >
                    <div style={{
                      width: '40px',
                      height: '40px',
                      backgroundColor: 'var(--btn-primary-color)',
                      color: 'white',
                      borderRadius: '50%',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      fontSize: '14px',
                      fontWeight: '600',
                      marginRight: '12px'
                    }}>
                      {user.avatar}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="font-medium text-sm truncate" style={{ color: 'var(--body-color)' }}>
                        {user.name.split(' ')[0]}
                      </div>
                      <div className="text-xs text-gray-500 truncate">{user.role}</div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Divider */}
          <div className="relative my-6">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-gray-300"></div>
            </div>
            <div className="relative flex justify-center text-xs">
              <span className="px-2 bg-white text-gray-500">ou entre com suas credenciais</span>
            </div>
          </div>

          {/* Login Form */}
          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1" style={{ color: 'var(--body-color)' }}>
                {t('email')}
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className={\`sb-input w-full \${errors.email ? 'border-red-500' : ''}\`}
                placeholder="seu@email.com"
              />
              {errors.email && <p className="mt-1 text-sm text-red-500">{errors.email}</p>}
            </div>

            <div>
              <label className="block text-sm font-medium mb-1" style={{ color: 'var(--body-color)' }}>
                {t('password')}
              </label>
              <div className="relative">
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className={\`sb-input w-full pr-10 \${errors.password ? 'border-red-500' : ''}\`}
                  placeholder="••••••••"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500"
                >
                  {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
              {errors.password && <p className="mt-1 text-sm text-red-500">{errors.password}</p>}
            </div>

            <div className="flex items-center justify-between">
              <label className="flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={rememberMe}
                  onChange={(e) => setRememberMe(e.target.checked)}
                  className="mr-2"
                />
                <span className="text-sm" style={{ color: 'var(--body-color)' }}>{t('rememberMe')}</span>
              </label>
              <button type="button" className="text-sm" style={{ color: 'var(--link-color)' }}>
                {t('forgotPassword')}?
              </button>
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="sb-btn-primary w-full"
            >
              {isLoading ? (
                <span className="flex items-center justify-center">
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                  Entrando...
                </span>
              ) : (
                t('login')
              )}
            </button>
          </form>

          {/* Demo Info */}
          {showDemoInfo && (
            <div className="mt-6 p-4 bg-blue-50 rounded-lg relative border border-blue-200">
              <button
                onClick={() => setShowDemoInfo(false)}
                className="absolute top-2 right-2 text-blue-400 hover:text-blue-600"
              >
                <X className="w-4 h-4" />
              </button>
              <p className="text-xs font-bold text-blue-800 mb-2 flex items-center">
                <Info className="w-4 h-4 mr-1" />
                💡 Clique em qualquer perfil acima para acesso rápido
              </p>
              <p className="text-xs text-blue-600 italic mt-2">
                Ou use: sofia/marcus/luna/rio@cineprod.com
              </p>
              <p className="text-xs text-blue-600">
                Senhas: director123, producer123, dp123, talent123
              </p>
            </div>
          )}

          {/* Footer */}
          <div className="mt-6 text-center">
            <p className="text-xs text-gray-500">
              Powered by CineProd Systems © 2024
            </p>
          </div>
        </div>
      </div>
    );
  };

  // Sidebar Component
  const Sidebar = () => {
    const menuItems = [
      { id: 'dashboard', label: t('modules.dashboard'), icon: Home },
      { id: 'projects', label: t('modules.projects'), icon: Film },
      { id: 'calendar', label: t('modules.calendar'), icon: Calendar },
      { id: 'callsheets', label: t('modules.callsheets'), icon: Clapperboard },
      { id: 'schedule', label: t('modules.schedule'), icon: Clock },
      { id: 'breakdown', label: t('modules.breakdown'), icon: Layers },
      { id: 'crew', label: t('modules.crew'), icon: Users },
      { id: 'documents', label: t('modules.documents'), icon: FolderOpen },
      { id: 'tasks', label: t('modules.tasks'), icon: CheckCircle },
      { id: 'budget', label: t('modules.budget'), icon: DollarSign },
      { id: 'reports', label: t('modules.reports'), icon: BarChart2 },
      { id: 'contacts', label: t('modules.contacts'), icon: Phone },
      { id: 'stripboard', label: t('modules.stripboard'), icon: Grid },
      { id: 'communication', label: t('modules.communication'), icon: MessageCircle },
      { id: 'postproduction', label: t('modules.postproduction'), icon: Video }
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
        flexDirection: 'column',
        overflowY: 'auto'
      }}>
        {/* Logo */}
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
              <span className="text-white font-semibold">{t('appName').split(' ')[0]}</span>
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
            const isActive = activeModule === item.id;
            
            return (
              <button
                key={item.id}
                onClick={() => setActiveModule(item.id)}
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
                className="hover:bg-white hover:bg-opacity-5"
              >
                <Icon className="w-5 h-5 flex-shrink-0" />
                {sidebarOpen && <span className="ml-3">{item.label}</span>}
              </button>
            );
          })}
        </nav>

        {/* Project Info */}
        {currentProject && sidebarOpen && (
          <div style={{
            padding: '16px',
            borderTop: '1px solid rgba(255,255,255,0.1)',
            color: 'rgba(255,255,255,0.8)'
          }}>
            <div className="text-xs mb-2">Projeto Ativo</div>
            <div className="font-semibold text-sm mb-2 text-white">{currentProject.title}</div>
            <div className="flex justify-between text-xs mb-1">
              <span>Dia {currentProject.completedDays}/{currentProject.shootingDays}</span>
              <span>{currentProject.progress}%</span>
            </div>
            <div style={{
              width: '100%',
              backgroundColor: 'rgba(255,255,255,0.2)',
              borderRadius: '4px',
              height: '4px'
            }}>
              <div style={{
                width: \`\${currentProject.progress}%\`,
                backgroundColor: 'var(--btn-primary-color)',
                height: '100%',
                borderRadius: '4px',
                transition: 'width 0.3s ease'
              }}></div>
            </div>
          </div>
        )}

        {/* Toggle Button */}
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
            className="hover:bg-white hover:bg-opacity-10"
          >
            <Menu className="w-5 h-5" />
          </button>
        </div>
      </div>
    );
  };

  // TopBar Component
  const TopBar = () => {
    const unreadNotifications = notifications.filter(n => n.unread).length;

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
              placeholder={t('search') + " projetos, contatos, documentos..."}
              value={globalSearch}
              onChange={(e) => setGlobalSearch(e.target.value)}
              className="sb-input w-full pl-10"
            />
          </div>
        </div>

        {/* Right Actions */}
        <div className="flex items-center space-x-4 ml-auto">
          {/* Language Switcher */}
          <div className="flex bg-gray-100 rounded p-1">
            <button
              className={\`px-2 py-1 rounded text-xs transition-all \${
                appState.language === 'pt' ? 'bg-white shadow-sm' : ''
              }\`}
              onClick={() => updateAppState({ language: 'pt' })}
            >
              PT
            </button>
            <button
              className={\`px-2 py-1 rounded text-xs transition-all \${
                appState.language === 'en' ? 'bg-white shadow-sm' : ''
              }\`}
              onClick={() => updateAppState({ language: 'en' })}
            >
              EN
            </button>
          </div>

          {/* Notifications */}
          <div className="relative">
            <button
              onClick={() => setNotificationsOpen(!notificationsOpen)}
              className="relative p-2 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <Bell className="w-5 h-5 text-gray-600" />
              {unreadNotifications > 0 && (
                <span style={{
                  position: 'absolute',
                  top: '4px',
                  right: '4px',
                  width: '18px',
                  height: '18px',
                  backgroundColor: 'var(--btn-accent-color)',
                  borderRadius: '50%',
                  fontSize: '10px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'white',
                  fontWeight: 'bold'
                }}>
                  {unreadNotifications}
                </span>
              )}
            </button>

            {notificationsOpen && (
              <div style={{
                position: 'absolute',
                right: 0,
                top: '100%',
                marginTop: '8px',
                width: '360px',
                backgroundColor: 'white',
                borderRadius: '8px',
                boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
                border: '1px solid var(--input-border-color)',
                zIndex: 1000
              }}>
                <div className="p-4 border-b flex justify-between items-center">
                  <h3 className="font-semibold">{t('notifications')}</h3>
                  <button
                    onClick={clearAllNotifications}
                    className="text-sm text-blue-600 hover:text-blue-700"
                  >
                    Limpar
                  </button>
                </div>
                <div className="max-h-96 overflow-y-auto">
                  {notifications.length === 0 ? (
                    <div className="p-8 text-center text-gray-500">
                      <Bell className="w-12 h-12 mx-auto mb-3 text-gray-300" />
                      <p>Nenhuma notificação</p>
                    </div>
                  ) : (
                    notifications.slice(0, 10).map(notification => (
                      <div
                        key={notification.id}
                        onClick={() => markNotificationAsRead(notification.id)}
                        className={\`p-4 border-b hover:bg-gray-50 cursor-pointer \${
                          notification.unread ? 'bg-blue-50' : ''
                        }\`}
                      >
                        <div className="flex justify-between items-start">
                          <div className="flex-1">
                            <p className="text-sm">{notification.message}</p>
                            <p className="text-xs text-gray-500 mt-1">
                              {new Date(notification.timestamp).toLocaleString('pt-BR')}
                            </p>
                          </div>
                          {notification.unread && (
                            <div style={{
                              width: '8px',
                              height: '8px',
                              backgroundColor: 'var(--btn-primary-color)',
                              borderRadius: '50%',
                              marginLeft: '8px',
                              marginTop: '4px'
                            }}></div>
                          )}
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </div>
            )}
          </div>

          {/* Help */}
          <button className="p-2 hover:bg-gray-100 rounded-lg transition-colors">
            <HelpCircle className="w-5 h-5 text-gray-600" />
          </button>

          {/* User Menu */}
          <div className="relative">
            <button
              onClick={() => setUserMenuOpen(!userMenuOpen)}
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
                {appState.currentUser?.avatar}
              </div>
              <div className="text-left hidden md:block">
                <div className="text-sm font-medium" style={{ color: 'var(--body-color)' }}>
                  {appState.currentUser?.name.split(' ')[0]}
                </div>
                <div className="text-xs text-gray-500">{appState.currentUser?.role}</div>
              </div>
              <ChevronDown className="w-4 h-4 text-gray-500" />
            </button>

            {userMenuOpen && (
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
                <div className="p-4 border-b">
                  <div className="font-medium" style={{ color: 'var(--body-color)' }}>
                    {appState.currentUser?.name}
                  </div>
                  <div className="text-sm text-gray-500">{appState.currentUser?.email}</div>
                  <div className="text-xs text-gray-400 mt-1">{appState.currentUser?.department}</div>
                </div>
                <div className="py-2">
                  <button
                    onClick={() => {
                      setActiveModule('profile');
                      setUserMenuOpen(false);
                    }}
                    className="w-full px-4 py-2 text-left hover:bg-gray-50 flex items-center space-x-3"
                  >
                    <User className="w-4 h-4 text-gray-500" />
                    <span className="text-sm">{t('myProfile')}</span>
                  </button>
                  <button className="w-full px-4 py-2 text-left hover:bg-gray-50 flex items-center space-x-3">
                    <Settings className="w-4 h-4 text-gray-500" />
                    <span className="text-sm">{t('accountSettings')}</span>
                  </button>
                  <button className="w-full px-4 py-2 text-left hover:bg-gray-50 flex items-center space-x-3">
                    <HelpCircle className="w-4 h-4 text-gray-500" />
                    <span className="text-sm">{t('help')}</span>
                  </button>
                  <hr className="my-2" />
                  <button
                    onClick={handleLogout}
                    className="w-full px-4 py-2 text-left hover:bg-gray-50 flex items-center space-x-3 text-red-600"
                  >
                    <LogOut className="w-4 h-4" />
                    <span className="text-sm">{t('logout')}</span>
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
      { label: 'Projetos Ativos', value: appState.currentUser?.projects || 0, icon: Film, color: 'var(--btn-primary-color)' },
      { label: 'Folhas de Chamada', value: productionData.callSheets.length, icon: Clapperboard, color: 'var(--btn-accent-color)' },
      { label: 'Tarefas Pendentes', value: productionData.tasks.filter(t => t.status === 'pending').length, icon: CheckCircle, color: '#f59e0b' },
      { label: 'Membros da Equipe', value: productionData.crew.length, icon: Users, color: '#10b981' }
    ];

    return (
      <div>
        {/* Welcome */}
        <div className="mb-8">
          <h1 className="text-2xl font-bold mb-2" style={{ color: 'var(--body-color)' }}>
            {t('welcome')}, {appState.currentUser?.name}!
          </h1>
          <p className="text-gray-600">
            {currentProject && (
              \`\${t('productionDay')} \${currentProject.completedDays} \${t('of')} \${currentProject.shootingDays} - \${currentProject.title}\`
            )}
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
                    backgroundColor: \`\${stat.color}20\`,
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

        {/* Quick Actions */}
        <div className="mb-8">
          <h2 className="text-lg font-semibold mb-4" style={{ color: 'var(--body-color)' }}>
            {t('newCallSheet')} Rápidas
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { id: 'callsheets', label: t('newCallSheet'), icon: Clapperboard, color: 'blue' },
              { id: 'reports', label: t('viewReports'), icon: BarChart2, color: 'green' },
              { id: 'crew', label: t('manageCrew'), icon: Users, color: 'purple' },
              { id: 'calendar', label: t('viewSchedule'), icon: Calendar, color: 'orange' }
            ].map((action) => {
              const Icon = action.icon;
              return (
                <button
                  key={action.id}
                  onClick={() => setActiveModule(action.id)}
                  className="bg-white p-6 rounded-lg shadow-sm hover:shadow-md transition-all border group"
                  style={{ borderColor: 'var(--input-border-color)' }}
                >
                  <div className="flex flex-col items-center text-center">
                    <div className={\`w-12 h-12 bg-\${action.color}-100 rounded-full flex items-center justify-center mb-3 group-hover:scale-110 transition-transform\`}>
                      <Icon className={\`w-6 h-6 text-\${action.color}-600\`} />
                    </div>
                    <h3 className="font-medium text-sm" style={{ color: 'var(--body-color)' }}>{action.label}</h3>
                  </div>
                </button>
              );
            })}
          </div>
        </div>

        {/* Recent Projects */}
        {productionData.projects.length > 0 && (
          <div className="bg-white rounded-lg shadow-sm" style={{
            border: '1px solid var(--input-border-color)'
          }}>
            <div className="p-6 border-b" style={{ borderColor: 'var(--input-border-color)' }}>
              <h2 className="text-lg font-semibold" style={{ color: 'var(--body-color)' }}>
                {t('modules.projects')} Recentes
              </h2>
            </div>
            <div className="p-6">
              <div className="space-y-4">
                {productionData.projects.map(project => (
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
                          {project.title}
                        </h3>
                        <p className="text-sm text-gray-500">{project.status}</p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-4">
                      <div className="text-right">
                        <div className="text-sm font-medium" style={{ color: 'var(--body-color)' }}>
                          {project.progress}%
                        </div>
                        <div className="text-xs text-gray-500">
                          Dia {project.completedDays}/{project.shootingDays}
                        </div>
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
        )}
      </div>
    );
  };

  // Generic Module Component
  const GenericModule = ({ title, icon: Icon }) => {
    return (
      <div className="bg-white rounded-lg shadow-sm p-6" style={{
        border: '1px solid var(--input-border-color)'
      }}>
        <div className="flex items-center mb-4">
          <Icon className="w-6 h-6 mr-3" style={{ color: 'var(--btn-primary-color)' }} />
          <h2 className="text-xl font-semibold" style={{ color: 'var(--body-color)' }}>
            {title}
          </h2>
        </div>
        <p className="text-gray-600">
          Módulo em desenvolvimento. Em breve você terá acesso completo a todas as funcionalidades.
        </p>
        <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
          <p className="text-sm text-blue-800">
            ✨ Esta seção incluirá ferramentas avançadas de gestão de produção cinematográfica.
          </p>
        </div>
      </div>
    );
  };

  // Profile Component
  const ProfileModule = () => {
    return (
      <div className="bg-white rounded-lg shadow-sm p-6" style={{
        border: '1px solid var(--input-border-color)'
      }}>
        <h2 className="text-xl font-semibold mb-6" style={{ color: 'var(--body-color)' }}>
          {t('myProfile')}
        </h2>
        <div className="space-y-6">
          <div className="flex items-center gap-6">
            <div style={{
              width: '80px',
              height: '80px',
              backgroundColor: 'var(--btn-primary-color)',
              color: 'white',
              borderRadius: '50%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '32px',
              fontWeight: '600'
            }}>
              {appState.currentUser?.avatar}
            </div>
            <div>
              <h3 className="text-xl font-bold" style={{ color: 'var(--body-color)' }}>
                {appState.currentUser?.name}
              </h3>
              <p className="text-gray-600">{appState.currentUser?.email}</p>
              <div className="flex gap-2 mt-2">
                <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">
                  {appState.currentUser?.role}
                </span>
                <span className="px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm font-medium">
                  {appState.currentUser?.department}
                </span>
              </div>
            </div>
          </div>
          
          <div className="grid grid-cols-3 gap-4 pt-6 border-t" style={{ borderColor: 'var(--input-border-color)' }}>
            <div className="text-center">
              <div className="text-2xl font-bold" style={{ color: 'var(--btn-primary-color)' }}>
                {appState.currentUser?.projects || 0}
              </div>
              <div className="text-sm text-gray-600">Projetos</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold" style={{ color: 'var(--btn-primary-color)' }}>
                {productionData.tasks.filter(t => t.assignee === appState.currentUser?.name).length}
              </div>
              <div className="text-sm text-gray-600">Tarefas</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold" style={{ color: 'var(--btn-primary-color)' }}>
                {currentProject?.completedDays || 0}
              </div>
              <div className="text-sm text-gray-600">Dias Trabalhados</div>
            </div>
          </div>
        </div>
      </div>
    );
  };

  // Render Module
  const renderModule = () => {
    switch (activeModule) {
      case 'dashboard':
        return <Dashboard />;
      case 'profile':
        return <ProfileModule />;
      case 'projects':
        return <GenericModule title={t('modules.projects')} icon={Film} />;
      case 'calendar':
        return <GenericModule title={t('modules.calendar')} icon={Calendar} />;
      case 'callsheets':
        return <GenericModule title={t('modules.callsheets')} icon={Clapperboard} />;
      case 'schedule':
        return <GenericModule title={t('modules.schedule')} icon={Clock} />;
      case 'breakdown':
        return <GenericModule title={t('modules.breakdown')} icon={Layers} />;
      case 'crew':
        return <GenericModule title={t('modules.crew')} icon={Users} />;
      case 'documents':
        return <GenericModule title={t('modules.documents')} icon={FolderOpen} />;
      case 'tasks':
        return <GenericModule title={t('modules.tasks')} icon={CheckCircle} />;
      case 'budget':
        return <GenericModule title={t('modules.budget')} icon={DollarSign} />;
      case 'reports':
        return <GenericModule title={t('modules.reports')} icon={BarChart2} />;
      case 'contacts':
        return <GenericModule title={t('modules.contacts')} icon={Phone} />;
      case 'stripboard':
        return <GenericModule title={t('modules.stripboard')} icon={Grid} />;
      case 'communication':
        return <GenericModule title={t('modules.communication')} icon={MessageCircle} />;
      case 'postproduction':
        return <GenericModule title={t('modules.postproduction')} icon={Video} />;
      default:
        return <Dashboard />;
    }
  };

  // Main Layout
  const MainLayout = () => {
    return (
      <div className="min-h-screen" style={{ backgroundColor: '#f8f9fa' }}>
        <Sidebar />
        <TopBar />
        
        <main style={{
          marginLeft: sidebarOpen ? '240px' : '60px',
          marginTop: '60px',
          padding: '24px',
          transition: 'margin-left 0.3s ease',
          minHeight: 'calc(100vh - 60px)'
        }}>
          {renderModule()}
        </main>
      </div>
    );
  };

  // Render
  if (loading) return <LoadingScreen />;
  if (!appState.isAuthenticated) return <LoginScreen />;
  return <MainLayout />;
};

// App Principal
export default function App() {
  return (
    <ModalProvider>
      <CineProductionSystem />
    </ModalProvider>
  );
}
