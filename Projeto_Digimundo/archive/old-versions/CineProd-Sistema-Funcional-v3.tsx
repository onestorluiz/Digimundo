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
const customStyles = `
  :root {
    --btn-primary-color: #5d78ff;
    --btn-primary-color-hover: #384ad7;
    --btn-accent-color: #FA1870;
    --nav-logged-in-bg-color: #1D1E2C;
    --link-sidebar-color: #5d78ff;
    --link-nav-bar-color: #A2A3B7;
    --input-border-color: #D8E0E6;
    --body-color: #1B1C21;
  }
  
  @keyframes fade-in {
    from { opacity: 0; }
    to { opacity: 1; }
  }
  
  @keyframes scale-in {
    from { 
      opacity: 0;
      transform: scale(0.95);
    }
    to { 
      opacity: 1;
      transform: scale(1);
    }
  }
  
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
  
  .animate-fade-in {
    animation: fade-in 0.3s ease-out;
  }
  
  .animate-scale-in {
    animation: scale-in 0.3s ease-out;
  }
  
  .user-card {
    transition: all 0.2s ease;
    cursor: pointer;
  }
  
  .user-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(93, 120, 255, 0.3);
  }
`;

// Injetar estilos
if (typeof document !== 'undefined') {
  const styleElement = document.createElement('style');
  styleElement.textContent = customStyles;
  document.head.appendChild(styleElement);
}

// Contextos
const AuthContext = createContext(null);
const NotificationContext = createContext(null);
const AppStateContext = createContext(null);
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

// Custom Hooks
const useModal = () => {
  const context = useContext(ModalContext);
  if (!context) throw new Error('useModal must be used within ModalProvider');
  return context;
};

// Sistema Principal
const ProductionManagementSystem = () => {
  // Estados Globais
  const [appState, setAppState] = useState(() => {
    // Tentar carregar sessão salva do localStorage
    const savedSession = localStorage.getItem('cineprod_session');
    if (savedSession) {
      try {
        const session = JSON.parse(savedSession);
        // Verificar se a sessão não expirou (24 horas)
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
    
    // Estado inicial padrão
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

  // Banco de dados de usuários (simulado)
  const usersDatabase = [
    {
      id: 1,
      name: 'Sofia Luz',
      email: 'sofia@cineprod.com',
      password: 'director123',
      role: 'Director',
      avatar: 'SL',
      twoFactorEnabled: false
    },
    {
      id: 2,
      name: 'Marcus Terra',
      email: 'marcus@cineprod.com',
      password: 'producer123',
      role: 'Producer',
      avatar: 'MT',
      twoFactorEnabled: false
    },
    {
      id: 3,
      name: 'Luna Sombra',
      email: 'luna@cineprod.com',
      password: 'dp123',
      role: 'DP',
      avatar: 'LS',
      twoFactorEnabled: false
    },
    {
      id: 4,
      name: 'Rio Vento',
      email: 'rio@cineprod.com',
      password: 'talent123',
      role: 'Talent',
      avatar: 'RV',
      twoFactorEnabled: false
    },
    {
      id: 5,
      name: 'Admin Demo',
      email: 'admin@cineprod.com',
      password: 'admin123',
      role: 'Administrator',
      avatar: 'AD',
      twoFactorEnabled: true
    }
  ];

  // Dados de produção
  const [productionData] = useState({
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
        dop: 'Luna Sombra'
      },
      {
        id: 2,
        title: 'Série Urban',
        type: 'TV Series',
        budget: 8000000,
        spent: 4800000,
        startDate: '2024-02-01',
        endDate: '2024-06-30',
        shootingDays: 90,
        completedDays: 54,
        director: 'Sofia Luz',
        producer: 'Marcus Terra',
        dop: 'Luna Sombra'
      },
      {
        id: 3,
        title: 'Campanha Nexus',
        type: 'Commercial',
        budget: 2500000,
        spent: 1625000,
        startDate: '2024-01-15',
        endDate: '2024-03-30',
        shootingDays: 45,
        completedDays: 29,
        director: 'Sofia Luz',
        producer: 'Marcus Terra',
        dop: 'Luna Sombra'
      }
    ]
  });

  // Sistema de Tradução Completo
  const translations = {
    pt: {
      // Auth
      login: 'Entrar',
      logout: 'Sair',
      email: 'Email',
      password: 'Senha',
      rememberMe: 'Lembrar de mim',
      forgotPassword: 'Esqueceu a senha?',
      createAccount: 'Criar conta',
      or: 'ou',
      loginWith: 'Entrar com',
      twoFactorAuth: 'Autenticação de dois fatores',
      enterCode: 'Digite o código',
      verify: 'Verificar',
      resendCode: 'Reenviar código',
      invalidCredentials: 'Email ou senha inválidos',
      resetPassword: 'Redefinir Senha',
      resetPasswordText: 'Digite seu email para receber as instruções de redefinição de senha.',
      sendInstructions: 'Enviar Instruções',
      backToLogin: 'Voltar ao Login',
      createNewAccount: 'Criar Nova Conta',
      fullName: 'Nome Completo',
      confirmPassword: 'Confirmar Senha',
      agreeTerms: 'Concordo com os termos de uso',
      alreadyHaveAccount: 'Já tem uma conta?',
      profile: 'Perfil',
      myProfile: 'Meu Perfil',
      accountSettings: 'Configurações da Conta',
      help: 'Ajuda',
      
      // Sistema
      appName: 'CineProd Systems',
      tagline: 'Gestão Profissional de Produção Cinematográfica',
      welcome: 'Bem-vindo de volta',
      selectProfile: 'Selecione seu perfil para continuar',
      loading: 'Carregando sistema...',
      saving: 'Salvando...',
      saved: 'Salvo',
      
      // Modules
      modules: {
        dashboard: 'Painel',
        callsheets: 'Folhas de Chamada',
        schedule: 'Cronograma',
        stripboard: 'Stripboard',
        breakdown: 'Decupagem',
        crew: 'Elenco e Equipe',
        documents: 'Documentos',
        tasks: 'Tarefas',
        budget: 'Orçamento',
        reports: 'Relatórios',
        communication: 'Comunicação',
        postproduction: 'Pós-produção',
        dood: 'DOOD',
        admin: 'Administração',
        analytics: 'Analytics',
        inventory: 'Inventário',
        profile: 'Perfil',
        settings: 'Configurações'
      },
      
      // Dashboard
      productionDay: 'Dia de Produção',
      of: 'de',
      budgetUsed: 'Orçamento Usado',
      dailyBurnRate: 'Gasto Diário',
      pagesPerDay: 'Páginas/Dia',
      crewAttendance: 'Presença da Equipe',
      scriptCoverage: 'Cobertura do Roteiro',
      productionEfficiency: 'Eficiência de Produção',
      setupsDay: 'Setups/Dia',
      overtime: 'Hora Extra',
      financialHealth: 'Saúde Financeira',
      variance: 'Variância',
      contingency: 'Contingência',
      crewMetrics: 'Métricas da Equipe',
      safetyIncidents: 'Incidentes',
      equipmentUse: 'Uso de Equip.',
      creativeProgress: 'Progresso Criativo',
      vfxProgress: 'Progresso VFX',
      adrNeeded: 'ADR Necessário',
      systemAlerts: 'Alertas do Sistema',
      weatherAlert: 'Alerta de Tempo',
      rainChance: 'Chance de chuva: 80%. Considere alternativas internas.',
      turnaroundRisk: 'Risco de Violação de Descanso',
      crewRestWarning: '3 membros da equipe próximos do período mínimo.',
      upcomingDeadlines: 'Prazos Próximos',
      recentActivity: 'Atividade Recente',
      quickActions: 'Ações Rápidas',
      newCallSheet: 'Nova Folha',
      viewReports: 'Ver Relatórios',
      manageCrew: 'Gerenciar Equipe',
      viewSchedule: 'Ver Cronograma',
      
      // Common
      save: 'Salvar',
      cancel: 'Cancelar',
      delete: 'Excluir',
      edit: 'Editar',
      new: 'Novo',
      search: 'Buscar',
      filter: 'Filtrar',
      export: 'Exportar',
      import: 'Importar',
      status: 'Status',
      priority: 'Prioridade',
      notifications: 'Notificações',
      settings: 'Configurações',
      close: 'Fechar'
    },
    en: {
      // Auth
      login: 'Login',
      logout: 'Logout',
      email: 'Email',
      password: 'Password',
      rememberMe: 'Remember me',
      forgotPassword: 'Forgot password?',
      createAccount: 'Create account',
      or: 'or',
      loginWith: 'Login with',
      twoFactorAuth: 'Two-factor authentication',
      enterCode: 'Enter code',
      verify: 'Verify',
      resendCode: 'Resend code',
      invalidCredentials: 'Invalid email or password',
      resetPassword: 'Reset Password',
      resetPasswordText: 'Enter your email to receive password reset instructions.',
      sendInstructions: 'Send Instructions',
      backToLogin: 'Back to Login',
      createNewAccount: 'Create New Account',
      fullName: 'Full Name',
      confirmPassword: 'Confirm Password',
      agreeTerms: 'I agree to the terms of use',
      alreadyHaveAccount: 'Already have an account?',
      profile: 'Profile',
      myProfile: 'My Profile',
      accountSettings: 'Account Settings',
      help: 'Help',
      
      // System
      appName: 'CineProd Systems',
      tagline: 'Professional Film Production Management',
      welcome: 'Welcome back',
      selectProfile: 'Select your profile to continue',
      loading: 'Loading system...',
      saving: 'Saving...',
      saved: 'Saved',
      
      // Modules
      modules: {
        dashboard: 'Dashboard',
        callsheets: 'Call Sheets',
        schedule: 'Schedule',
        stripboard: 'Stripboard',
        breakdown: 'Script Breakdown',
        crew: 'Cast & Crew',
        documents: 'Documents',
        tasks: 'Tasks',
        budget: 'Budget',
        reports: 'Reports',
        communication: 'Communication',
        postproduction: 'Post-production',
        dood: 'DOOD',
        admin: 'Administration',
        analytics: 'Analytics',
        inventory: 'Inventory',
        profile: 'Profile',
        settings: 'Settings'
      },
      
      // Dashboard
      productionDay: 'Production Day',
      of: 'of',
      budgetUsed: 'Budget Used',
      dailyBurnRate: 'Daily Burn Rate',
      pagesPerDay: 'Pages/Day',
      crewAttendance: 'Crew Attendance',
      scriptCoverage: 'Script Coverage',
      productionEfficiency: 'Production Efficiency',
      setupsDay: 'Setups/Day',
      overtime: 'Overtime',
      financialHealth: 'Financial Health',
      variance: 'Variance',
      contingency: 'Contingency',
      crewMetrics: 'Crew Metrics',
      safetyIncidents: 'Safety Incidents',
      equipmentUse: 'Equipment Use',
      creativeProgress: 'Creative Progress',
      vfxProgress: 'VFX Progress',
      adrNeeded: 'ADR Needed',
      systemAlerts: 'System Alerts',
      weatherAlert: 'Weather Alert',
      rainChance: '80% chance of rain. Consider indoor alternatives.',
      turnaroundRisk: 'Turnaround Violation Risk',
      crewRestWarning: '3 crew members approaching minimum rest period.',
      upcomingDeadlines: 'Upcoming Deadlines',
      recentActivity: 'Recent Activity',
      quickActions: 'Quick Actions',
      newCallSheet: 'New Call Sheet',
      viewReports: 'View Reports',
      manageCrew: 'Manage Crew',
      viewSchedule: 'View Schedule',
      
      // Common
      save: 'Save',
      cancel: 'Cancel',
      delete: 'Delete',
      edit: 'Edit',
      new: 'New',
      search: 'Search',
      filter: 'Filter',
      export: 'Export',
      import: 'Import',
      status: 'Status',
      priority: 'Priority',
      notifications: 'Notifications',
      settings: 'Settings',
      close: 'Close'
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
    // Simular carregamento inicial
    const timer = setTimeout(() => {
      setLoading(false);
      if (appState.isAuthenticated && !currentProject) {
        setCurrentProject(productionData.projects[0]);
      }
    }, 800);
    
    return () => clearTimeout(timer);
  }, [appState.isAuthenticated, currentProject, productionData.projects]);

  // Salvar sessão quando autenticar
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
      
      if (appState.rememberMe) {
        localStorage.setItem('cineprod_saved_email', appState.savedEmail);
      }
    }
  }, [appState.isAuthenticated, appState.currentUser, appState.authToken, appState.rememberMe, appState.savedEmail]);

  // Sistema de notificações
  useEffect(() => {
    if (!appState.isAuthenticated) return;

    const notificationInterval = setInterval(() => {
      const randomNotifications = [
        { 
          message: 'Nova folha de chamada disponível', 
          type: 'info',
          module: 'callsheets',
          priority: 'normal'
        },
        { 
          message: 'Orçamento atualizado por Marcus Terra', 
          type: 'success',
          module: 'budget',
          priority: 'normal'
        },
        { 
          message: 'Prazo próximo: Revisar cena 5', 
          type: 'warning',
          module: 'tasks',
          priority: 'high'
        }
      ];

      if (Math.random() > 0.8) {
        const notif = randomNotifications[Math.floor(Math.random() * randomNotifications.length)];
        addNotification(notif);
      }
    }, 30000);

    return () => clearInterval(notificationInterval);
  }, [appState.isAuthenticated]);

  // Detectar redimensionamento
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
    addNotification({
      message: 'Você saiu do sistema com sucesso',
      type: 'info',
      priority: 'normal'
    });
  }, []);

  // Componente de Loading
  const LoadingScreen = () => (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-purple-50">
      <div className="text-center">
        <div className="relative w-24 h-24 mx-auto mb-6">
          <div className="absolute inset-0 border-4 border-blue-200 rounded-full animate-pulse"></div>
          <div className="absolute inset-0 border-4 border-transparent border-t-blue-600 rounded-full animate-spin"></div>
          <Film className="absolute inset-0 m-auto w-10 h-10 text-blue-600" />
        </div>
        <h2 className="text-xl font-semibold text-gray-800 mb-2">{t('loading')}</h2>
        <div className="flex justify-center gap-1">
          <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
          <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
          <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
        </div>
      </div>
    </div>
  );

  // Componente de Login
  const LoginScreen = () => {
    const [loginMode, setLoginMode] = useState('login');
    const [email, setEmail] = useState(appState.savedEmail || '');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [fullName, setFullName] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const [twoFactorCode, setTwoFactorCode] = useState(['', '', '', '', '', '']);
    const [errors, setErrors] = useState({});
    const [isLoading, setIsLoading] = useState(false);
    const [showDemoInfo, setShowDemoInfo] = useState(true);
    const [agreeTerms, setAgreeTerms] = useState(false);
    const [rememberMe, setRememberMe] = useState(appState.rememberMe);

    const validateEmail = (email) => {
      const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return re.test(email);
    };

    const handleLogin = async () => {
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
          throw new Error(t('invalidCredentials'));
        }
        
        if (user.twoFactorEnabled) {
          setLoginMode('twoFactor');
          setIsLoading(false);
        } else {
          completeLogin(user);
        }
      } catch (error) {
        setErrors({ general: error.message });
        setIsLoading(false);
      }
    };

    const handleCreateAccount = async () => {
      setErrors({});
      setIsLoading(true);

      const newErrors = {};
      if (!fullName) newErrors.fullName = 'Nome é obrigatório';
      if (!email) newErrors.email = 'Email é obrigatório';
      else if (!validateEmail(email)) newErrors.email = 'Email inválido';
      if (!password) newErrors.password = 'Senha é obrigatória';
      else if (password.length < 6) newErrors.password = 'Senha deve ter no mínimo 6 caracteres';
      if (password !== confirmPassword) newErrors.confirmPassword = 'Senhas não conferem';
      if (!agreeTerms) newErrors.agreeTerms = 'Você deve concordar com os termos';

      if (Object.keys(newErrors).length > 0) {
        setErrors(newErrors);
        setIsLoading(false);
        return;
      }

      try {
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        addNotification({
          message: 'Conta criada com sucesso! Faça login para continuar.',
          type: 'success',
          priority: 'high'
        });
        
        setLoginMode('login');
        setPassword('');
        setConfirmPassword('');
        setFullName('');
        setAgreeTerms(false);
      } catch (error) {
        setErrors({ general: 'Erro ao criar conta. Tente novamente.' });
      } finally {
        setIsLoading(false);
      }
    };

    const handleForgotPassword = async () => {
      setErrors({});
      setIsLoading(true);

      if (!email) {
        setErrors({ email: 'Email é obrigatório' });
        setIsLoading(false);
        return;
      }

      if (!validateEmail(email)) {
        setErrors({ email: 'Email inválido' });
        setIsLoading(false);
        return;
      }

      try {
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        addNotification({
          message: 'Instruções de redefinição de senha enviadas para seu email.',
          type: 'success',
          priority: 'high'
        });
        
        setLoginMode('login');
      } catch (error) {
        setErrors({ general: 'Erro ao enviar instruções. Tente novamente.' });
      } finally {
        setIsLoading(false);
      }
    };

    const completeLogin = (user) => {
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
        message: `${t('welcome')}, ${user.name}!`,
        type: 'success',
        priority: 'high'
      });
    };

    const handleTwoFactor = async () => {
      const code = twoFactorCode.join('');
      if (code.length !== 6) {
        setErrors({ twoFactor: 'Digite o código completo' });
        return;
      }

      setIsLoading(true);
      
      try {
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        if (code !== '123456') {
          throw new Error('Código inválido');
        }

        const user = usersDatabase.find(u => u.email === email);
        completeLogin(user);
      } catch (error) {
        setErrors({ twoFactor: error.message });
      } finally {
        setIsLoading(false);
      }
    };

    const handleTwoFactorInput = (index, value) => {
      if (!/^\d*$/.test(value)) return;
      
      const newCode = [...twoFactorCode];
      newCode[index] = value.slice(-1);
      setTwoFactorCode(newCode);
      
      if (value && index < 5) {
        const nextInput = document.getElementById(`code-${index + 1}`);
        nextInput?.focus();
      }
    };

    const handleSocialLogin = (provider) => {
      addNotification({
        message: `Login com ${provider} em desenvolvimento`,
        type: 'info',
        priority: 'normal'
      });
    };

    // Forgot Password Screen
    if (loginMode === 'forgotPassword') {
      return (
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-purple-50">
          <div className="bg-white p-8 rounded-2xl shadow-xl w-full max-w-md">
            <div className="text-center mb-8">
              <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl mx-auto mb-4 flex items-center justify-center shadow-lg">
                <Lock className="w-10 h-10 text-white" />
              </div>
              <h1 className="text-2xl font-bold mb-2">{t('resetPassword')}</h1>
              <p className="text-gray-600">{t('resetPasswordText')}</p>
            </div>

            {errors.general && (
              <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
                {errors.general}
              </div>
            )}

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  {t('email')}
                </label>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all ${
                    errors.email ? 'border-red-500' : 'border-gray-300'
                  }`}
                  placeholder="seu@email.com"
                />
                {errors.email && (
                  <p className="mt-1 text-sm text-red-500">{errors.email}</p>
                )}
              </div>

              <button
                onClick={handleForgotPassword}
                disabled={isLoading}
                className="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white py-3 rounded-lg font-medium hover:shadow-lg transform hover:-translate-y-0.5 transition-all disabled:opacity-50 disabled:transform-none"
              >
                {isLoading ? (
                  <span className="flex items-center justify-center">
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2" />
                    Enviando...
                  </span>
                ) : (
                  t('sendInstructions')
                )}
              </button>

              <button
                onClick={() => setLoginMode('login')}
                className="w-full text-blue-600 hover:text-blue-700 text-sm"
              >
                {t('backToLogin')}
              </button>
            </div>
          </div>
        </div>
      );
    }

    // Create Account Screen
    if (loginMode === 'createAccount') {
      return (
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-purple-50 py-8">
          <div className="bg-white p-8 rounded-2xl shadow-xl w-full max-w-md">
            <div className="text-center mb-8">
              <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl mx-auto mb-4 flex items-center justify-center shadow-lg">
                <UserPlus className="w-10 h-10 text-white" />
              </div>
              <h1 className="text-2xl font-bold mb-2">{t('createNewAccount')}</h1>
              <p className="text-gray-600">{t('tagline')}</p>
            </div>

            {errors.general && (
              <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
                {errors.general}
              </div>
            )}

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  {t('fullName')}
                </label>
                <input
                  type="text"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all ${
                    errors.fullName ? 'border-red-500' : 'border-gray-300'
                  }`}
                  placeholder="João Silva"
                />
                {errors.fullName && (
                  <p className="mt-1 text-sm text-red-500">{errors.fullName}</p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  {t('email')}
                </label>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all ${
                    errors.email ? 'border-red-500' : 'border-gray-300'
                  }`}
                  placeholder="seu@email.com"
                />
                {errors.email && (
                  <p className="mt-1 text-sm text-red-500">{errors.email}</p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  {t('password')}
                </label>
                <div className="relative">
                  <input
                    type={showPassword ? 'text' : 'password'}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className={`w-full px-4 py-3 pr-10 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all ${
                      errors.password ? 'border-red-500' : 'border-gray-300'
                    }`}
                    placeholder="••••••••"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700"
                  >
                    {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                  </button>
                </div>
                {errors.password && (
                  <p className="mt-1 text-sm text-red-500">{errors.password}</p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  {t('confirmPassword')}
                </label>
                <input
                  type="password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all ${
                    errors.confirmPassword ? 'border-red-500' : 'border-gray-300'
                  }`}
                  placeholder="••••••••"
                />
                {errors.confirmPassword && (
                  <p className="mt-1 text-sm text-red-500">{errors.confirmPassword}</p>
                )}
              </div>

              <div>
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={agreeTerms}
                    onChange={(e) => setAgreeTerms(e.target.checked)}
                    className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                  />
                  <span className="ml-2 text-sm text-gray-700">{t('agreeTerms')}</span>
                </label>
                {errors.agreeTerms && (
                  <p className="mt-1 text-sm text-red-500">{errors.agreeTerms}</p>
                )}
              </div>

              <button
                onClick={handleCreateAccount}
                disabled={isLoading || !agreeTerms}
                className="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white py-3 rounded-lg font-medium hover:shadow-lg transform hover:-translate-y-0.5 transition-all disabled:opacity-50 disabled:transform-none"
              >
                {isLoading ? (
                  <span className="flex items-center justify-center">
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2" />
                    Criando conta...
                  </span>
                ) : (
                  t('createAccount')
                )}
              </button>

              <p className="text-center text-sm text-gray-600">
                {t('alreadyHaveAccount')}{' '}
                <button
                  onClick={() => setLoginMode('login')}
                  className="text-blue-600 hover:text-blue-700 font-medium"
                >
                  {t('login')}
                </button>
              </p>
            </div>
          </div>
        </div>
      );
    }

    // Two Factor Screen
    if (loginMode === 'twoFactor') {
      return (
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-purple-50">
          <div className="bg-white p-8 rounded-2xl shadow-xl w-full max-w-md">
            <div className="text-center mb-8">
              <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl mx-auto mb-4 flex items-center justify-center shadow-lg">
                <Shield className="w-10 h-10 text-white" />
              </div>
              <h1 className="text-2xl font-bold mb-2">{t('twoFactorAuth')}</h1>
              <p className="text-gray-600">Digite o código enviado para seu dispositivo</p>
              <div className="mt-2 p-3 bg-blue-50 rounded-lg cursor-pointer hover:bg-blue-100 transition-colors"
                onClick={() => setTwoFactorCode(['1', '2', '3', '4', '5', '6'])}>
                <p className="text-sm text-blue-800">
                  🔐 Código de demonstração: <span className="font-bold">123456</span> (clique para preencher)
                </p>
              </div>
            </div>

            <div className="flex justify-center gap-2 mb-6">
              {twoFactorCode.map((digit, index) => (
                <input
                  key={index}
                  type="text"
                  maxLength="1"
                  value={digit}
                  onChange={(e) => handleTwoFactorInput(index, e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === 'Backspace' && !digit && index > 0) {
                      const prevInput = document.getElementById(`code-${index - 1}`);
                      prevInput?.focus();
                    }
                    if (e.key === 'Enter' && twoFactorCode.every(d => d)) {
                      handleTwoFactor();
                    }
                  }}
                  id={`code-${index}`}
                  className="w-12 h-12 text-center text-xl font-bold border-2 rounded-lg focus:border-blue-500 focus:outline-none transition-colors"
                />
              ))}
            </div>

            {errors.twoFactor && (
              <p className="text-red-500 text-sm text-center mb-4">{errors.twoFactor}</p>
            )}

            <button
              onClick={handleTwoFactor}
              disabled={isLoading || !twoFactorCode.every(d => d)}
              className="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white py-3 rounded-lg font-medium hover:shadow-lg transform hover:-translate-y-0.5 transition-all disabled:opacity-50 disabled:transform-none"
            >
              {isLoading ? (
                <span className="flex items-center justify-center">
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2" />
                  Verificando...
                </span>
              ) : (
                t('verify')
              )}
            </button>

            <button
              onClick={() => setLoginMode('login')}
              className="w-full mt-4 text-blue-600 hover:text-blue-700 text-sm"
            >
              {t('backToLogin')}
            </button>
          </div>
        </div>
      );
    }

    // Login Screen Principal
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-purple-50 p-4">
        <div className="bg-white p-8 rounded-2xl shadow-xl w-full max-w-md">
          <div className="text-center mb-8">
            <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl mx-auto mb-4 flex items-center justify-center shadow-lg transform hover:scale-105 transition-transform">
              <Film className="w-10 h-10 text-white" />
            </div>
            <h1 className="text-3xl font-bold mb-2 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              {t('appName')}
            </h1>
            <p className="text-gray-600">{t('tagline')}</p>
          </div>

          {errors.general && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm flex items-start">
              <AlertCircle className="w-5 h-5 mr-2 flex-shrink-0 mt-0.5" />
              <span>{errors.general}</span>
            </div>
          )}

          {/* Quick Access Cards */}
          <div className="mb-6">
            <p className="text-sm text-gray-600 mb-3 text-center">{t('selectProfile')}</p>
            <div className="grid grid-cols-2 gap-3">
              {usersDatabase.slice(0, 4).map((user) => (
                <div
                  key={user.id}
                  onClick={() => {
                    setEmail(user.email);
                    setPassword(user.password);
                    setTimeout(() => handleLogin(), 100);
                  }}
                  className="user-card flex items-center p-3 border border-gray-300 rounded-lg hover:border-blue-500 transition-all"
                >
                  <div style={{
                    width: '40px',
                    height: '40px',
                    backgroundColor: '#5d78ff',
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
                    <div className="font-medium text-sm truncate text-gray-900">
                      {user.name.split(' ')[0]}
                    </div>
                    <div className="text-xs text-gray-500 truncate">{user.role}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Divider */}
          <div className="relative mb-6">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-gray-300"></div>
            </div>
            <div className="relative flex justify-center text-xs">
              <span className="px-2 bg-white text-gray-500">ou entre com suas credenciais</span>
            </div>
          </div>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                {t('email')}
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleLogin()}
                className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all ${
                  errors.email ? 'border-red-500' : 'border-gray-300'
                }`}
                placeholder="seu@email.com"
              />
              {errors.email && (
                <p className="mt-1 text-sm text-red-500">{errors.email}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                {t('password')}
              </label>
              <div className="relative">
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleLogin()}
                  className={`w-full px-4 py-3 pr-10 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all ${
                    errors.password ? 'border-red-500' : 'border-gray-300'
                  }`}
                  placeholder="••••••••"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700"
                >
                  {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
              {errors.password && (
                <p className="mt-1 text-sm text-red-500">{errors.password}</p>
              )}
            </div>

            <div className="flex items-center justify-between">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={rememberMe}
                  onChange={(e) => setRememberMe(e.target.checked)}
                  className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                />
                <span className="ml-2 text-sm text-gray-700">{t('rememberMe')}</span>
              </label>
              <button
                onClick={() => setLoginMode('forgotPassword')}
                className="text-sm text-blue-600 hover:text-blue-700"
              >
                {t('forgotPassword')}?
              </button>
            </div>

            <button
              onClick={handleLogin}
              disabled={isLoading || !email || !password}
              className="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white py-3 rounded-lg font-medium hover:shadow-lg transform hover:-translate-y-0.5 transition-all disabled:opacity-50 disabled:transform-none"
            >
              {isLoading ? (
                <span className="flex items-center justify-center">
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2" />
                  Entrando...
                </span>
              ) : (
                t('login')
              )}
            </button>
          </div>

          <div className="mt-6 text-center">
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-gray-300"></div>
              </div>
              <div className="relative bg-white px-4 text-sm text-gray-500">
                {t('or')}
              </div>
            </div>
          </div>

          <div className="mt-6 grid grid-cols-2 gap-3">
            <button 
              onClick={() => handleSocialLogin('Google')}
              className="flex items-center justify-center px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <Globe className="w-5 h-5 mr-2" />
              Google
            </button>
            <button 
              onClick={() => handleSocialLogin('Apple')}
              className="flex items-center justify-center px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <Film className="w-5 h-5 mr-2" />
              Apple
            </button>
          </div>

          <p className="mt-6 text-center text-sm text-gray-600">
            Não tem uma conta?{' '}
            <button
              onClick={() => setLoginMode('createAccount')}
              className="text-blue-600 hover:text-blue-700 font-medium"
            >
              {t('createAccount')}
            </button>
          </p>

          {showDemoInfo && (
            <div className="mt-6 p-4 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg relative border border-blue-200">
              <button
                onClick={() => setShowDemoInfo(false)}
                className="absolute top-2 right-2 text-blue-400 hover:text-blue-600"
              >
                <X className="w-4 h-4" />
              </button>
              <p className="text-xs font-bold text-blue-800 mb-2 flex items-center">
                <Info className="w-4 h-4 mr-1" />
                🎬 Usuários de demonstração:
              </p>
              <div className="space-y-1.5 text-xs text-blue-700">
                <div className="flex items-center">
                  <CheckCircle className="w-3 h-3 mr-1 text-green-600" />
                  <strong>Diretor:</strong> sofia@cineprod.com / director123
                </div>
                <div className="flex items-center">
                  <CheckCircle className="w-3 h-3 mr-1 text-green-600" />
                  <strong>Produtor:</strong> marcus@cineprod.com / producer123
                </div>
                <div className="flex items-center">
                  <CheckCircle className="w-3 h-3 mr-1 text-green-600" />
                  <strong>DP:</strong> luna@cineprod.com / dp123
                </div>
                <div className="flex items-center">
                  <CheckCircle className="w-3 h-3 mr-1 text-green-600" />
                  <strong>Talento:</strong> rio@cineprod.com / talent123
                </div>
                <div className="flex items-center">
                  <Shield className="w-3 h-3 mr-1 text-purple-600" />
                  <strong>Admin (2FA):</strong> admin@cineprod.com / admin123
                </div>
              </div>
              <p className="mt-2 text-xs text-blue-600 italic">
                💡 Use estas credenciais para acessar o sistema
              </p>
            </div>
          )}
        </div>
      </div>
    );
  };

  // Dashboard Component (simplificado)
  const Dashboard = () => {
    return (
      <div className="space-y-6">
        <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl p-6 text-white">
          <h1 className="text-3xl font-bold mb-2">
            {t('welcome')}, {appState.currentUser?.name}! 👋
          </h1>
          <p className="text-white/90 mb-4">
            {currentProject ? `${t('productionDay')} ${currentProject.completedDays} ${t('of')} ${currentProject.shootingDays}` : 'Carregando projeto...'}
          </p>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
            <div className="bg-white/20 backdrop-blur-sm rounded-lg p-4">
              <div className="text-sm text-white/80">{t('dailyBurnRate')}</div>
              <div className="text-2xl font-bold">$65K</div>
            </div>
            <div className="bg-white/20 backdrop-blur-sm rounded-lg p-4">
              <div className="text-sm text-white/80">{t('pagesPerDay')}</div>
              <div className="text-2xl font-bold">2.8</div>
            </div>
            <div className="bg-white/20 backdrop-blur-sm rounded-lg p-4">
              <div className="text-sm text-white/80">{t('crewAttendance')}</div>
              <div className="text-2xl font-bold">96.5%</div>
            </div>
            <div className="bg-white/20 backdrop-blur-sm rounded-lg p-4">
              <div className="text-sm text-white/80">{t('scriptCoverage')}</div>
              <div className="text-2xl font-bold">64.4%</div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <button
            onClick={() => setActiveModule('callsheets')}
            className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition-all border-2 border-transparent hover:border-blue-500 group"
          >
            <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
              <FileText className="w-6 h-6 text-blue-600" />
            </div>
            <h3 className="font-semibold mb-1">{t('newCallSheet')}</h3>
            <p className="text-sm text-gray-600">Criar nova folha de chamada</p>
          </button>

          <button
            onClick={() => setActiveModule('reports')}
            className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition-all border-2 border-transparent hover:border-purple-500 group"
          >
            <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
              <BarChart2 className="w-6 h-6 text-purple-600" />
            </div>
            <h3 className="font-semibold mb-1">{t('viewReports')}</h3>
            <p className="text-sm text-gray-600">Ver relatórios de produção</p>
          </button>

          <button
            onClick={() => setActiveModule('crew')}
            className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition-all border-2 border-transparent hover:border-green-500 group"
          >
            <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
              <Users className="w-6 h-6 text-green-600" />
            </div>
            <h3 className="font-semibold mb-1">{t('manageCrew')}</h3>
            <p className="text-sm text-gray-600">Gerenciar equipe</p>
          </button>

          <button
            onClick={() => setActiveModule('schedule')}
            className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition-all border-2 border-transparent hover:border-orange-500 group"
          >
            <div className="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
              <Calendar className="w-6 h-6 text-orange-600" />
            </div>
            <h3 className="font-semibold mb-1">{t('viewSchedule')}</h3>
            <p className="text-sm text-gray-600">Ver cronograma</p>
          </button>
        </div>

        {/* System Status */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold mb-4 flex items-center">
            <Activity className="w-5 h-5 mr-2 text-blue-600" />
            Status do Sistema
          </h2>
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
              <div className="flex items-center">
                <CheckCircle className="w-5 h-5 text-green-600 mr-3" />
                <span className="font-medium">Sistema Operacional</span>
              </div>
              <span className="text-sm text-green-600">Todos os serviços online</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
              <div className="flex items-center">
                <Cloud className="w-5 h-5 text-blue-600 mr-3" />
                <span className="font-medium">Sincronização</span>
              </div>
              <span className="text-sm text-blue-600">Ativa</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-purple-50 rounded-lg">
              <div className="flex items-center">
                <Shield className="w-5 h-5 text-purple-600 mr-3" />
                <span className="font-medium">Segurança</span>
              </div>
              <span className="text-sm text-purple-600">Protegido</span>
            </div>
          </div>
        </div>
      </div>
    );
  };

  // Render Module (simplificado)
  const renderModule = () => {
    switch (activeModule) {
      case 'dashboard':
        return <Dashboard />;
      case 'callsheets':
        return (
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-2xl font-bold mb-4 flex items-center">
              <FileText className="w-6 h-6 mr-2 text-blue-600" />
              Folhas de Chamada
            </h2>
            <p className="text-gray-600">Módulo de folhas de chamada em desenvolvimento...</p>
          </div>
        );
      case 'schedule':
        return (
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-2xl font-bold mb-4 flex items-center">
              <Calendar className="w-6 h-6 mr-2 text-blue-600" />
              Cronograma
            </h2>
            <p className="text-gray-600">Módulo de cronograma em desenvolvimento...</p>
          </div>
        );
      case 'crew':
        return (
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-2xl font-bold mb-4 flex items-center">
              <Users className="w-6 h-6 mr-2 text-blue-600" />
              Elenco e Equipe
            </h2>
            <p className="text-gray-600">Módulo de equipe em desenvolvimento...</p>
          </div>
        );
      case 'reports':
        return (
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-2xl font-bold mb-4 flex items-center">
              <BarChart2 className="w-6 h-6 mr-2 text-blue-600" />
              Relatórios
            </h2>
            <p className="text-gray-600">Módulo de relatórios em desenvolvimento...</p>
          </div>
        );
      case 'profile':
        return (
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-2xl font-bold mb-4 flex items-center">
              <User className="w-6 h-6 mr-2 text-blue-600" />
              Meu Perfil
            </h2>
            <div className="space-y-4">
              <div className="flex items-center gap-4">
                <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white text-2xl font-bold">
                  {appState.currentUser?.avatar}
                </div>
                <div>
                  <h3 className="text-xl font-bold">{appState.currentUser?.name}</h3>
                  <p className="text-gray-600">{appState.currentUser?.email}</p>
                  <p className="text-sm text-blue-600">{appState.currentUser?.role}</p>
                </div>
              </div>
            </div>
          </div>
        );
      case 'settings':
        return (
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-2xl font-bold mb-4 flex items-center">
              <Settings className="w-6 h-6 mr-2 text-blue-600" />
              Configurações
            </h2>
            <p className="text-gray-600">Módulo de configurações em desenvolvimento...</p>
          </div>
        );
      default:
        return <Dashboard />;
    }
  };

  const unreadNotifications = notifications.filter(n => n.unread).length;

  // Sistema Principal
  const MainSystem = () => {
    return (
      <div className="flex h-screen bg-gray-50">
        {/* Sidebar */}
        <div style={{
          width: sidebarOpen ? '240px' : '60px',
          backgroundColor: '#1D1E2C',
          minHeight: '100vh',
          transition: 'width 0.3s ease',
          overflow: 'hidden',
          display: 'flex',
          flexDirection: 'column'
        }}>
          <div style={{
            padding: sidebarOpen ? '20px' : '16px',
            borderBottom: '1px solid rgba(255,255,255,0.1)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: sidebarOpen ? 'flex-start' : 'center'
          }}>
            {sidebarOpen ? (
              <div className="flex items-center gap-3">
                <div style={{
                  width: '32px',
                  height: '32px',
                  backgroundColor: '#5d78ff',
                  borderRadius: '8px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center'
                }}>
                  <Film className="w-5 h-5 text-white" />
                </div>
                <div>
                  <h1 className="font-bold text-white">CineProd</h1>
                  <p className="text-xs" style={{ color: '#A2A3B7' }}>Systems</p>
                </div>
              </div>
            ) : (
              <div style={{
                width: '32px',
                height: '32px',
                backgroundColor: '#5d78ff',
                borderRadius: '8px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}>
                <Film className="w-5 h-5 text-white" />
              </div>
            )}
          </div>

          <nav style={{ flex: 1, padding: '16px 0', overflowY: 'auto' }}>
            {[
              { id: 'dashboard', icon: Home, label: t('modules.dashboard') },
              { id: 'callsheets', icon: Clapperboard, label: t('modules.callsheets') },
              { id: 'schedule', icon: Calendar, label: t('modules.schedule') },
              { id: 'crew', icon: Users, label: t('modules.crew') },
              { id: 'documents', icon: FolderOpen, label: t('modules.documents') },
              { id: 'tasks', icon: CheckCircle, label: t('modules.tasks') },
              { id: 'budget', icon: DollarSign, label: t('modules.budget') },
              { id: 'reports', icon: BarChart2, label: t('modules.reports') }
            ].map((item) => {
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
                    gap: '12px',
                    border: 'none',
                    backgroundColor: isActive ? 'rgba(93, 120, 255, 0.1)' : 'transparent',
                    color: isActive ? '#5d78ff' : '#A2A3B7',
                    borderLeft: isActive ? '3px solid #5d78ff' : '3px solid transparent',
                    cursor: 'pointer',
                    transition: 'all 0.2s ease',
                    fontSize: '14px'
                  }}
                  className="hover:bg-white hover:bg-opacity-5"
                >
                  <item.icon className="w-5 h-5 flex-shrink-0" />
                  {sidebarOpen && <span>{item.label}</span>}
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
              <div className="text-xs mb-2" style={{ color: '#A2A3B7' }}>Projeto Ativo</div>
              <div className="font-semibold text-sm mb-2 text-white">{currentProject.title}</div>
              <div className="flex justify-between text-xs mb-1" style={{ color: '#A2A3B7' }}>
                <span>Dia {currentProject.completedDays}/{currentProject.shootingDays}</span>
                <span>{Math.round((currentProject.completedDays / currentProject.shootingDays) * 100)}%</span>
              </div>
              <div style={{
                width: '100%',
                backgroundColor: 'rgba(255,255,255,0.2)',
                borderRadius: '4px',
                height: '4px'
              }}>
                <div style={{
                  width: `${(currentProject.completedDays / currentProject.shootingDays) * 100}%`,
                  backgroundColor: '#5d78ff',
                  height: '100%',
                  borderRadius: '4px',
                  transition: 'width 0.3s ease'
                }}></div>
              </div>
            </div>
          )}

          {/* Toggle Button */}
          <div style={{
            padding: '16px',
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
                color: '#A2A3B7',
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

        {/* Main Content */}
        <div className="flex-1 flex flex-col">
          {/* Header */}
          <header className="bg-white shadow-sm border-b border-gray-200">
            <div className="flex items-center justify-between px-6 py-4">
              <div className="flex items-center gap-4 flex-1">
                <button
                  onClick={() => setSidebarOpen(!sidebarOpen)}
                  className="p-2 hover:bg-gray-100 rounded-lg"
                >
                  <Menu className="w-5 h-5" />
                </button>
                
                <div className="relative flex-1 max-w-md">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                  <input
                    type="text"
                    placeholder={t('search')}
                    value={globalSearch}
                    onChange={(e) => setGlobalSearch(e.target.value)}
                    className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
              </div>

              <div className="flex items-center gap-3">
                {/* Language Switcher */}
                <div className="flex bg-gray-100 rounded-lg p-1">
                  <button
                    className={`px-2 py-1 rounded text-xs transition-all ${
                      appState.language === 'pt' ? 'bg-white shadow-sm' : ''
                    }`}
                    onClick={() => updateAppState({ language: 'pt' })}
                  >
                    PT
                  </button>
                  <button
                    className={`px-2 py-1 rounded text-xs transition-all ${
                      appState.language === 'en' ? 'bg-white shadow-sm' : ''
                    }`}
                    onClick={() => updateAppState({ language: 'en' })}
                  >
                    EN
                  </button>
                </div>

                {/* Notifications */}
                <div className="relative">
                  <button
                    onClick={() => setNotificationsOpen(!notificationsOpen)}
                    className="p-2 hover:bg-gray-100 rounded-lg relative"
                  >
                    <Bell className="w-5 h-5 text-gray-600" />
                    {unreadNotifications > 0 && (
                      <span className="absolute top-0 right-0 w-5 h-5 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
                        {unreadNotifications}
                      </span>
                    )}
                  </button>

                  {notificationsOpen && (
                    <div className="absolute right-0 mt-2 w-96 bg-white rounded-lg shadow-lg border border-gray-200 z-50">
                      <div className="p-4 border-b border-gray-200 flex justify-between items-center">
                        <h3 className="font-semibold">{t('notifications')}</h3>
                        <button
                          onClick={clearAllNotifications}
                          className="text-sm text-blue-600 hover:text-blue-700"
                        >
                          Limpar todas
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
                              className={`p-4 border-b border-gray-100 hover:bg-gray-50 cursor-pointer ${
                                notification.unread ? 'bg-blue-50' : ''
                              }`}
                            >
                              <div className="flex justify-between items-start">
                                <div className="flex-1">
                                  <p className="text-sm">{notification.message}</p>
                                  <p className="text-xs text-gray-500 mt-1">
                                    {new Date(notification.timestamp).toLocaleString('pt-BR')}
                                  </p>
                                </div>
                                {notification.unread && (
                                  <div className="w-2 h-2 bg-blue-500 rounded-full ml-2 mt-1.5" />
                                )}
                              </div>
                            </div>
                          ))
                        )}
                      </div>
                    </div>
                  )}
                </div>

                {/* User Menu */}
                <div className="relative">
                  <button
                    onClick={() => setUserMenuOpen(!userMenuOpen)}
                    className="flex items-center gap-2 p-2 hover:bg-gray-100 rounded-lg"
                  >
                    <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white text-sm font-bold">
                      {appState.currentUser?.avatar}
                    </div>
                    <ChevronDown className="w-4 h-4 text-gray-600" />
                  </button>

                  {userMenuOpen && (
                    <div className="absolute right-0 mt-2 w-56 bg-white rounded-lg shadow-lg border border-gray-200 z-50">
                      <div className="p-4 border-b border-gray-200">
                        <p className="font-medium">{appState.currentUser?.name}</p>
                        <p className="text-sm text-gray-600">{appState.currentUser?.email}</p>
                      </div>
                      <div className="p-2">
                        <button
                          onClick={() => {
                            setActiveModule('profile');
                            setUserMenuOpen(false);
                          }}
                          className="w-full flex items-center gap-3 px-3 py-2 hover:bg-gray-100 rounded-lg text-left"
                        >
                          <User className="w-4 h-4 text-gray-600" />
                          <span className="text-sm">{t('myProfile')}</span>
                        </button>
                        <button
                          onClick={() => {
                            setActiveModule('settings');
                            setUserMenuOpen(false);
                          }}
                          className="w-full flex items-center gap-3 px-3 py-2 hover:bg-gray-100 rounded-lg text-left"
                        >
                          <Settings className="w-4 h-4 text-gray-600" />
                          <span className="text-sm">{t('accountSettings')}</span>
                        </button>
                        <button className="w-full flex items-center gap-3 px-3 py-2 hover:bg-gray-100 rounded-lg text-left">
                          <HelpCircle className="w-4 h-4 text-gray-600" />
                          <span className="text-sm">{t('help')}</span>
                        </button>
                        <div className="border-t border-gray-200 mt-2 pt-2">
                          <button
                            onClick={handleLogout}
                            className="w-full flex items-center gap-3 px-3 py-2 hover:bg-gray-100 rounded-lg text-left text-red-600"
                          >
                            <LogOut className="w-4 h-4" />
                            <span className="text-sm">{t('logout')}</span>
                          </button>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </header>

          {/* Main Content Area */}
          <main className="flex-1 overflow-y-auto">
            <div className="p-6">
              {renderModule()}
            </div>
          </main>
        </div>
      </div>
    );
  };

  // Render condicional baseado no estado de autenticação
  if (loading) return <LoadingScreen />;
  if (!appState.isAuthenticated) return <LoginScreen />;
  return <MainSystem />;
};

// Componente principal com providers
export default function App() {
  return (
    <ModalProvider>
      <ProductionManagementSystem />
    </ModalProvider>
  );
}
