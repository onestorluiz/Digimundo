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

// CSS Customizado
const customStyles = `
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
  
  .animate-fade-in {
    animation: fade-in 0.3s ease-out;
  }
  
  .animate-scale-in {
    animation: scale-in 0.3s ease-out;
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
  const [appState, setAppState] = useState({
    language: 'pt',
    theme: 'light',
    currentUser: null,
    isAuthenticated: false,
    authToken: null,
    rememberMe: false,
    savedEmail: ''
  });
  
  const [activeModule, setActiveModule] = useState('dashboard');
  const [loading, setLoading] = useState(true);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [notifications, setNotifications] = useState([]);
  const [currentProject, setCurrentProject] = useState(null);
  const [globalSearch, setGlobalSearch] = useState('');

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
      
      // Call Sheets
      callSheet: 'Folha de Chamada',
      distribute: 'Distribuir',
      print: 'Imprimir',
      shootingDate: 'Data de Filmagem',
      generalCrewCall: 'Chamada Geral',
      weatherForecast: 'Previsão do Tempo',
      locationInfo: 'Informações de Locação',
      scenesSchedule: 'Cronograma de Cenas',
      scene: 'Cena',
      scenes: 'Cenas',
      pages: 'Páginas',
      description: 'Descrição',
      cast: 'Elenco',
      location: 'Locação',
      crewCallTimes: 'Horários de Chamada',
      createNewCallSheet: 'Criar Nova Folha de Chamada',
      
      // Crew
      department: 'Departamento',
      role: 'Função',
      contact: 'Contato',
      dayRate: 'Diária',
      union: 'Sindicato',
      daysWorked: 'Dias Trabalhados',
      phone: 'Telefone',
      
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
      urgent: 'Urgente',
      high: 'Alta',
      medium: 'Média',
      low: 'Baixa',
      pending: 'Pendente',
      inProgress: 'Em Progresso',
      completed: 'Concluído',
      all: 'Todos',
      none: 'Nenhum',
      actions: 'Ações',
      more: 'Mais',
      close: 'Fechar',
      confirm: 'Confirmar',
      back: 'Voltar',
      next: 'Próximo',
      settings: 'Configurações',
      preferences: 'Preferências',
      notifications: 'Notificações',
      security: 'Segurança',
      about: 'Sobre'
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
      
      // Call Sheets
      callSheet: 'Call Sheet',
      distribute: 'Distribute',
      print: 'Print',
      shootingDate: 'Shooting Date',
      generalCrewCall: 'General Crew Call',
      weatherForecast: 'Weather Forecast',
      locationInfo: 'Location Information',
      scenesSchedule: 'Scenes Schedule',
      scene: 'Scene',
      scenes: 'Scenes',
      pages: 'Pages',
      description: 'Description',
      cast: 'Cast',
      location: 'Location',
      crewCallTimes: 'Crew Call Times',
      createNewCallSheet: 'Create New Call Sheet',
      
      // Crew
      department: 'Department',
      role: 'Role',
      contact: 'Contact',
      dayRate: 'Day Rate',
      union: 'Union',
      daysWorked: 'Days Worked',
      phone: 'Phone',
      
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
      urgent: 'Urgent',
      high: 'High',
      medium: 'Medium',
      low: 'Low',
      pending: 'Pending',
      inProgress: 'In Progress',
      completed: 'Completed',
      all: 'All',
      none: 'None',
      actions: 'Actions',
      more: 'More',
      close: 'Close',
      confirm: 'Confirm',
      back: 'Back',
      next: 'Next',
      settings: 'Settings',
      preferences: 'Preferences',
      notifications: 'Notifications',
      security: 'Security',
      about: 'About'
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

  // Sistema de Permissões
  const permissions = {
    'Director': {
      modules: ['dashboard', 'callsheets', 'schedule', 'stripboard', 'breakdown', 'crew', 'documents', 'tasks', 'budget', 'reports', 'communication', 'postproduction', 'dood', 'analytics', 'inventory'],
      actions: {
        view: true,
        edit: true,
        create: true,
        delete: false,
        approve: true
      }
    },
    'Producer': {
      modules: ['dashboard', 'callsheets', 'schedule', 'stripboard', 'breakdown', 'crew', 'documents', 'tasks', 'budget', 'reports', 'communication', 'postproduction', 'dood', 'admin', 'analytics', 'inventory'],
      actions: {
        view: true,
        edit: true,
        create: true,
        delete: true,
        approve: true
      }
    },
    'DP': {
      modules: ['dashboard', 'callsheets', 'schedule', 'stripboard', 'breakdown', 'documents', 'tasks', 'communication', 'inventory'],
      actions: {
        view: true,
        edit: true,
        create: false,
        delete: false,
        approve: false
      }
    },
    'Talent': {
      modules: ['dashboard', 'callsheets', 'schedule', 'documents', 'tasks', 'communication'],
      actions: {
        view: true,
        edit: false,
        create: false,
        delete: false,
        approve: false
      }
    }
  };

  // Database simulado
  const usersDatabase = [
    {
      id: 1,
      name: 'Sofia Luz',
      email: 'sofia@cineprod.com',
      password: 'director123',
      role: 'Director',
      department: 'Creative',
      avatar: 'SL',
      phone: '+55 11 99999-0001',
      twoFactorEnabled: false,
      status: 'active',
      projects: 3
    },
    {
      id: 2,
      name: 'Marcus Terra',
      email: 'marcus@cineprod.com',
      password: 'producer123',
      role: 'Producer',
      department: 'Production',
      avatar: 'MT',
      phone: '+55 11 99999-0002',
      twoFactorEnabled: false,
      status: 'active',
      projects: 5
    },
    {
      id: 3,
      name: 'Luna Sombra',
      email: 'luna@cineprod.com',
      password: 'dp123',
      role: 'DP',
      department: 'Camera',
      avatar: 'LS',
      phone: '+55 11 99999-0003',
      twoFactorEnabled: false,
      status: 'active',
      projects: 2
    },
    {
      id: 4,
      name: 'Rio Vento',
      email: 'rio@cineprod.com',
      password: 'talent123',
      role: 'Talent',
      department: 'Cast',
      avatar: 'RV',
      phone: '+55 11 99999-0004',
      twoFactorEnabled: false,
      status: 'active',
      projects: 1
    }
  ];

  // Estado de Produção
  const [productionData, setProductionData] = useState({
    projects: [
      {
        id: 1,
        name: 'Summer Campaign 2024',
        client: 'Global Brand Inc.',
        status: 'In Production',
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
      },
      {
        id: 2,
        date: '2024-01-21',
        day: 6,
        callTime: '07:00',
        wrap: '19:00',
        location: 'Downtown Office',
        scenes: ['4', '5A', '5B'],
        status: 'draft',
        weather: { temp: 26, condition: 'cloudy', sunrise: '05:46', sunset: '19:29' }
      }
    ],
    tasks: [
      { id: 1, title: 'Review script changes Scene 5', assignee: 'Sofia Luz', due: '2024-01-22', priority: 'high', status: 'pending', department: 'Direction' },
      { id: 2, title: 'Confirm location permits Downtown', assignee: 'Marcus Terra', due: '2024-01-23', priority: 'urgent', status: 'inProgress', department: 'Production' },
      { id: 3, title: 'Camera test new lenses', assignee: 'Luna Sombra', due: '2024-01-21', priority: 'medium', status: 'completed', department: 'Camera' },
      { id: 4, title: 'Review talent contracts', assignee: 'Marcus Terra', due: '2024-01-24', priority: 'high', status: 'pending', department: 'Production' },
      { id: 5, title: 'Prepare wardrobe for Scene 6', assignee: 'Ana Costa', due: '2024-01-22', priority: 'medium', status: 'inProgress', department: 'Wardrobe' }
    ],
    crew: [
      { id: 1, name: 'Sofia Luz', role: 'Director', department: 'Direction', phone: '+55 11 99999-0001', email: 'sofia@prod.com', dayRate: 5000, union: 'DGA', daysWorked: 29 },
      { id: 2, name: 'Marcus Terra', role: 'Producer', department: 'Production', phone: '+55 11 99999-0002', email: 'marcus@prod.com', dayRate: 4500, union: 'PGA', daysWorked: 45 },
      { id: 3, name: 'Luna Sombra', role: 'DP', department: 'Camera', phone: '+55 11 99999-0003', email: 'luna@prod.com', dayRate: 4000, union: 'IATSE', daysWorked: 28 },
      { id: 4, name: 'Rio Vento', role: 'Lead Actor', department: 'Cast', phone: '+55 11 99999-0004', email: 'rio@prod.com', dayRate: 8000, union: 'SAG-AFTRA', daysWorked: 15 },
      { id: 5, name: 'Marina Costa', role: '1st AD', department: 'Direction', phone: '+55 11 99999-0005', email: 'marina@prod.com', dayRate: 3000, union: 'DGA', daysWorked: 29 },
      { id: 6, name: 'Pedro Silva', role: 'Gaffer', department: 'Electric', phone: '+55 11 99999-0006', email: 'pedro@prod.com', dayRate: 2500, union: 'IATSE', daysWorked: 25 }
    ],
    documents: [
      { id: 1, name: 'Script_v3_Final.pdf', type: 'script', size: '2.4MB', lastModified: '2024-01-18', uploadedBy: 'Sofia Luz', department: 'Direction' },
      { id: 2, name: 'Budget_Breakdown.xlsx', type: 'budget', size: '854KB', lastModified: '2024-01-15', uploadedBy: 'Marcus Terra', department: 'Production' },
      { id: 3, name: 'Location_Photos.zip', type: 'images', size: '45.2MB', lastModified: '2024-01-12', uploadedBy: 'Location Scout', department: 'Production' }
    ],
    schedule: [
      { id: 1, date: '2024-01-22', scenes: ['6', '7'], location: 'Beach Location', status: 'confirmed', callTime: '05:30' },
      { id: 2, date: '2024-01-23', scenes: ['8', '9', '10'], location: 'City Street', status: 'tentative', callTime: '14:00' },
      { id: 3, date: '2024-01-24', scenes: ['11', '12'], location: 'Studio B', status: 'confirmed', callTime: '08:00' }
    ]
  });

  // Effects
  useEffect(() => {
    const timer = setTimeout(() => {
      setLoading(false);
      if (appState.isAuthenticated && !currentProject) {
        setCurrentProject(productionData.projects[0]);
      }
    }, 1500);
    
    return () => clearTimeout(timer);
  }, [appState.isAuthenticated, currentProject, productionData.projects]);

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
  const hasPermission = useCallback((action) => {
    if (!appState.currentUser) return false;
    const userPermissions = permissions[appState.currentUser.role];
    return userPermissions?.actions?.[action] || false;
  }, [appState.currentUser]);

  const canAccessModule = useCallback((module) => {
    if (!appState.currentUser) return false;
    const userPermissions = permissions[appState.currentUser.role];
    return userPermissions?.modules?.includes(module) || false;
  }, [appState.currentUser]);

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
    const [loginMode, setLoginMode] = useState('login'); // login, forgotPassword, createAccount, twoFactor
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [fullName, setFullName] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const [twoFactorCode, setTwoFactorCode] = useState(['', '', '', '', '', '']);
    const [errors, setErrors] = useState({});
    const [isLoading, setIsLoading] = useState(false);
    const [showDemoInfo, setShowDemoInfo] = useState(true);
    const [agreeTerms, setAgreeTerms] = useState(false);

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
        } else {
          completeLogin(user);
        }
      } catch (error) {
        setErrors({ general: error.message });
      } finally {
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
        
        // Simular criação de conta
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
        savedEmail: appState.rememberMe ? email : ''
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
              onClick={() => setTwoFactorCode(['', '', '', '', '', ''])}
              className="w-full mt-4 text-blue-600 hover:text-blue-700 text-sm"
            >
              {t('resendCode')}
            </button>
            
            <button 
              onClick={() => {
                const user = usersDatabase.find(u => u.email === email);
                completeLogin(user);
              }}
              className="w-full mt-2 text-gray-600 hover:text-gray-700 text-sm"
            >
              Pular verificação (demo)
            </button>
          </div>
        </div>
      );
    }

    // Login Screen
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-purple-50">
        <div className="bg-white p-8 rounded-2xl shadow-xl w-full max-w-md">
          <div className="flex justify-end mb-4">
            <div className="flex bg-gray-100 rounded-lg p-1">
              <button
                className={`px-3 py-1 rounded text-sm transition-all ${
                  appState.language === 'pt' ? 'bg-white shadow-sm' : ''
                }`}
                onClick={() => updateAppState({ language: 'pt' })}
              >
                PT
              </button>
              <button
                className={`px-3 py-1 rounded text-sm transition-all ${
                  appState.language === 'en' ? 'bg-white shadow-sm' : ''
                }`}
                onClick={() => updateAppState({ language: 'en' })}
              >
                EN
              </button>
            </div>
          </div>

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
            <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm flex items-center">
              <AlertCircle className="w-4 h-4 mr-2 flex-shrink-0" />
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
                  checked={appState.rememberMe}
                  onChange={(e) => updateAppState({ rememberMe: e.target.checked })}
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
            <div className="mt-6 p-4 bg-blue-50 rounded-lg relative">
              <button
                onClick={() => setShowDemoInfo(false)}
                className="absolute top-2 right-2 text-blue-400 hover:text-blue-600"
              >
                <X className="w-4 h-4" />
              </button>
              <p className="text-xs text-blue-800 font-medium mb-2">
                🎬 Usuários de demonstração (sem 2FA):
              </p>
              <div className="space-y-1 text-xs text-blue-700">
                <div>✅ Director: sofia@cineprod.com / director123</div>
                <div>✅ Producer: marcus@cineprod.com / producer123</div>
                <div>✅ DP: luna@cineprod.com / dp123</div>
                <div>✅ Talent: rio@cineprod.com / talent123</div>
              </div>
            </div>
          )}
        </div>
      </div>
    );
  };

  // Dashboard Component
  const Dashboard = () => {
    const [showWelcomeMessage, setShowWelcomeMessage] = useState(true);

    const productionKPIs = {
      efficiency: {
        pagesPerDay: 2.8,
        setupsPerDay: 18,
        overtimePercent: 12
      },
      financial: {
        burnRate: 65000,
        budgetVariance: 3.2,
        contingencyUsed: 8
      },
      crew: {
        attendanceRate: 96.5,
        safetyIncidents: 0,
        equipmentUtilization: 82
      },
      creative: {
        scriptCoverage: 64.4,
        vfxProgress: 35,
        adrRequired: 28
      }
    };

    const handleQuickAction = (action) => {
      switch(action) {
        case 'newCallSheet':
          setActiveModule('callsheets');
          break;
        case 'viewReports':
          setActiveModule('reports');
          break;
        case 'manageCrew':
          setActiveModule('crew');
          break;
        case 'viewSchedule':
          setActiveModule('schedule');
          break;
        default:
          addNotification({
            message: `Ação "${action}" será implementada em breve`,
            type: 'info',
            priority: 'normal'
          });
      }
    };

    return (
      <div className="space-y-6">
        {showWelcomeMessage && (
          <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl p-6 text-white relative overflow-hidden">
            <button
              onClick={() => setShowWelcomeMessage(false)}
              className="absolute top-4 right-4 text-white/80 hover:text-white"
            >
              <X className="w-5 h-5" />
            </button>
            
            <div className="relative z-10">
              <h1 className="text-3xl font-bold mb-2">
                {t('welcome')}, {appState.currentUser?.name}! 👋
              </h1>
              <p className="text-white/90 mb-4">
                {currentProject ? `${t('productionDay')} ${currentProject.completedDays} ${t('of')} ${currentProject.shootingDays}` : 'Carregando projeto...'}
              </p>
              
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
                <div className="bg-white/20 backdrop-blur-sm rounded-lg p-4">
                  <div className="text-sm text-white/80">{t('dailyBurnRate')}</div>
                  <div className="text-2xl font-bold">
                    ${(productionKPIs.financial.burnRate / 1000).toFixed(0)}K
                  </div>
                </div>
                <div className="bg-white/20 backdrop-blur-sm rounded-lg p-4">
                  <div className="text-sm text-white/80">{t('pagesPerDay')}</div>
                  <div className="text-2xl font-bold">{productionKPIs.efficiency.pagesPerDay}</div>
                </div>
                <div className="bg-white/20 backdrop-blur-sm rounded-lg p-4">
                  <div className="text-sm text-white/80">{t('crewAttendance')}</div>
                  <div className="text-2xl font-bold">{productionKPIs.crew.attendanceRate}%</div>
                </div>
                <div className="bg-white/20 backdrop-blur-sm rounded-lg p-4">
                  <div className="text-sm text-white/80">{t('scriptCoverage')}</div>
                  <div className="text-2xl font-bold">{productionKPIs.creative.scriptCoverage}%</div>
                </div>
              </div>
            </div>
            
            <div className="absolute -right-20 -top-20 w-64 h-64 bg-white/10 rounded-full blur-3xl"></div>
            <div className="absolute -left-20 -bottom-20 w-64 h-64 bg-purple-400/20 rounded-full blur-3xl"></div>
          </div>
        )}

        {/* Quick Actions */}
        <div>
          <h2 className="text-lg font-semibold mb-4">{t('quickActions')}</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { id: 'newCallSheet', label: t('newCallSheet'), icon: Clapperboard, bgClass: 'bg-blue-100', iconClass: 'text-blue-600' },
              { id: 'viewReports', label: t('viewReports'), icon: FileBarChart, bgClass: 'bg-green-100', iconClass: 'text-green-600' },
              { id: 'manageCrew', label: t('manageCrew'), icon: Users, bgClass: 'bg-purple-100', iconClass: 'text-purple-600' },
              { id: 'viewSchedule', label: t('viewSchedule'), icon: Calendar, bgClass: 'bg-orange-100', iconClass: 'text-orange-600' }
            ].map((action) => {
              const Icon = action.icon;
              return (
                <button
                  key={action.id}
                  onClick={() => handleQuickAction(action.id)}
                  className="bg-white p-6 rounded-xl shadow-sm hover:shadow-md transition-all border border-gray-100 group"
                >
                  <div className="flex flex-col items-center text-center">
                    <div className={`w-12 h-12 ${action.bgClass} rounded-full flex items-center justify-center mb-3 group-hover:scale-110 transition-transform`}>
                      <Icon className={`w-6 h-6 ${action.iconClass}`} />
                    </div>
                    <h3 className="font-medium text-gray-900">{action.label}</h3>
                  </div>
                </button>
              );
            })}
          </div>
        </div>

        {/* KPIs */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="bg-white rounded-xl p-6 shadow-sm hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                <Activity className="w-6 h-6 text-blue-600" />
              </div>
              <span className="text-sm text-green-600 font-medium flex items-center">
                <TrendingUp className="w-4 h-4 mr-1" />
                +5.2%
              </span>
            </div>
            <h3 className="text-lg font-semibold mb-1">{t('productionEfficiency')}</h3>
            <div className="space-y-2 mt-4">
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">{t('setupsDay')}</span>
                <span className="font-medium">{productionKPIs.efficiency.setupsPerDay}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">{t('overtime')}</span>
                <span className="font-medium text-yellow-600">{productionKPIs.efficiency.overtimePercent}%</span>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-sm hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                <DollarSign className="w-6 h-6 text-green-600" />
              </div>
              <span className="text-sm text-red-600 font-medium flex items-center">
                <TrendingDown className="w-4 h-4 mr-1" />
                -3.2%
              </span>
            </div>
            <h3 className="text-lg font-semibold mb-1">{t('financialHealth')}</h3>
            <div className="space-y-2 mt-4">
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">{t('variance')}</span>
                <span className="font-medium">{productionKPIs.financial.budgetVariance}%</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">{t('contingency')}</span>
                <span className="font-medium">{productionKPIs.financial.contingencyUsed}%</span>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-sm hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                <Users className="w-6 h-6 text-purple-600" />
              </div>
              <span className="text-sm text-green-600 font-medium">96.5%</span>
            </div>
            <h3 className="text-lg font-semibold mb-1">{t('crewMetrics')}</h3>
            <div className="space-y-2 mt-4">
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">{t('safetyIncidents')}</span>
                <span className="font-medium text-green-600">0</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">{t('equipmentUse')}</span>
                <span className="font-medium">{productionKPIs.crew.equipmentUtilization}%</span>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-sm hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center">
                <Film className="w-6 h-6 text-orange-600" />
              </div>
              <span className="text-sm font-medium">{productionKPIs.creative.scriptCoverage}%</span>
            </div>
            <h3 className="text-lg font-semibold mb-1">{t('creativeProgress')}</h3>
            <div className="space-y-2 mt-4">
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">{t('vfxProgress')}</span>
                <span className="font-medium">{productionKPIs.creative.vfxProgress}%</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">{t('adrNeeded')}</span>
                <span className="font-medium">{productionKPIs.creative.adrRequired}%</span>
              </div>
            </div>
          </div>
        </div>

        {/* Recent Activity & Alerts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white rounded-xl shadow-sm">
            <div className="p-6 border-b border-gray-100">
              <h2 className="text-lg font-semibold">{t('recentActivity')}</h2>
            </div>
            <div className="p-6 space-y-4">
              {notifications.slice(0, 3).map((activity) => (
                <div key={activity.id} className="flex items-start gap-3">
                  <div className={`w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 ${
                    activity.type === 'success' ? 'bg-green-100' :
                    activity.type === 'warning' ? 'bg-yellow-100' :
                    activity.type === 'error' ? 'bg-red-100' :
                    'bg-blue-100'
                  }`}>
                    {activity.module === 'callsheets' ? <Clapperboard className="w-5 h-5 text-blue-600" /> :
                     activity.module === 'budget' ? <DollarSign className="w-5 h-5 text-green-600" /> :
                     activity.module === 'tasks' ? <CheckCircle className="w-5 h-5 text-purple-600" /> :
                     <Activity className="w-5 h-5 text-gray-600" />}
                  </div>
                  <div className="flex-1">
                    <p className="text-sm text-gray-900">{activity.message}</p>
                    <p className="text-xs text-gray-500 mt-1">
                      {new Date(activity.timestamp).toLocaleTimeString('pt-BR')}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-sm">
            <div className="p-6 border-b border-gray-100">
              <h2 className="text-lg font-semibold flex items-center gap-2">
                <Bell className="w-5 h-5 text-gray-600" />
                {t('systemAlerts')}
              </h2>
            </div>
            <div className="p-6 space-y-4">
              <div className="flex items-start gap-3 p-4 bg-yellow-50 rounded-lg border border-yellow-200">
                <AlertTriangle className="w-5 h-5 text-yellow-600 flex-shrink-0 mt-0.5" />
                <div className="flex-1">
                  <p className="font-medium text-yellow-900">{t('weatherAlert')}</p>
                  <p className="text-sm text-yellow-700 mt-1">{t('rainChance')}</p>
                </div>
              </div>
              
              <div className="flex items-start gap-3 p-4 bg-blue-50 rounded-lg border border-blue-200">
                <Clock className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
                <div className="flex-1">
                  <p className="font-medium text-blue-900">{t('turnaroundRisk')}</p>
                  <p className="text-sm text-blue-700 mt-1">{t('crewRestWarning')}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Próximos Prazos */}
        <div className="bg-white rounded-xl shadow-sm">
          <div className="p-6 border-b border-gray-100">
            <h2 className="text-lg font-semibold flex items-center gap-2">
              <Clock className="w-5 h-5 text-gray-600" />
              {t('upcomingDeadlines')}
            </h2>
          </div>
          <div className="p-6">
            <div className="space-y-3">
              {productionData.tasks
                .filter(task => task.status !== 'completed')
                .sort((a, b) => new Date(a.due) - new Date(b.due))
                .slice(0, 5)
                .map(task => (
                  <div key={task.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div className="flex items-center gap-3">
                      <div className={`w-2 h-2 rounded-full ${
                        task.priority === 'urgent' ? 'bg-red-500' :
                        task.priority === 'high' ? 'bg-yellow-500' :
                        task.priority === 'medium' ? 'bg-blue-500' :
                        'bg-gray-400'
                      }`} />
                      <div>
                        <p className="font-medium text-sm">{task.title}</p>
                        <p className="text-xs text-gray-600">{task.assignee} • {task.department}</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-sm font-medium text-gray-900">
                        {new Date(task.due).toLocaleDateString('pt-BR')}
                      </p>
                      <p className={`text-xs ${
                        task.priority === 'urgent' ? 'text-red-600' :
                        task.priority === 'high' ? 'text-yellow-600' :
                        'text-gray-600'
                      }`}>
                        {t(task.priority)}
                      </p>
                    </div>
                  </div>
                ))}
            </div>
          </div>
        </div>
      </div>
    );
  };

  // Call Sheets Module
  const CallSheetsModule = () => {
    const [selectedCallSheet, setSelectedCallSheet] = useState(null);
    const { openModal, closeModal } = useModal();

    const handleCreateCallSheet = () => {
      openModal((modalId) => {
        const [callSheetData, setCallSheetData] = useState({
          date: '',
          callTime: '06:00',
          wrap: '18:00',
          location: '',
          scenes: ''
        });

        return (
          <div className="p-6">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-semibold">{t('createNewCallSheet')}</h2>
              <button
                onClick={() => closeModal(modalId)}
                className="p-2 hover:bg-gray-100 rounded-lg"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  {t('shootingDate')}
                </label>
                <input
                  type="date"
                  value={callSheetData.date}
                  onChange={(e) => setCallSheetData({...callSheetData, date: e.target.value})}
                  className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    {t('generalCrewCall')}
                  </label>
                  <input
                    type="time"
                    value={callSheetData.callTime}
                    onChange={(e) => setCallSheetData({...callSheetData, callTime: e.target.value})}
                    className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Wrap Time
                  </label>
                  <input
                    type="time"
                    value={callSheetData.wrap}
                    onChange={(e) => setCallSheetData({...callSheetData, wrap: e.target.value})}
                    className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  {t('location')}
                </label>
                <input
                  type="text"
                  value={callSheetData.location}
                  onChange={(e) => setCallSheetData({...callSheetData, location: e.target.value})}
                  placeholder="Ex: Studio A - São Paulo"
                  className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  {t('scenes')}
                </label>
                <input
                  type="text"
                  value={callSheetData.scenes}
                  onChange={(e) => setCallSheetData({...callSheetData, scenes: e.target.value})}
                  placeholder="Ex: 1A, 2B, 3"
                  className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div className="flex justify-end gap-3 mt-6">
                <button
                  onClick={() => closeModal(modalId)}
                  className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg"
                >
                  {t('cancel')}
                </button>
                <button
                  onClick={() => {
                    if (callSheetData.date && callSheetData.location && callSheetData.scenes) {
                      const newCallSheet = {
                        id: Date.now(),
                        ...callSheetData,
                        day: productionData.callSheets.length + 1,
                        scenes: callSheetData.scenes.split(',').map(s => s.trim()),
                        status: 'draft',
                        weather: { temp: 25, condition: 'sunny', sunrise: '05:45', sunset: '19:30' }
                      };
                      setProductionData(prev => ({
                        ...prev,
                        callSheets: [...prev.callSheets, newCallSheet]
                      }));
                      closeModal(modalId);
                      addNotification({
                        message: 'Folha de chamada criada com sucesso!',
                        type: 'success',
                        priority: 'normal'
                      });
                    } else {
                      addNotification({
                        message: 'Preencha todos os campos obrigatórios',
                        type: 'error',
                        priority: 'high'
                      });
                    }
                  }}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  {t('save')}
                </button>
              </div>
            </div>
          </div>
        );
      });
    };

    const handleDistribute = (callSheet) => {
      openModal((modalId) => (
        <div className="p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-semibold">{t('distribute')} - Day {callSheet.day}</h2>
            <button
              onClick={() => closeModal(modalId)}
              className="p-2 hover:bg-gray-100 rounded-lg"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
          
          <div className="space-y-4">
            <div className="bg-blue-50 p-4 rounded-lg">
              <p className="text-sm text-blue-800">
                Esta folha de chamada será enviada para todos os {productionData.crew.length} membros da equipe.
              </p>
            </div>
            
            <div>
              <label className="flex items-center">
                <input type="checkbox" className="mr-2" defaultChecked />
                <span className="text-sm">Enviar por email</span>
              </label>
            </div>
            
            <div>
              <label className="flex items-center">
                <input type="checkbox" className="mr-2" defaultChecked />
                <span className="text-sm">Enviar por SMS</span>
              </label>
            </div>
            
            <div>
              <label className="flex items-center">
                <input type="checkbox" className="mr-2" />
                <span className="text-sm">Enviar notificação no app</span>
              </label>
            </div>
            
            <div className="flex justify-end gap-3 mt-6">
              <button
                onClick={() => closeModal(modalId)}
                className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg"
              >
                {t('cancel')}
              </button>
              <button
                onClick={() => {
                  closeModal(modalId);
                  const updatedCallSheets = productionData.callSheets.map(cs => 
                    cs.id === callSheet.id ? { ...cs, status: 'distributed' } : cs
                  );
                  setProductionData(prev => ({ ...prev, callSheets: updatedCallSheets }));
                  addNotification({
                    message: 'Folha de chamada distribuída com sucesso!',
                    type: 'success',
                    priority: 'high'
                  });
                }}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center gap-2"
              >
                <Send className="w-4 h-4" />
                {t('distribute')}
              </button>
            </div>
          </div>
        </div>
      ));
    };

    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-bold">{t('modules.callsheets')}</h1>
          <button
            onClick={handleCreateCallSheet}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center gap-2"
          >
            <Plus className="w-4 h-4" />
            {t('new')} {t('callSheet')}
          </button>
        </div>

        <div className="grid gap-4">
          {productionData.callSheets.map(callSheet => (
            <div key={callSheet.id} className="bg-white rounded-lg shadow-sm p-6">
              <div className="flex items-start justify-between">
                <div>
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="text-lg font-semibold">Day {callSheet.day}</h3>
                    <span className={`px-2 py-1 text-xs rounded-full ${
                      callSheet.status === 'distributed' 
                        ? 'bg-green-100 text-green-800' 
                        : 'bg-yellow-100 text-yellow-800'
                    }`}>
                      {callSheet.status === 'distributed' ? 'Distribuída' : 'Rascunho'}
                    </span>
                  </div>
                  <div className="space-y-1 text-sm text-gray-600">
                    <p>{new Date(callSheet.date).toLocaleDateString('pt-BR')} • {callSheet.callTime} - {callSheet.wrap}</p>
                    <p className="flex items-center gap-1">
                      <MapPin className="w-4 h-4" />
                      {callSheet.location}
                    </p>
                    <p>Cenas: {callSheet.scenes.join(', ')}</p>
                  </div>
                </div>
                
                <div className="flex gap-2">
                  <button
                    onClick={() => window.print()}
                    className="p-2 hover:bg-gray-100 rounded-lg"
                    title={t('print')}
                  >
                    <Printer className="w-4 h-4 text-gray-600" />
                  </button>
                  <button
                    onClick={() => handleDistribute(callSheet)}
                    className="p-2 hover:bg-gray-100 rounded-lg"
                    title={t('distribute')}
                  >
                    <Send className="w-4 h-4 text-gray-600" />
                  </button>
                  <button
                    onClick={() => setSelectedCallSheet(callSheet)}
                    className="p-2 hover:bg-gray-100 rounded-lg"
                    title={t('edit')}
                  >
                    <Edit className="w-4 h-4 text-gray-600" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  // Tasks Module
  const TasksModule = () => {
    const [filter, setFilter] = useState('all');
    const { openModal, closeModal } = useModal();

    const filteredTasks = productionData.tasks.filter(task => {
      if (filter === 'all') return true;
      return task.status === filter;
    });

    const handleCreateTask = () => {
      openModal((modalId) => {
        const [taskData, setTaskData] = useState({
          title: '',
          assignee: productionData.crew[0]?.name || '',
          due: '',
          priority: 'medium',
          department: 'Production'
        });

        return (
          <div className="p-6">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-semibold">Nova Tarefa</h2>
              <button
                onClick={() => closeModal(modalId)}
                className="p-2 hover:bg-gray-100 rounded-lg"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Título
                </label>
                <input
                  type="text"
                  value={taskData.title}
                  onChange={(e) => setTaskData({...taskData, title: e.target.value})}
                  className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                  placeholder="Descreva a tarefa..."
                />
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Responsável
                  </label>
                  <select 
                    value={taskData.assignee}
                    onChange={(e) => setTaskData({...taskData, assignee: e.target.value})}
                    className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                  >
                    {productionData.crew.map(member => (
                      <option key={member.id} value={member.name}>
                        {member.name}
                      </option>
                    ))}
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Prazo
                  </label>
                  <input
                    type="date"
                    value={taskData.due}
                    onChange={(e) => setTaskData({...taskData, due: e.target.value})}
                    className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Prioridade
                </label>
                <select 
                  value={taskData.priority}
                  onChange={(e) => setTaskData({...taskData, priority: e.target.value})}
                  className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                >
                  <option value="low">Baixa</option>
                  <option value="medium">Média</option>
                  <option value="high">Alta</option>
                  <option value="urgent">Urgente</option>
                </select>
              </div>
              
              <div className="flex justify-end gap-3 mt-6">
                <button
                  onClick={() => closeModal(modalId)}
                  className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg"
                >
                  {t('cancel')}
                </button>
                <button
                  onClick={() => {
                    if (taskData.title && taskData.due) {
                      const newTask = {
                        id: Date.now(),
                        ...taskData,
                        status: 'pending'
                      };
                      setProductionData(prev => ({
                        ...prev,
                        tasks: [...prev.tasks, newTask]
                      }));
                      closeModal(modalId);
                      addNotification({
                        message: 'Tarefa criada com sucesso!',
                        type: 'success',
                        priority: 'normal'
                      });
                    } else {
                      addNotification({
                        message: 'Preencha todos os campos obrigatórios',
                        type: 'error',
                        priority: 'high'
                      });
                    }
                  }}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  {t('save')}
                </button>
              </div>
            </div>
          </div>
        );
      });
    };

    const handleTaskUpdate = (taskId, newStatus) => {
      const updatedTasks = productionData.tasks.map(task => 
        task.id === taskId ? { ...task, status: newStatus } : task
      );
      setProductionData(prev => ({ ...prev, tasks: updatedTasks }));
      
      addNotification({
        message: `Tarefa atualizada para: ${t(newStatus)}`,
        type: 'success',
        priority: 'normal'
      });
    };

    const handleTaskDelete = (taskId) => {
      const updatedTasks = productionData.tasks.filter(task => task.id !== taskId);
      setProductionData(prev => ({ ...prev, tasks: updatedTasks }));
      
      addNotification({
        message: 'Tarefa removida com sucesso!',
        type: 'success',
        priority: 'normal'
      });
    };

    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-bold">{t('modules.tasks')}</h1>
          <button
            onClick={handleCreateTask}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center gap-2"
          >
            <Plus className="w-4 h-4" />
            Nova Tarefa
          </button>
        </div>

        <div className="flex gap-2">
          {['all', 'pending', 'inProgress', 'completed'].map(status => (
            <button
              key={status}
              onClick={() => setFilter(status)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                filter === status 
                  ? 'bg-blue-500 text-white' 
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {t(status === 'all' ? 'all' : status)} ({productionData.tasks.filter(t => status === 'all' ? true : t.status === status).length})
            </button>
          ))}
        </div>

        <div className="grid gap-4">
          {filteredTasks.map(task => (
            <div key={task.id} className="bg-white rounded-lg shadow-sm p-6">
              <div className="flex items-start justify-between">
                <div className="flex items-start gap-4">
                  <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${
                    task.status === 'completed' ? 'bg-green-100' :
                    task.status === 'inProgress' ? 'bg-blue-100' :
                    'bg-gray-100'
                  }`}>
                    {task.status === 'completed' ? 
                      <CheckCircle className="w-5 h-5 text-green-600" /> :
                      task.status === 'inProgress' ?
                      <Clock className="w-5 h-5 text-blue-600" /> :
                      <AlertCircle className="w-5 h-5 text-gray-600" />
                    }
                  </div>
                  <div>
                    <h3 className="font-semibold">{task.title}</h3>
                    <div className="flex items-center gap-4 mt-2 text-sm">
                      <span className="text-gray-600">Responsável: {task.assignee}</span>
                      <span className={`font-medium ${
                        task.priority === 'urgent' ? 'text-red-600' :
                        task.priority === 'high' ? 'text-yellow-600' :
                        task.priority === 'medium' ? 'text-blue-600' :
                        'text-gray-600'
                      }`}>
                        {t(task.priority)}
                      </span>
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <div className="text-right">
                    <div className="text-sm text-gray-600">Prazo</div>
                    <div className="font-medium">{new Date(task.due).toLocaleDateString('pt-BR')}</div>
                  </div>
                  <select
                    value={task.status}
                    onChange={(e) => handleTaskUpdate(task.id, e.target.value)}
                    className="px-3 py-1 border rounded-lg text-sm focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="pending">{t('pending')}</option>
                    <option value="inProgress">{t('inProgress')}</option>
                    <option value="completed">{t('completed')}</option>
                  </select>
                  {hasPermission('delete') && (
                    <button
                      onClick={() => handleTaskDelete(task.id)}
                      className="p-2 text-red-600 hover:bg-red-50 rounded-lg"
                      title="Deletar tarefa"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  // Crew Module Component
  const CrewModule = () => {
    const [selectedDepartment, setSelectedDepartment] = useState('all');
    const { openModal, closeModal } = useModal();

    const departments = ['all', 'Direction', 'Production', 'Camera', 'Cast', 'Electric', 'Wardrobe'];
    
    const filteredCrew = productionData.crew.filter(member => {
      if (selectedDepartment === 'all') return true;
      return member.department === selectedDepartment;
    });

    const handleAddCrewMember = () => {
      openModal((modalId) => {
        const [memberData, setMemberData] = useState({
          name: '',
          role: '',
          department: 'Direction',
          phone: '',
          email: '',
          dayRate: ''
        });

        return (
          <div className="p-6">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-semibold">Adicionar Membro da Equipe</h2>
              <button
                onClick={() => closeModal(modalId)}
                className="p-2 hover:bg-gray-100 rounded-lg"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
            
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Nome
                  </label>
                  <input
                    type="text"
                    value={memberData.name}
                    onChange={(e) => setMemberData({...memberData, name: e.target.value})}
                    className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    {t('role')}
                  </label>
                  <input
                    type="text"
                    value={memberData.role}
                    onChange={(e) => setMemberData({...memberData, role: e.target.value})}
                    className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    {t('department')}
                  </label>
                  <select 
                    value={memberData.department}
                    onChange={(e) => setMemberData({...memberData, department: e.target.value})}
                    className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                  >
                    {departments.filter(d => d !== 'all').map(dept => (
                      <option key={dept} value={dept}>{dept}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    {t('dayRate')}
                  </label>
                  <input
                    type="number"
                    value={memberData.dayRate}
                    onChange={(e) => setMemberData({...memberData, dayRate: e.target.value})}
                    className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                    placeholder="0.00"
                  />
                </div>
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    {t('phone')}
                  </label>
                  <input
                    type="tel"
                    value={memberData.phone}
                    onChange={(e) => setMemberData({...memberData, phone: e.target.value})}
                    className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    {t('email')}
                  </label>
                  <input
                    type="email"
                    value={memberData.email}
                    onChange={(e) => setMemberData({...memberData, email: e.target.value})}
                    className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>
              
              <div className="flex justify-end gap-3 mt-6">
                <button
                  onClick={() => closeModal(modalId)}
                  className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg"
                >
                  {t('cancel')}
                </button>
                <button
                  onClick={() => {
                    if (memberData.name && memberData.role && memberData.email) {
                      const newMember = {
                        id: Date.now(),
                        ...memberData,
                        dayRate: parseFloat(memberData.dayRate) || 0,
                        union: 'N/A',
                        daysWorked: 0
                      };
                      setProductionData(prev => ({
                        ...prev,
                        crew: [...prev.crew, newMember]
                      }));
                      closeModal(modalId);
                      addNotification({
                        message: 'Membro da equipe adicionado com sucesso!',
                        type: 'success',
                        priority: 'normal'
                      });
                    } else {
                      addNotification({
                        message: 'Preencha nome, função e email',
                        type: 'error',
                        priority: 'high'
                      });
                    }
                  }}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  {t('save')}
                </button>
              </div>
            </div>
          </div>
        );
      });
    };

    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-bold">{t('modules.crew')}</h1>
          <button
            onClick={handleAddCrewMember}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center gap-2"
          >
            <Plus className="w-4 h-4" />
            Adicionar Membro
          </button>
        </div>

        <div className="flex gap-2">
          {departments.map(dept => (
            <button
              key={dept}
              onClick={() => setSelectedDepartment(dept)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                selectedDepartment === dept 
                  ? 'bg-blue-500 text-white' 
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {dept === 'all' ? t('all') : dept}
            </button>
          ))}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredCrew.map(member => (
            <div key={member.id} className="bg-white rounded-lg shadow-sm p-6">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold">
                    {member.name.split(' ').map(n => n[0]).join('')}
                  </div>
                  <div>
                    <h3 className="font-semibold">{member.name}</h3>
                    <p className="text-sm text-gray-600">{member.role}</p>
                  </div>
                </div>
                <button className="p-1 hover:bg-gray-100 rounded">
                  <MoreVertical className="w-4 h-4 text-gray-400" />
                </button>
              </div>
              
              <div className="space-y-2 text-sm">
                <div className="flex items-center gap-2 text-gray-600">
                  <Building2 className="w-4 h-4" />
                  <span>{member.department}</span>
                </div>
                <div className="flex items-center gap-2 text-gray-600">
                  <Phone className="w-4 h-4" />
                  <span>{member.phone}</span>
                </div>
                <div className="flex items-center gap-2 text-gray-600">
                  <Mail className="w-4 h-4" />
                  <span className="truncate">{member.email}</span>
                </div>
                <div className="flex items-center gap-2 text-gray-600">
                  <DollarSign className="w-4 h-4" />
                  <span>R$ {member.dayRate.toLocaleString('pt-BR')}/dia</span>
                </div>
                <div className="flex items-center gap-2 text-gray-600">
                  <Calendar className="w-4 h-4" />
                  <span>{member.daysWorked} dias trabalhados</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  // Schedule Module
  const ScheduleModule = () => {
    const [viewMode, setViewMode] = useState('list'); // list or calendar
    const { openModal, closeModal } = useModal();

    const handleAddScheduleItem = () => {
      openModal((modalId) => {
        const [scheduleData, setScheduleData] = useState({
          date: '',
          scenes: '',
          location: '',
          callTime: '08:00',
          status: 'confirmed'
        });

        return (
          <div className="p-6">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-semibold">Adicionar ao Cronograma</h2>
              <button
                onClick={() => closeModal(modalId)}
                className="p-2 hover:bg-gray-100 rounded-lg"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Data
                </label>
                <input
                  type="date"
                  value={scheduleData.date}
                  onChange={(e) => setScheduleData({...scheduleData, date: e.target.value})}
                  className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  {t('scenes')}
                </label>
                <input
                  type="text"
                  value={scheduleData.scenes}
                  onChange={(e) => setScheduleData({...scheduleData, scenes: e.target.value})}
                  placeholder="Ex: 1, 2A, 3B"
                  className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  {t('location')}
                </label>
                <input
                  type="text"
                  value={scheduleData.location}
                  onChange={(e) => setScheduleData({...scheduleData, location: e.target.value})}
                  className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Horário de Chamada
                  </label>
                  <input
                    type="time"
                    value={scheduleData.callTime}
                    onChange={(e) => setScheduleData({...scheduleData, callTime: e.target.value})}
                    className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    {t('status')}
                  </label>
                  <select 
                    value={scheduleData.status}
                    onChange={(e) => setScheduleData({...scheduleData, status: e.target.value})}
                    className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="confirmed">Confirmado</option>
                    <option value="tentative">Tentativo</option>
                    <option value="cancelled">Cancelado</option>
                  </select>
                </div>
              </div>
              
              <div className="flex justify-end gap-3 mt-6">
                <button
                  onClick={() => closeModal(modalId)}
                  className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg"
                >
                  {t('cancel')}
                </button>
                <button
                  onClick={() => {
                    if (scheduleData.date && scheduleData.scenes && scheduleData.location) {
                      const newScheduleItem = {
                        id: Date.now(),
                        ...scheduleData,
                        scenes: scheduleData.scenes.split(',').map(s => s.trim())
                      };
                      setProductionData(prev => ({
                        ...prev,
                        schedule: [...prev.schedule, newScheduleItem]
                      }));
                      closeModal(modalId);
                      addNotification({
                        message: 'Item adicionado ao cronograma!',
                        type: 'success',
                        priority: 'normal'
                      });
                    } else {
                      addNotification({
                        message: 'Preencha todos os campos obrigatórios',
                        type: 'error',
                        priority: 'high'
                      });
                    }
                  }}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  {t('save')}
                </button>
              </div>
            </div>
          </div>
        );
      });
    };

    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-bold">{t('modules.schedule')}</h1>
          <div className="flex gap-3">
            <div className="flex bg-gray-100 rounded-lg p-1">
              <button
                onClick={() => setViewMode('list')}
                className={`px-3 py-1 rounded text-sm transition-all ${
                  viewMode === 'list' ? 'bg-white shadow-sm' : ''
                }`}
              >
                <List className="w-4 h-4" />
              </button>
              <button
                onClick={() => setViewMode('calendar')}
                className={`px-3 py-1 rounded text-sm transition-all ${
                  viewMode === 'calendar' ? 'bg-white shadow-sm' : ''
                }`}
              >
                <Calendar className="w-4 h-4" />
              </button>
            </div>
            <button
              onClick={handleAddScheduleItem}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center gap-2"
            >
              <Plus className="w-4 h-4" />
              Adicionar
            </button>
          </div>
        </div>

        {viewMode === 'list' ? (
          <div className="space-y-4">
            {productionData.schedule.map(item => (
              <div key={item.id} className="bg-white rounded-lg shadow-sm p-6">
                <div className="flex items-start justify-between">
                  <div className="flex items-start gap-4">
                    <div className="w-16 text-center">
                      <div className="text-2xl font-bold text-blue-600">
                        {new Date(item.date).getDate()}
                      </div>
                      <div className="text-xs text-gray-600 uppercase">
                        {new Date(item.date).toLocaleDateString('pt-BR', { month: 'short' })}
                      </div>
                    </div>
                    <div>
                      <h3 className="font-semibold mb-1">
                        Cenas: {item.scenes.join(', ')}
                      </h3>
                      <div className="flex items-center gap-4 text-sm text-gray-600">
                        <span className="flex items-center gap-1">
                          <MapPin className="w-4 h-4" />
                          {item.location}
                        </span>
                        <span className="flex items-center gap-1">
                          <Clock className="w-4 h-4" />
                          {item.callTime}
                        </span>
                      </div>
                    </div>
                  </div>
                  <span className={`px-3 py-1 text-xs rounded-full ${
                    item.status === 'confirmed' ? 'bg-green-100 text-green-800' :
                    item.status === 'tentative' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-red-100 text-red-800'
                  }`}>
                    {item.status === 'confirmed' ? 'Confirmado' :
                     item.status === 'tentative' ? 'Tentativo' :
                     'Cancelado'}
                  </span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="bg-white rounded-lg shadow-sm p-6">
            <div className="text-center text-gray-500 py-12">
              <Calendar className="w-16 h-16 mx-auto mb-4 text-gray-300" />
              <p>Visualização em calendário em desenvolvimento</p>
            </div>
          </div>
        )}
      </div>
    );
  };

  // Documents Module
  const DocumentsModule = () => {
    const [selectedType, setSelectedType] = useState('all');
    const { openModal, closeModal } = useModal();

    const documentTypes = ['all', 'script', 'budget', 'images', 'contracts', 'reports'];
    
    const filteredDocuments = productionData.documents.filter(doc => {
      if (selectedType === 'all') return true;
      return doc.type === selectedType;
    });

    const getDocumentIcon = (type) => {
      switch(type) {
        case 'script': return FileText;
        case 'budget': return BarChart2;
        case 'images': return Image;
        default: return FileText;
      }
    };

    const handleUploadDocument = () => {
      openModal((modalId) => {
        const [documentData, setDocumentData] = useState({
          name: '',
          type: 'script',
          department: 'Direction'
        });

        return (
          <div className="p-6">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-semibold">Upload de Documento</h2>
              <button
                onClick={() => closeModal(modalId)}
                className="p-2 hover:bg-gray-100 rounded-lg"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
            
            <div className="space-y-4">
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
                <Upload className="w-12 h-12 mx-auto text-gray-400 mb-4" />
                <p className="text-gray-600 mb-2">Arraste arquivos aqui ou</p>
                <button 
                  onClick={() => {
                    // Simular nome de arquivo
                    const fileNames = ['Documento_v1.pdf', 'Relatorio_final.xlsx', 'Imagens_locacao.zip', 'Script_revisado.docx'];
                    const randomName = fileNames[Math.floor(Math.random() * fileNames.length)];
                    setDocumentData({...documentData, name: randomName});
                  }}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  Selecionar Arquivos
                </button>
              </div>
              
              {documentData.name && (
                <div className="p-3 bg-gray-50 rounded-lg">
                  <p className="text-sm text-gray-700">Arquivo selecionado: {documentData.name}</p>
                </div>
              )}
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Tipo de Documento
                </label>
                <select 
                  value={documentData.type}
                  onChange={(e) => setDocumentData({...documentData, type: e.target.value})}
                  className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                >
                  {documentTypes.filter(t => t !== 'all').map(type => (
                    <option key={type} value={type}>{type}</option>
                  ))}
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  {t('department')}
                </label>
                <select 
                  value={documentData.department}
                  onChange={(e) => setDocumentData({...documentData, department: e.target.value})}
                  className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                >
                  <option>Direction</option>
                  <option>Production</option>
                  <option>Camera</option>
                  <option>Art</option>
                </select>
              </div>
              
              <div className="flex justify-end gap-3 mt-6">
                <button
                  onClick={() => closeModal(modalId)}
                  className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg"
                >
                  {t('cancel')}
                </button>
                <button
                  onClick={() => {
                    if (documentData.name) {
                      const newDocument = {
                        id: Date.now(),
                        ...documentData,
                        size: `${(Math.random() * 50 + 0.5).toFixed(1)}MB`,
                        lastModified: new Date().toISOString().split('T')[0],
                        uploadedBy: appState.currentUser?.name || 'User'
                      };
                      setProductionData(prev => ({
                        ...prev,
                        documents: [...prev.documents, newDocument]
                      }));
                      closeModal(modalId);
                      addNotification({
                        message: 'Documento enviado com sucesso!',
                        type: 'success',
                        priority: 'normal'
                      });
                    } else {
                      addNotification({
                        message: 'Selecione um arquivo primeiro',
                        type: 'error',
                        priority: 'high'
                      });
                    }
                  }}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  Upload
                </button>
              </div>
            </div>
          </div>
        );
      });
    };

    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-bold">{t('modules.documents')}</h1>
          <button
            onClick={handleUploadDocument}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center gap-2"
          >
            <Upload className="w-4 h-4" />
            Upload
          </button>
        </div>

        <div className="flex gap-2">
          {documentTypes.map(type => (
            <button
              key={type}
              onClick={() => setSelectedType(type)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                selectedType === type 
                  ? 'bg-blue-500 text-white' 
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {type === 'all' ? t('all') : type}
            </button>
          ))}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredDocuments.map(doc => {
            const Icon = getDocumentIcon(doc.type);
            return (
              <div key={doc.id} className="bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition-shadow">
                <div className="flex items-start justify-between mb-4">
                  <div className="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center">
                    <Icon className="w-6 h-6 text-gray-600" />
                  </div>
                  <button className="p-1 hover:bg-gray-100 rounded">
                    <MoreVertical className="w-4 h-4 text-gray-400" />
                  </button>
                </div>
                
                <h3 className="font-semibold mb-2 truncate">{doc.name}</h3>
                
                <div className="space-y-1 text-sm text-gray-600">
                  <p>Tamanho: {doc.size}</p>
                  <p>Modificado: {new Date(doc.lastModified).toLocaleDateString('pt-BR')}</p>
                  <p>Por: {doc.uploadedBy}</p>
                </div>
                
                <div className="flex gap-2 mt-4">
                  <button className="flex-1 px-3 py-1 text-sm bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors">
                    <Download className="w-4 h-4 inline mr-1" />
                    Baixar
                  </button>
                  <button className="flex-1 px-3 py-1 text-sm bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors">
                    <Share2 className="w-4 h-4 inline mr-1" />
                    Compartilhar
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    );
  };

  // Reports Module
  const ReportsModule = () => {
    const reportTypes = [
      { id: 'daily', name: 'Relatório Diário', icon: Calendar, bgClass: 'bg-blue-100', iconClass: 'text-blue-600' },
      { id: 'financial', name: 'Relatório Financeiro', icon: DollarSign, bgClass: 'bg-green-100', iconClass: 'text-green-600' },
      { id: 'crew', name: 'Relatório de Equipe', icon: Users, bgClass: 'bg-purple-100', iconClass: 'text-purple-600' },
      { id: 'progress', name: 'Relatório de Progresso', icon: TrendingUp, bgClass: 'bg-orange-100', iconClass: 'text-orange-600' }
    ];

    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-bold">{t('modules.reports')}</h1>
          <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center gap-2">
            <FileBarChart className="w-4 h-4" />
            Gerar Relatório
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {reportTypes.map(report => {
            const Icon = report.icon;
            return (
              <div key={report.id} className="bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition-shadow cursor-pointer">
                <div className="flex items-center gap-4 mb-4">
                  <div className={`w-12 h-12 ${report.bgClass} rounded-lg flex items-center justify-center`}>
                    <Icon className={`w-6 h-6 ${report.iconClass}`} />
                  </div>
                  <h3 className="text-lg font-semibold">{report.name}</h3>
                </div>
                
                <p className="text-gray-600 mb-4">
                  Visualize e exporte relatórios detalhados sobre {report.name.toLowerCase()}.
                </p>
                
                <button className="text-blue-600 hover:text-blue-700 font-medium text-sm flex items-center gap-1">
                  Visualizar
                  <ArrowRight className="w-4 h-4" />
                </button>
              </div>
            );
          })}
        </div>

        <div className="bg-white rounded-lg shadow-sm p-6">
          <h2 className="text-lg font-semibold mb-4">Relatórios Recentes</h2>
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center gap-3">
                <FileBarChart className="w-5 h-5 text-gray-600" />
                <div>
                  <p className="font-medium">Relatório Diário - 19/01/2024</p>
                  <p className="text-sm text-gray-600">Gerado por Sofia Luz</p>
                </div>
              </div>
              <button className="text-blue-600 hover:text-blue-700 text-sm">
                Baixar
              </button>
            </div>
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center gap-3">
                <FileBarChart className="w-5 h-5 text-gray-600" />
                <div>
                  <p className="font-medium">Relatório Financeiro - 15/01/2024</p>
                  <p className="text-sm text-gray-600">Gerado por Marcus Terra</p>
                </div>
              </div>
              <button className="text-blue-600 hover:text-blue-700 text-sm">
                Baixar
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  };

  // Settings Module
  const SettingsModule = () => {
    const [activeTab, setActiveTab] = useState('preferences');
    
    return (
      <div className="space-y-6">
        <h1 className="text-2xl font-bold">{t('settings')}</h1>
        
        <div className="bg-white rounded-lg shadow-sm">
          <div className="border-b border-gray-200">
            <nav className="flex -mb-px">
              {['preferences', 'notifications', 'security'].map(tab => (
                <button
                  key={tab}
                  onClick={() => setActiveTab(tab)}
                  className={`py-2 px-4 border-b-2 font-medium text-sm ${
                    activeTab === tab
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  {t(tab)}
                </button>
              ))}
            </nav>
          </div>
          
          <div className="p-6">
            {activeTab === 'preferences' && (
              <div className="space-y-6">
                <div>
                  <h3 className="text-lg font-medium mb-4">Preferências Gerais</h3>
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Idioma
                      </label>
                      <select 
                        value={appState.language}
                        onChange={(e) => updateAppState({ language: e.target.value })}
                        className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                      >
                        <option value="pt">Português</option>
                        <option value="en">English</option>
                      </select>
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Tema
                      </label>
                      <select 
                        value={appState.theme}
                        onChange={(e) => updateAppState({ theme: e.target.value })}
                        className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                      >
                        <option value="light">Claro</option>
                        <option value="dark">Escuro</option>
                      </select>
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Fuso Horário
                      </label>
                      <select className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500">
                        <option>São Paulo (GMT-3)</option>
                        <option>Los Angeles (GMT-8)</option>
                        <option>New York (GMT-5)</option>
                      </select>
                    </div>
                  </div>
                </div>
              </div>
            )}
            
            {activeTab === 'notifications' && (
              <div className="space-y-6">
                <div>
                  <h3 className="text-lg font-medium mb-4">Configurações de Notificação</h3>
                  <div className="space-y-4">
                    <label className="flex items-center">
                      <input type="checkbox" className="mr-3" defaultChecked />
                      <div>
                        <p className="font-medium">Notificações por Email</p>
                        <p className="text-sm text-gray-600">Receba atualizações importantes por email</p>
                      </div>
                    </label>
                    
                    <label className="flex items-center">
                      <input type="checkbox" className="mr-3" defaultChecked />
                      <div>
                        <p className="font-medium">Notificações Push</p>
                        <p className="text-sm text-gray-600">Receba notificações em tempo real</p>
                      </div>
                    </label>
                    
                    <label className="flex items-center">
                      <input type="checkbox" className="mr-3" />
                      <div>
                        <p className="font-medium">Notificações SMS</p>
                        <p className="text-sm text-gray-600">Receba alertas críticos por SMS</p>
                      </div>
                    </label>
                  </div>
                </div>
              </div>
            )}
            
            {activeTab === 'security' && (
              <div className="space-y-6">
                <div>
                  <h3 className="text-lg font-medium mb-4">Segurança da Conta</h3>
                  <div className="space-y-4">
                    <div>
                      <p className="font-medium mb-2">Autenticação de Dois Fatores</p>
                      <p className="text-sm text-gray-600 mb-3">
                        Adicione uma camada extra de segurança à sua conta
                      </p>
                      <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                        {appState.currentUser?.twoFactorEnabled ? 'Desativar 2FA' : 'Ativar 2FA'}
                      </button>
                    </div>
                    
                    <div>
                      <p className="font-medium mb-2">Alterar Senha</p>
                      <p className="text-sm text-gray-600 mb-3">
                        Recomendamos alterar sua senha regularmente
                      </p>
                      <button className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
                        Alterar Senha
                      </button>
                    </div>
                    
                    <div>
                      <p className="font-medium mb-2">Sessões Ativas</p>
                      <p className="text-sm text-gray-600 mb-3">
                        Gerencie os dispositivos conectados à sua conta
                      </p>
                      <button className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
                        Ver Sessões
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    );
  };

  // Profile Module
  const ProfileModule = () => {
    const [isEditing, setIsEditing] = useState(false);
    const [profileData, setProfileData] = useState({
      name: appState.currentUser?.name || '',
      email: appState.currentUser?.email || '',
      phone: appState.currentUser?.phone || '',
      role: appState.currentUser?.role || '',
      department: appState.currentUser?.department || ''
    });

    const handleSaveProfile = () => {
      updateAppState({
        currentUser: {
          ...appState.currentUser,
          ...profileData
        }
      });
      setIsEditing(false);
      addNotification({
        message: 'Perfil atualizado com sucesso!',
        type: 'success',
        priority: 'normal'
      });
    };

    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-bold">{t('myProfile')}</h1>
          {!isEditing && (
            <button
              onClick={() => setIsEditing(true)}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center gap-2"
            >
              <Edit className="w-4 h-4" />
              Editar Perfil
            </button>
          )}
        </div>

        <div className="bg-white rounded-lg shadow-sm p-6">
          <div className="flex items-center gap-6 mb-6">
            <div className="w-24 h-24 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white text-2xl font-bold">
              {appState.currentUser?.avatar}
            </div>
            <div>
              <h2 className="text-2xl font-bold">{appState.currentUser?.name}</h2>
              <p className="text-gray-600">{appState.currentUser?.role} • {appState.currentUser?.department}</p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Nome Completo
              </label>
              <input
                type="text"
                value={profileData.name}
                onChange={(e) => setProfileData({ ...profileData, name: e.target.value })}
                disabled={!isEditing}
                className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 disabled:bg-gray-50"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Email
              </label>
              <input
                type="email"
                value={profileData.email}
                onChange={(e) => setProfileData({ ...profileData, email: e.target.value })}
                disabled={!isEditing}
                className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 disabled:bg-gray-50"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Telefone
              </label>
              <input
                type="tel"
                value={profileData.phone}
                onChange={(e) => setProfileData({ ...profileData, phone: e.target.value })}
                disabled={!isEditing}
                className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 disabled:bg-gray-50"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Função
              </label>
              <input
                type="text"
                value={profileData.role}
                disabled={true}
                className="w-full px-3 py-2 border rounded-lg bg-gray-50"
              />
            </div>
          </div>

          {isEditing && (
            <div className="flex justify-end gap-3 mt-6">
              <button
                onClick={() => {
                  setIsEditing(false);
                  setProfileData({
                    name: appState.currentUser?.name || '',
                    email: appState.currentUser?.email || '',
                    phone: appState.currentUser?.phone || '',
                    role: appState.currentUser?.role || '',
                    department: appState.currentUser?.department || ''
                  });
                }}
                className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg"
              >
                Cancelar
              </button>
              <button
                onClick={handleSaveProfile}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
              >
                Salvar Alterações
              </button>
            </div>
          )}
        </div>

        <div className="bg-white rounded-lg shadow-sm p-6">
          <h3 className="text-lg font-semibold mb-4">Estatísticas</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">
                {appState.currentUser?.projects || 0}
              </div>
              <div className="text-sm text-gray-600">Projetos</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">
                {appState.currentUser?.daysWorked || 0}
              </div>
              <div className="text-sm text-gray-600">Dias Trabalhados</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-purple-600">
                {productionData.tasks.filter(t => t.assignee === appState.currentUser?.name && t.status === 'completed').length}
              </div>
              <div className="text-sm text-gray-600">Tarefas Concluídas</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-orange-600">
                98.5%
              </div>
              <div className="text-sm text-gray-600">Pontualidade</div>
            </div>
          </div>
        </div>
      </div>
    );
  };

  // Componente Principal do Sistema (com Dashboard, Header, Sidebar)
  const MainSystem = () => {
    const [userMenuOpen, setUserMenuOpen] = useState(false);
    const [notificationsOpen, setNotificationsOpen] = useState(false);

    const unreadNotifications = notifications.filter(n => n.unread).length;

    const moduleIcons = {
      dashboard: Home,
      callsheets: Clapperboard,
      schedule: Calendar,
      stripboard: Layers,
      breakdown: FileText,
      crew: Users,
      documents: FolderOpen,
      tasks: ListChecks,
      budget: DollarSign,
      reports: FileBarChart,
      communication: MessageCircle,
      postproduction: Video,
      dood: Film,
      admin: Shield,
      analytics: BarChart2,
      inventory: Package,
      profile: User,
      settings: Settings
    };

    const renderModule = () => {
      switch(activeModule) {
        case 'dashboard': return <Dashboard />;
        case 'callsheets': return <CallSheetsModule />;
        case 'tasks': return <TasksModule />;
        case 'crew': return <CrewModule />;
        case 'schedule': return <ScheduleModule />;
        case 'documents': return <DocumentsModule />;
        case 'reports': return <ReportsModule />;
        case 'settings': return <SettingsModule />;
        case 'profile': return <ProfileModule />;
        default:
          return (
            <div className="flex items-center justify-center h-96">
              <div className="text-center">
                <div className="w-16 h-16 bg-gray-200 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Settings className="w-8 h-8 text-gray-500" />
                </div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">Módulo em Desenvolvimento</h3>
                <p className="text-gray-600">Este módulo estará disponível em breve.</p>
              </div>
            </div>
          );
      }
    };

    const handleLogout = () => {
      updateAppState({
        currentUser: null,
        isAuthenticated: false,
        authToken: null
      });
      setCurrentProject(null);
      setNotifications([]);
      addNotification({
        message: 'Logout realizado com sucesso!',
        type: 'success',
        priority: 'high'
      });
    };

    return (
      <div className="flex h-screen bg-gray-50">
        {/* Sidebar */}
        <div className={`${sidebarOpen ? 'w-64' : 'w-20'} bg-gradient-to-b from-gray-900 to-gray-800 text-white transition-all duration-300 flex flex-col`}>
          <div className="p-4 border-b border-gray-700">
            <div className="flex items-center justify-between">
              <div className={`flex items-center gap-3 ${!sidebarOpen && 'justify-center'}`}>
                <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                  <Film className="w-6 h-6 text-white" />
                </div>
                {sidebarOpen && (
                  <div>
                    <h1 className="font-bold text-lg">CineProd</h1>
                    <p className="text-xs text-gray-400">Systems</p>
                  </div>
                )}
              </div>
              <button
                onClick={() => setSidebarOpen(!sidebarOpen)}
                className="p-1 hover:bg-gray-700 rounded-lg transition-colors"
              >
                {sidebarOpen ? <ChevronLeft className="w-5 h-5" /> : <ChevronRight className="w-5 h-5" />}
              </button>
            </div>
          </div>

          <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
            {Object.entries(moduleIcons).map(([module, Icon]) => {
              if (!canAccessModule(module)) return null;
              
              return (
                <button
                  key={module}
                  onClick={() => setActiveModule(module)}
                  className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg transition-all ${
                    activeModule === module
                      ? 'bg-blue-600 text-white shadow-lg'
                      : 'hover:bg-gray-700 text-gray-300'
                  } ${!sidebarOpen && 'justify-center'}`}
                  title={!sidebarOpen ? t(`modules.${module}`) : ''}
                >
                  <Icon className="w-5 h-5 flex-shrink-0" />
                  {sidebarOpen && (
                    <span className="text-sm font-medium">{t(`modules.${module}`)}</span>
                  )}
                </button>
              );
            })}
          </nav>

          {sidebarOpen && currentProject && (
            <div className="p-4 border-t border-gray-700">
              <p className="text-xs text-gray-400 mb-1">Projeto Atual</p>
              <p className="text-sm font-medium truncate">{currentProject.name}</p>
              <div className="mt-2 space-y-1">
                <div className="flex justify-between text-xs">
                  <span className="text-gray-400">Progresso</span>
                  <span>{Math.round((currentProject.completedDays / currentProject.shootingDays) * 100)}%</span>
                </div>
                <div className="w-full bg-gray-700 rounded-full h-1.5">
                  <div 
                    className="bg-blue-500 h-1.5 rounded-full"
                    style={{ width: `${(currentProject.completedDays / currentProject.shootingDays) * 100}%` }}
                  />
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Main Content */}
        <div className="flex-1 flex flex-col">
          {/* Header */}
          <header className="bg-white shadow-sm border-b border-gray-200">
            <div className="flex items-center justify-between px-6 py-4">
              <div className="flex items-center gap-4 flex-1">
                <button
                  onClick={() => setSidebarOpen(!sidebarOpen)}
                  className="p-2 hover:bg-gray-100 rounded-lg lg:hidden"
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