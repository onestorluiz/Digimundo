import React, { useState, useEffect, useCallback, useMemo, useRef, createContext, useContext } from 'react';
import { 
  // Ícones principais
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
  RefreshCw, PlayCircle, Pause, SkipForward, UserCheck, Clipboard,
  UserX, UserPlus, EyeOff, Info, Smartphone, Monitor, Building,
  Megaphone, Headphones, Mic, MicOff, VideoOff, MoreVertical, Star,
  Building2, FileBarChart, Moon, User, Save, PlusCircle, Wallet,
  FileDown, FilePlus, ChevronUp, MessageSquare, Paperclip, Lightbulb,
  Bookmark, Archive, Link, Inbox, Hash, AtSign, Tag, Flag, HardDrive,
  BookOpen, Code, Terminal, Cpu, Server, Crosshair, Cast, Airplay,
  Anchor, Battery, BatteryCharging, Bluetooth, CreditCard, Disc, Loader,
  SunIcon, MoonIcon, Sunrise, Sunset, CloudSnow, Gauge, Wrench,
  Scissors, Brush, PenTool, Type, Bold, Italic, Underline, AlignLeft
} from 'lucide-react';

// ============================
// SISTEMA CINEPROD ULTIMATE
// ============================
// Versão completa com todas as funcionalidades
// Baseado em StudioBinder + melhorias customizadas

const CineProUltimate = () => {
  // ==================== ESTADOS PRINCIPAIS ====================
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [currentUser, setCurrentUser] = useState(null);
  const [activeModule, setActiveModule] = useState('dashboard');
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [theme, setTheme] = useState('dark');
  const [language, setLanguage] = useState('pt-BR');
  const [notifications, setNotifications] = useState([]);
  const [projects, setProjects] = useState([]);
  const [currentProject, setCurrentProject] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [showNotifications, setShowNotifications] = useState(false);
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [globalLoading, setGlobalLoading] = useState(false);
  
  // Estados avançados
  const [chatMessages, setChatMessages] = useState([]);
  const [activities, setActivities] = useState([]);
  const [weatherData, setWeatherData] = useState(null);
  const [callSheets, setCallSheets] = useState([]);
  const [scripts, setScripts] = useState([]);
  const [budget, setBudget] = useState(null);
  const [schedule, setSchedule] = useState([]);
  const [crew, setCrew] = useState([]);
  const [equipment, setEquipment] = useState([]);
  const [locations, setLocations] = useState([]);
  const [documents, setDocuments] = useState([]);
  const [contacts, setContacts] = useState([]);
  const [shotList, setShotList] = useState([]);
  const [storyboard, setStoryboard] = useState([]);
  
  // ==================== BANCO DE DADOS MOCK ====================
  const database = {
    users: [
      {
        id: 'user-001',
        name: 'Sofia Luz',
        email: 'sofia@cinepro.com',
        password: 'demo123',
        role: 'Director',
        department: 'Direction',
        phone: '+55 11 98765-4321',
        avatar: 'SL',
        permissions: ['all'],
        status: 'online',
        twoFactor: false
      },
      {
        id: 'user-002',
        name: 'Marcus Terra',
        email: 'marcus@cinepro.com',
        password: 'demo123',
        role: 'Producer',
        department: 'Production',
        phone: '+55 11 98765-4322',
        avatar: 'MT',
        permissions: ['all'],
        status: 'online',
        twoFactor: false
      },
      {
        id: 'user-003',
        name: 'Luna Sombra',
        email: 'luna@cinepro.com',
        password: 'demo123',
        role: 'Director of Photography',
        department: 'Camera',
        phone: '+55 11 98765-4323',
        avatar: 'LS',
        permissions: ['read', 'write', 'edit'],
        status: 'offline',
        twoFactor: true
      },
      {
        id: 'user-004',
        name: 'Rio Vento',
        email: 'rio@cinepro.com',
        password: 'demo123',
        role: 'Art Director',
        department: 'Art',
        phone: '+55 11 98765-4324',
        avatar: 'RV',
        permissions: ['read', 'write'],
        status: 'busy',
        twoFactor: false
      },
      {
        id: 'user-005',
        name: 'Admin System',
        email: 'admin@cinepro.com',
        password: 'admin123',
        role: 'System Administrator',
        department: 'IT',
        phone: '+55 11 98765-4320',
        avatar: 'AD',
        permissions: ['all', 'admin'],
        status: 'online',
        twoFactor: true
      }
    ],
    
    projects: [
      {
        id: 'proj-001',
        title: 'Eclipse - O Filme',
        type: 'Feature Film',
        genre: 'Sci-Fi/Drama',
        status: 'Production',
        phase: 'Principal Photography',
        budget: 5000000,
        spent: 3225000,
        startDate: '2024-01-10',
        endDate: '2024-04-15',
        shootingDays: 60,
        completedDays: 38,
        director: 'Sofia Luz',
        producer: 'Marcus Terra',
        dop: 'Luna Sombra',
        writer: 'Alex Rivers',
        editor: 'Sam Sky',
        composer: 'Jazz Moon',
        description: 'Um épico de ficção científica sobre a última esperança da humanidade durante um eclipse solar permanente.',
        synopsis: 'Em 2055, um eclipse solar anômalo mergulha a Terra em escuridão permanente. A Dra. Elena Vasquez lidera uma missão desesperada para restaurar a luz solar.',
        logline: 'Uma cientista deve salvar a humanidade quando um eclipse eterno ameaça extinguir toda vida na Terra.',
        posterUrl: '/assets/posters/eclipse.jpg',
        locations: ['São Paulo', 'Rio de Janeiro', 'Brasília'],
        cast: [
          { name: 'Ana Silva', role: 'Dra. Elena Vasquez', status: 'confirmed' },
          { name: 'Pedro Santos', role: 'Captain Marcus', status: 'confirmed' },
          { name: 'Julia Costa', role: 'AI System LUNA', status: 'pending' }
        ],
        progress: {
          preProduction: 100,
          production: 63,
          postProduction: 0,
          distribution: 0
        }
      },
      {
        id: 'proj-002',
        title: 'Urban Shadows - Series',
        type: 'TV Series',
        genre: 'Drama/Thriller',
        status: 'Pre-Production',
        phase: 'Script Development',
        budget: 8000000,
        spent: 1200000,
        startDate: '2024-02-01',
        endDate: '2024-06-30',
        shootingDays: 90,
        completedDays: 12,
        director: 'Alex Rivers',
        producer: 'Marcus Terra',
        dop: 'Luna Sombra',
        writer: 'Sara Night',
        showrunner: 'Marcus Terra',
        description: 'Série dramática explorando os segredos obscuros de uma metrópole moderna.',
        synopsis: 'Três famílias poderosas controlam os destinos de São Paulo em uma trama de poder, traição e redenção.',
        seasons: 1,
        episodes: 10,
        episodeDuration: 50,
        network: 'StreamMax',
        cast: [
          { name: 'Carlos Mendes', role: 'Roberto Silva', status: 'confirmed' },
          { name: 'Maria Oliveira', role: 'Detective Laura', status: 'confirmed' }
        ],
        progress: {
          preProduction: 45,
          production: 13,
          postProduction: 0,
          distribution: 0
        }
      },
      {
        id: 'proj-003',
        title: 'Nexus 2024 Campaign',
        type: 'Commercial',
        genre: 'Technology/Lifestyle',
        status: 'Post-Production',
        phase: 'Color Grading',
        budget: 2500000,
        spent: 2100000,
        startDate: '2024-01-15',
        endDate: '2024-03-30',
        shootingDays: 45,
        completedDays: 45,
        director: 'Sofia Luz',
        producer: 'Eva Storm',
        dop: 'Chris Light',
        agency: 'Creative Minds Agency',
        client: 'Nexus Technologies',
        description: 'Campanha publicitária revolucionária para o lançamento do Nexus 2024.',
        deliverables: ['TV Spot 30s', 'TV Spot 15s', 'Digital Campaign', 'Print Ads'],
        platforms: ['TV', 'YouTube', 'Instagram', 'TikTok'],
        targetAudience: '18-35 anos, tech enthusiasts',
        progress: {
          preProduction: 100,
          production: 100,
          postProduction: 84,
          distribution: 0
        }
      }
    ],
    
    callSheets: [
      {
        id: 'cs-001',
        projectId: 'proj-001',
        date: '2024-01-15',
        callTime: '06:00',
        wrap: '18:00',
        location: 'Estúdio A - São Paulo',
        scenes: ['1', '2', '3A'],
        weather: { temp: 25, condition: 'Partly Cloudy', sunrise: '05:45', sunset: '18:30' },
        crew: 45,
        cast: 12,
        status: 'sent',
        notes: 'Breakfast at 5:30 AM. Safety meeting at 6:15 AM.'
      }
    ],
    
    equipment: [
      {
        id: 'eq-001',
        name: 'ARRI Alexa Mini LF',
        category: 'Camera',
        brand: 'ARRI',
        model: 'Alexa Mini LF',
        serial: 'AML-12345',
        status: 'available',
        dailyRate: 2500,
        owner: 'CineProd',
        location: 'Warehouse A',
        lastMaintenance: '2024-01-01',
        nextMaintenance: '2024-04-01'
      },
      {
        id: 'eq-002',
        name: 'Zeiss Master Prime Set',
        category: 'Lens',
        brand: 'Zeiss',
        model: 'Master Prime',
        serial: 'ZMP-SET-001',
        status: 'in-use',
        dailyRate: 1500,
        owner: 'CineProd',
        project: 'proj-001',
        location: 'Set - Eclipse',
        kit: ['16mm', '25mm', '35mm', '50mm', '75mm', '100mm']
      }
    ],
    
    locations: [
      {
        id: 'loc-001',
        name: 'Estúdio CineProd A',
        type: 'Studio',
        address: 'Rua das Câmeras, 100, São Paulo, SP',
        capacity: 200,
        area: '2000m²',
        facilities: ['Green Screen', 'Lighting Grid', 'Sound Stage', 'Dressing Rooms'],
        availability: 'Available',
        dailyRate: 5000,
        contact: 'João Studio - (11) 98765-4321',
        parking: 50,
        powerCapacity: '500kW'
      },
      {
        id: 'loc-002',
        name: 'Edifício Skyline',
        type: 'Location',
        address: 'Av. Paulista, 1000, São Paulo, SP',
        floor: 'Rooftop',
        permits: ['Film Permit #2024-001', 'Safety Certificate'],
        restrictions: 'No filming 22:00 - 06:00',
        contact: 'Building Manager - (11) 3456-7890'
      }
    ]
  };

  // ==================== SISTEMA DE TRADUÇÃO ====================
  const translations = {
    'pt-BR': {
      // Sistema
      appName: 'CineProd Ultimate',
      tagline: 'Sistema Completo de Gestão Cinematográfica',
      welcome: 'Bem-vindo',
      loading: 'Carregando...',
      save: 'Salvar',
      cancel: 'Cancelar',
      delete: 'Excluir',
      edit: 'Editar',
      add: 'Adicionar',
      search: 'Buscar',
      filter: 'Filtrar',
      export: 'Exportar',
      import: 'Importar',
      print: 'Imprimir',
      share: 'Compartilhar',
      download: 'Baixar',
      upload: 'Enviar',
      
      // Auth
      login: 'Entrar',
      logout: 'Sair',
      email: 'Email',
      password: 'Senha',
      rememberMe: 'Lembrar de mim',
      forgotPassword: 'Esqueceu a senha',
      selectProfile: 'Selecione um perfil para acesso rápido',
      invalidCredentials: 'Email ou senha inválidos',
      
      // Menu
      dashboard: 'Dashboard',
      projects: 'Projetos',
      schedule: 'Cronograma',
      crew: 'Equipe',
      equipment: 'Equipamentos',
      locations: 'Locações',
      documents: 'Documentos',
      budget: 'Orçamento',
      callSheets: 'Call Sheets',
      scripts: 'Roteiros',
      shotList: 'Lista de Cenas',
      storyboard: 'Storyboard',
      reports: 'Relatórios',
      contacts: 'Contatos',
      calendar: 'Calendário',
      weather: 'Clima',
      chat: 'Chat',
      settings: 'Configurações',
      help: 'Ajuda',
      
      // Dashboard
      activeProjects: 'Projetos Ativos',
      totalCrew: 'Equipe Total',
      totalBudget: 'Orçamento Total',
      shootingDays: 'Dias de Filmagem',
      upcomingDeadlines: 'Próximos Prazos',
      recentActivities: 'Atividades Recentes',
      productionStatus: 'Status da Produção',
      
      // Projects
      projectDetails: 'Detalhes do Projeto',
      projectType: 'Tipo de Projeto',
      projectStatus: 'Status do Projeto',
      projectPhase: 'Fase Atual',
      genre: 'Gênero',
      director: 'Diretor',
      producer: 'Produtor',
      cinematographer: 'Diretor de Fotografia',
      writer: 'Roteirista',
      editor: 'Editor',
      composer: 'Compositor',
      synopsis: 'Sinopse',
      logline: 'Logline',
      
      // Status
      online: 'Online',
      offline: 'Offline',
      busy: 'Ocupado',
      available: 'Disponível',
      'in-use': 'Em Uso',
      maintenance: 'Manutenção',
      confirmed: 'Confirmado',
      pending: 'Pendente',
      cancelled: 'Cancelado',
      completed: 'Concluído',
      
      // Phases
      'Pre-Production': 'Pré-Produção',
      'Production': 'Produção',
      'Post-Production': 'Pós-Produção',
      'Distribution': 'Distribuição'
    },
    
    'en-US': {
      // Sistema
      appName: 'CineProd Ultimate',
      tagline: 'Complete Film Production Management System',
      welcome: 'Welcome',
      loading: 'Loading...',
      save: 'Save',
      cancel: 'Cancel',
      delete: 'Delete',
      edit: 'Edit',
      add: 'Add',
      search: 'Search',
      filter: 'Filter',
      export: 'Export',
      import: 'Import',
      print: 'Print',
      share: 'Share',
      download: 'Download',
      upload: 'Upload',
      
      // Auth
      login: 'Login',
      logout: 'Logout',
      email: 'Email',
      password: 'Password',
      rememberMe: 'Remember me',
      forgotPassword: 'Forgot password',
      selectProfile: 'Select a profile for quick access',
      invalidCredentials: 'Invalid email or password',
      
      // Menu items (English)
      dashboard: 'Dashboard',
      projects: 'Projects',
      schedule: 'Schedule',
      crew: 'Crew',
      equipment: 'Equipment',
      locations: 'Locations',
      documents: 'Documents',
      budget: 'Budget',
      callSheets: 'Call Sheets',
      scripts: 'Scripts',
      shotList: 'Shot List',
      storyboard: 'Storyboard',
      reports: 'Reports',
      contacts: 'Contacts',
      calendar: 'Calendar',
      weather: 'Weather',
      chat: 'Chat',
      settings: 'Settings',
      help: 'Help'
    }
  };

  const t = (key) => translations[language][key] || key;

  // ==================== FUNÇÕES UTILITÁRIAS ====================
  const formatCurrency = (value) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  };

  const formatDate = (date) => {
    return new Date(date).toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
  };

  const formatTime = (time) => {
    return time; // Already in HH:MM format
  };

  const calculateProgress = (completed, total) => {
    return Math.round((completed / total) * 100);
  };

  const getStatusColor = (status) => {
    const colors = {
      'online': '#10b981',
      'offline': '#6b7280',
      'busy': '#f59e0b',
      'available': '#10b981',
      'in-use': '#f59e0b',
      'maintenance': '#ef4444',
      'confirmed': '#10b981',
      'pending': '#f59e0b',
      'cancelled': '#ef4444',
      'completed': '#3b82f6'
    };
    return colors[status] || '#6b7280';
  };

  // ==================== HOOKS PERSONALIZADOS ====================
  useEffect(() => {
    // Verificar sessão salva
    const savedSession = localStorage.getItem('cinepro_session');
    if (savedSession) {
      try {
        const session = JSON.parse(savedSession);
        if (session.user && session.timestamp) {
          const hoursSinceLogin = (Date.now() - session.timestamp) / (1000 * 60 * 60);
          if (hoursSinceLogin < 24) {
            setCurrentUser(session.user);
            setIsAuthenticated(true);
            setProjects(database.projects);
            setCurrentProject(database.projects[0]);
          } else {
            localStorage.removeItem('cinepro_session');
          }
        }
      } catch (error) {
        console.error('Session recovery error:', error);
        localStorage.removeItem('cinepro_session');
      }
    }
    
    // Carregar dados iniciais
    setNotifications([
      { id: 1, message: 'Nova call sheet disponível para amanhã', time: 'Há 5 minutos', type: 'info' },
      { id: 2, message: 'Orçamento do Projeto Eclipse atualizado', time: 'Há 1 hora', type: 'warning' },
      { id: 3, message: 'Equipamento devolvido com sucesso', time: 'Há 2 horas', type: 'success' }
    ]);
    
    setActivities([
      { id: 1, user: 'Sofia Luz', action: 'atualizou o cronograma', project: 'Eclipse', time: '10:30' },
      { id: 2, user: 'Marcus Terra', action: 'aprovou o orçamento', project: 'Urban Shadows', time: '09:45' },
      { id: 3, user: 'Luna Sombra', action: 'adicionou novas fotos', project: 'Eclipse', time: '08:20' }
    ]);
  }, []);

  // ==================== COMPONENTE DE LOGIN ====================
  const LoginScreen = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [rememberMe, setRememberMe] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');
    const [showPassword, setShowPassword] = useState(false);

    const handleLogin = (e) => {
      e?.preventDefault();
      setIsLoading(true);
      setError('');

      setTimeout(() => {
        const user = database.users.find(u => u.email === email && u.password === password);
        
        if (user) {
          setCurrentUser(user);
          setIsAuthenticated(true);
          setProjects(database.projects);
          setCurrentProject(database.projects[0]);
          
          if (rememberMe) {
            localStorage.setItem('cinepro_session', JSON.stringify({
              user,
              timestamp: Date.now()
            }));
          }
          
          setNotifications(prev => [{
            id: Date.now(),
            message: `Bem-vindo de volta, ${user.name}!`,
            time: 'Agora',
            type: 'success'
          }, ...prev]);
        } else {
          setError(t('invalidCredentials'));
        }
        
        setIsLoading(false);
      }, 500);
    };

    const quickLogin = (userEmail) => {
      const user = database.users.find(u => u.email === userEmail);
      if (user) {
        setEmail(user.email);
        setPassword(user.password);
      }
    };

    return (
      <div style={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        padding: '20px'
      }}>
        <div style={{
          background: 'white',
          borderRadius: '20px',
          padding: '40px',
          width: '100%',
          maxWidth: '480px',
          boxShadow: '0 20px 60px rgba(0,0,0,0.3)'
        }}>
          {/* Logo */}
          <div style={{ textAlign: 'center', marginBottom: '30px' }}>
            <div style={{
              width: '80px',
              height: '80px',
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              borderRadius: '20px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              margin: '0 auto 20px',
              boxShadow: '0 10px 30px rgba(102, 126, 234, 0.4)'
            }}>
              <Film size={40} color="white" />
            </div>
            <h1 style={{ fontSize: '28px', fontWeight: 'bold', color: '#1a202c', margin: '0 0 8px' }}>
              {t('appName')}
            </h1>
            <p style={{ color: '#718096', fontSize: '14px' }}>{t('tagline')}</p>
          </div>

          {/* Quick Access */}
          <div style={{ marginBottom: '25px' }}>
            <p style={{ fontSize: '13px', color: '#718096', marginBottom: '12px', textAlign: 'center' }}>
              {t('selectProfile')}
            </p>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '10px' }}>
              {database.users.slice(0, 4).map(user => (
                <button
                  key={user.id}
                  onClick={() => quickLogin(user.email)}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    padding: '12px',
                    border: '1px solid #e2e8f0',
                    borderRadius: '10px',
                    background: 'white',
                    cursor: 'pointer',
                    transition: 'all 0.2s',
                    ':hover': {
                      borderColor: '#667eea',
                      transform: 'translateY(-2px)',
                      boxShadow: '0 4px 12px rgba(0,0,0,0.1)'
                    }
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.borderColor = '#667eea';
                    e.currentTarget.style.transform = 'translateY(-2px)';
                    e.currentTarget.style.boxShadow = '0 4px 12px rgba(0,0,0,0.1)';
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.borderColor = '#e2e8f0';
                    e.currentTarget.style.transform = 'translateY(0)';
                    e.currentTarget.style.boxShadow = 'none';
                  }}
                >
                  <div style={{
                    width: '36px',
                    height: '36px',
                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                    borderRadius: '50%',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'white',
                    fontSize: '14px',
                    fontWeight: 'bold',
                    marginRight: '10px',
                    flexShrink: 0
                  }}>
                    {user.avatar}
                  </div>
                  <div style={{ textAlign: 'left', overflow: 'hidden' }}>
                    <div style={{ fontSize: '13px', fontWeight: '600', color: '#2d3748', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                      {user.name.split(' ')[0]}
                    </div>
                    <div style={{ fontSize: '11px', color: '#718096', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                      {user.role}
                    </div>
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Divider */}
          <div style={{ position: 'relative', margin: '25px 0' }}>
            <div style={{ position: 'absolute', inset: '0', display: 'flex', alignItems: 'center' }}>
              <div style={{ width: '100%', borderTop: '1px solid #e2e8f0' }}></div>
            </div>
            <div style={{ position: 'relative', display: 'flex', justifyContent: 'center' }}>
              <span style={{ padding: '0 10px', background: 'white', fontSize: '12px', color: '#a0aec0' }}>
                ou entre com suas credenciais
              </span>
            </div>
          </div>

          {/* Login Form */}
          <form onSubmit={handleLogin}>
            {error && (
              <div style={{
                padding: '10px',
                background: '#fed7d7',
                border: '1px solid #fc8181',
                borderRadius: '8px',
                color: '#742a2a',
                fontSize: '13px',
                marginBottom: '15px',
                display: 'flex',
                alignItems: 'center'
              }}>
                <AlertCircle size={16} style={{ marginRight: '8px' }} />
                {error}
              </div>
            )}

            <div style={{ marginBottom: '15px' }}>
              <label style={{ display: 'block', fontSize: '13px', fontWeight: '500', color: '#4a5568', marginBottom: '5px' }}>
                {t('email')}
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                style={{
                  width: '100%',
                  padding: '10px 12px',
                  border: '1px solid #e2e8f0',
                  borderRadius: '8px',
                  fontSize: '14px',
                  transition: 'all 0.2s',
                  outline: 'none'
                }}
                placeholder="seu@email.com"
                onFocus={(e) => e.target.style.borderColor = '#667eea'}
                onBlur={(e) => e.target.style.borderColor = '#e2e8f0'}
              />
            </div>

            <div style={{ marginBottom: '15px' }}>
              <label style={{ display: 'block', fontSize: '13px', fontWeight: '500', color: '#4a5568', marginBottom: '5px' }}>
                {t('password')}
              </label>
              <div style={{ position: 'relative' }}>
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  style={{
                    width: '100%',
                    padding: '10px 40px 10px 12px',
                    border: '1px solid #e2e8f0',
                    borderRadius: '8px',
                    fontSize: '14px',
                    transition: 'all 0.2s',
                    outline: 'none'
                  }}
                  placeholder="••••••••"
                  onFocus={(e) => e.target.style.borderColor = '#667eea'}
                  onBlur={(e) => e.target.style.borderColor = '#e2e8f0'}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  style={{
                    position: 'absolute',
                    right: '12px',
                    top: '50%',
                    transform: 'translateY(-50%)',
                    background: 'none',
                    border: 'none',
                    cursor: 'pointer',
                    color: '#718096'
                  }}
                >
                  {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                </button>
              </div>
            </div>

            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
              <label style={{ display: 'flex', alignItems: 'center', cursor: 'pointer', fontSize: '13px', color: '#4a5568' }}>
                <input
                  type="checkbox"
                  checked={rememberMe}
                  onChange={(e) => setRememberMe(e.target.checked)}
                  style={{ marginRight: '6px' }}
                />
                {t('rememberMe')}
              </label>
              <button type="button" style={{
                background: 'none',
                border: 'none',
                color: '#667eea',
                fontSize: '13px',
                cursor: 'pointer',
                textDecoration: 'underline'
              }}>
                {t('forgotPassword')}?
              </button>
            </div>

            <button
              type="submit"
              disabled={isLoading}
              style={{
                width: '100%',
                padding: '12px',
                background: isLoading ? '#cbd5e0' : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                color: 'white',
                border: 'none',
                borderRadius: '8px',
                fontSize: '14px',
                fontWeight: '600',
                cursor: isLoading ? 'not-allowed' : 'pointer',
                transition: 'all 0.2s',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '8px'
              }}
            >
              {isLoading && <Loader size={16} className="animate-spin" />}
              {isLoading ? t('loading') : t('login')}
            </button>
          </form>

          {/* Demo Info */}
          <div style={{
            marginTop: '20px',
            padding: '12px',
            background: '#f7fafc',
            borderRadius: '8px',
            fontSize: '12px',
            color: '#718096',
            textAlign: 'center'
          }}>
            <strong>Demo:</strong> Use qualquer email acima com senha <code style={{ 
              background: '#edf2f7', 
              padding: '2px 4px', 
              borderRadius: '4px',
              color: '#2d3748'
            }}>demo123</code>
          </div>
        </div>
      </div>
    );
  };

  // ==================== SIDEBAR ====================
  const Sidebar = () => {
    const menuItems = [
      { id: 'dashboard', label: t('dashboard'), icon: Home, badge: null },
      { id: 'projects', label: t('projects'), icon: Film, badge: projects.length },
      { id: 'schedule', label: t('schedule'), icon: Calendar, badge: null },
      { id: 'callSheets', label: t('callSheets'), icon: Clipboard, badge: 3 },
      { id: 'crew', label: t('crew'), icon: Users, badge: null },
      { id: 'equipment', label: t('equipment'), icon: Camera, badge: null },
      { id: 'locations', label: t('locations'), icon: MapPin, badge: null },
      { id: 'scripts', label: t('scripts'), icon: FileText, badge: null },
      { id: 'shotList', label: t('shotList'), icon: List, badge: null },
      { id: 'storyboard', label: t('storyboard'), icon: Image, badge: null },
      { id: 'budget', label: t('budget'), icon: DollarSign, badge: null },
      { id: 'documents', label: t('documents'), icon: FolderOpen, badge: 12 },
      { id: 'contacts', label: t('contacts'), icon: Phone, badge: null },
      { id: 'weather', label: t('weather'), icon: Cloud, badge: null },
      { id: 'chat', label: t('chat'), icon: MessageCircle, badge: 5 },
      { id: 'reports', label: t('reports'), icon: FileBarChart, badge: null },
      { id: 'settings', label: t('settings'), icon: Settings, badge: null }
    ];

    return (
      <div style={{
        position: 'fixed',
        left: 0,
        top: 0,
        height: '100vh',
        width: sidebarOpen ? '260px' : '70px',
        background: '#1a202c',
        borderRight: '1px solid #2d3748',
        transition: 'width 0.3s ease',
        zIndex: 1000,
        overflowY: 'auto',
        overflowX: 'hidden'
      }}>
        {/* Logo */}
        <div style={{
          padding: '20px',
          borderBottom: '1px solid #2d3748',
          display: 'flex',
          alignItems: 'center',
          justifyContent: sidebarOpen ? 'space-between' : 'center'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div style={{
              width: '40px',
              height: '40px',
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              borderRadius: '10px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              flexShrink: 0
            }}>
              <Film size={24} color="white" />
            </div>
            {sidebarOpen && (
              <span style={{ color: 'white', fontSize: '18px', fontWeight: 'bold', whiteSpace: 'nowrap' }}>
                CineProd
              </span>
            )}
          </div>
          {sidebarOpen && (
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              style={{
                background: 'none',
                border: 'none',
                color: '#a0aec0',
                cursor: 'pointer',
                padding: '4px'
              }}
            >
              <ChevronLeft size={20} />
            </button>
          )}
        </div>

        {/* Menu Items */}
        <nav style={{ padding: '10px' }}>
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeModule === item.id;
            
            return (
              <button
                key={item.id}
                onClick={() => setActiveModule(item.id)}
                style={{
                  width: '100%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: sidebarOpen ? 'space-between' : 'center',
                  padding: sidebarOpen ? '12px 16px' : '12px',
                  marginBottom: '4px',
                  background: isActive ? 'rgba(102, 126, 234, 0.1)' : 'transparent',
                  border: 'none',
                  borderRadius: '8px',
                  color: isActive ? '#667eea' : '#a0aec0',
                  cursor: 'pointer',
                  transition: 'all 0.2s',
                  position: 'relative'
                }}
                onMouseEnter={(e) => {
                  if (!isActive) {
                    e.currentTarget.style.background = 'rgba(255, 255, 255, 0.05)';
                    e.currentTarget.style.color = '#e2e8f0';
                  }
                }}
                onMouseLeave={(e) => {
                  if (!isActive) {
                    e.currentTarget.style.background = 'transparent';
                    e.currentTarget.style.color = '#a0aec0';
                  }
                }}
                title={!sidebarOpen ? item.label : ''}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                  <Icon size={20} />
                  {sidebarOpen && (
                    <span style={{ fontSize: '14px', fontWeight: '500', whiteSpace: 'nowrap' }}>
                      {item.label}
                    </span>
                  )}
                </div>
                {sidebarOpen && item.badge && (
                  <span style={{
                    background: isActive ? '#667eea' : '#4a5568',
                    color: 'white',
                    fontSize: '11px',
                    padding: '2px 6px',
                    borderRadius: '10px',
                    fontWeight: 'bold'
                  }}>
                    {item.badge}
                  </span>
                )}
              </button>
            );
          })}
        </nav>

        {/* Toggle Button (when closed) */}
        {!sidebarOpen && (
          <button
            onClick={() => setSidebarOpen(true)}
            style={{
              position: 'absolute',
              bottom: '20px',
              left: '50%',
              transform: 'translateX(-50%)',
              background: 'rgba(255, 255, 255, 0.1)',
              border: 'none',
              borderRadius: '8px',
              padding: '8px',
              color: '#a0aec0',
              cursor: 'pointer'
            }}
          >
            <ChevronRight size={20} />
          </button>
        )}
      </div>
    );
  };

  // ==================== HEADER ====================
  const Header = () => {
    return (
      <header style={{
        position: 'fixed',
        top: 0,
        left: sidebarOpen ? '260px' : '70px',
        right: 0,
        height: '70px',
        background: 'white',
        borderBottom: '1px solid #e2e8f0',
        padding: '0 24px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        transition: 'left 0.3s ease',
        zIndex: 999
      }}>
        {/* Search Bar */}
        <div style={{ flex: 1, maxWidth: '500px' }}>
          <div style={{ position: 'relative' }}>
            <Search size={20} style={{
              position: 'absolute',
              left: '12px',
              top: '50%',
              transform: 'translateY(-50%)',
              color: '#a0aec0'
            }} />
            <input
              type="text"
              placeholder="Buscar projetos, pessoas, documentos..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              style={{
                width: '100%',
                padding: '10px 12px 10px 40px',
                background: '#f7fafc',
                border: '1px solid #e2e8f0',
                borderRadius: '8px',
                fontSize: '14px',
                outline: 'none',
                transition: 'all 0.2s'
              }}
              onFocus={(e) => {
                e.target.style.background = 'white';
                e.target.style.borderColor = '#667eea';
              }}
              onBlur={(e) => {
                e.target.style.background = '#f7fafc';
                e.target.style.borderColor = '#e2e8f0';
              }}
            />
          </div>
        </div>

        {/* Actions */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          {/* Weather Widget */}
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            padding: '8px 12px',
            background: '#f7fafc',
            borderRadius: '8px',
            fontSize: '13px',
            color: '#4a5568'
          }}>
            <Sun size={16} />
            <span>São Paulo • 25°C</span>
          </div>

          {/* Notifications */}
          <div style={{ position: 'relative' }}>
            <button
              onClick={() => setShowNotifications(!showNotifications)}
              style={{
                position: 'relative',
                background: '#f7fafc',
                border: 'none',
                borderRadius: '8px',
                padding: '10px',
                cursor: 'pointer',
                color: '#4a5568',
                transition: 'all 0.2s'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.background = '#e2e8f0';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = '#f7fafc';
              }}
            >
              <Bell size={20} />
              {notifications.length > 0 && (
                <span style={{
                  position: 'absolute',
                  top: '8px',
                  right: '8px',
                  width: '8px',
                  height: '8px',
                  background: '#f56565',
                  borderRadius: '50%'
                }}></span>
              )}
            </button>

            {/* Notifications Dropdown */}
            {showNotifications && (
              <div style={{
                position: 'absolute',
                top: 'calc(100% + 8px)',
                right: 0,
                width: '320px',
                background: 'white',
                borderRadius: '12px',
                boxShadow: '0 10px 40px rgba(0,0,0,0.15)',
                zIndex: 1000,
                overflow: 'hidden'
              }}>
                <div style={{
                  padding: '16px',
                  borderBottom: '1px solid #e2e8f0',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center'
                }}>
                  <h3 style={{ margin: 0, fontSize: '16px', fontWeight: '600', color: '#2d3748' }}>
                    Notificações
                  </h3>
                  <button style={{
                    background: 'none',
                    border: 'none',
                    color: '#667eea',
                    fontSize: '12px',
                    cursor: 'pointer'
                  }}>
                    Marcar todas como lidas
                  </button>
                </div>
                <div style={{ maxHeight: '300px', overflowY: 'auto' }}>
                  {notifications.map(notif => (
                    <div key={notif.id} style={{
                      padding: '12px 16px',
                      borderBottom: '1px solid #f7fafc',
                      cursor: 'pointer',
                      transition: 'background 0.2s'
                    }}
                    onMouseEnter={(e) => e.currentTarget.style.background = '#f7fafc'}
                    onMouseLeave={(e) => e.currentTarget.style.background = 'white'}
                    >
                      <p style={{ margin: '0 0 4px', fontSize: '13px', color: '#2d3748' }}>
                        {notif.message}
                      </p>
                      <span style={{ fontSize: '11px', color: '#a0aec0' }}>
                        {notif.time}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* User Menu */}
          <div style={{ position: 'relative' }}>
            <button
              onClick={() => setShowUserMenu(!showUserMenu)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '10px',
                background: 'none',
                border: 'none',
                cursor: 'pointer',
                padding: '8px'
              }}
            >
              <div style={{
                width: '36px',
                height: '36px',
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                borderRadius: '50%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: 'white',
                fontSize: '14px',
                fontWeight: 'bold'
              }}>
                {currentUser?.avatar}
              </div>
              <div style={{ textAlign: 'left' }}>
                <div style={{ fontSize: '13px', fontWeight: '600', color: '#2d3748' }}>
                  {currentUser?.name}
                </div>
                <div style={{ fontSize: '11px', color: '#718096' }}>
                  {currentUser?.role}
                </div>
              </div>
              <ChevronDown size={16} color="#718096" />
            </button>

            {/* User Dropdown */}
            {showUserMenu && (
              <div style={{
                position: 'absolute',
                top: 'calc(100% + 8px)',
                right: 0,
                width: '240px',
                background: 'white',
                borderRadius: '12px',
                boxShadow: '0 10px 40px rgba(0,0,0,0.15)',
                zIndex: 1000,
                overflow: 'hidden'
              }}>
                <div style={{ padding: '8px' }}>
                  <button style={{
                    width: '100%',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '12px',
                    padding: '10px 12px',
                    background: 'none',
                    border: 'none',
                    borderRadius: '8px',
                    color: '#4a5568',
                    cursor: 'pointer',
                    transition: 'background 0.2s',
                    fontSize: '13px',
                    textAlign: 'left'
                  }}
                  onMouseEnter={(e) => e.currentTarget.style.background = '#f7fafc'}
                  onMouseLeave={(e) => e.currentTarget.style.background = 'none'}
                  >
                    <User size={18} />
                    Meu Perfil
                  </button>
                  <button style={{
                    width: '100%',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '12px',
                    padding: '10px 12px',
                    background: 'none',
                    border: 'none',
                    borderRadius: '8px',
                    color: '#4a5568',
                    cursor: 'pointer',
                    transition: 'background 0.2s',
                    fontSize: '13px',
                    textAlign: 'left'
                  }}
                  onMouseEnter={(e) => e.currentTarget.style.background = '#f7fafc'}
                  onMouseLeave={(e) => e.currentTarget.style.background = 'none'}
                  >
                    <Settings size={18} />
                    Configurações
                  </button>
                  <button style={{
                    width: '100%',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '12px',
                    padding: '10px 12px',
                    background: 'none',
                    border: 'none',
                    borderRadius: '8px',
                    color: '#4a5568',
                    cursor: 'pointer',
                    transition: 'background 0.2s',
                    fontSize: '13px',
                    textAlign: 'left'
                  }}
                  onMouseEnter={(e) => e.currentTarget.style.background = '#f7fafc'}
                  onMouseLeave={(e) => e.currentTarget.style.background = 'none'}
                  >
                    <HelpCircle size={18} />
                    Ajuda
                  </button>
                  <div style={{ borderTop: '1px solid #e2e8f0', margin: '8px 0' }}></div>
                  <button 
                    onClick={() => {
                      setIsAuthenticated(false);
                      setCurrentUser(null);
                      localStorage.removeItem('cinepro_session');
                      setShowUserMenu(false);
                    }}
                    style={{
                      width: '100%',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '12px',
                      padding: '10px 12px',
                      background: 'none',
                      border: 'none',
                      borderRadius: '8px',
                      color: '#f56565',
                      cursor: 'pointer',
                      transition: 'background 0.2s',
                      fontSize: '13px',
                      textAlign: 'left'
                    }}
                    onMouseEnter={(e) => e.currentTarget.style.background = '#fed7e2'}
                    onMouseLeave={(e) => e.currentTarget.style.background = 'none'}
                  >
                    <LogOut size={18} />
                    Sair
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </header>
    );
  };

  // ==================== DASHBOARD ====================
  const Dashboard = () => {
    const stats = [
      { label: t('activeProjects'), value: projects.length, icon: Film, color: '#667eea', trend: '+12%' },
      { label: t('totalCrew'), value: 156, icon: Users, color: '#48bb78', trend: '+8%' },
      { label: t('totalBudget'), value: formatCurrency(15500000), icon: DollarSign, color: '#f6ad55', trend: '-3%' },
      { label: t('shootingDays'), value: 195, icon: Calendar, color: '#ed64a6', trend: '+15%' }
    ];

    return (
      <div style={{ padding: '24px' }}>
        <div style={{ marginBottom: '24px' }}>
          <h1 style={{ fontSize: '28px', fontWeight: 'bold', color: '#2d3748', margin: '0 0 8px' }}>
            {t('dashboard')}
          </h1>
          <p style={{ color: '#718096', fontSize: '14px' }}>
            {t('welcome')}, {currentUser?.name}! Aqui está sua visão geral.
          </p>
        </div>

        {/* Stats Grid */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
          gap: '20px',
          marginBottom: '32px'
        }}>
          {stats.map((stat, index) => {
            const Icon = stat.icon;
            return (
              <div key={index} style={{
                background: 'white',
                borderRadius: '12px',
                padding: '20px',
                boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
                transition: 'all 0.3s',
                cursor: 'pointer',
                position: 'relative',
                overflow: 'hidden'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'translateY(-4px)';
                e.currentTarget.style.boxShadow = '0 10px 30px rgba(0,0,0,0.15)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'translateY(0)';
                e.currentTarget.style.boxShadow = '0 1px 3px rgba(0,0,0,0.1)';
              }}
              >
                <div style={{
                  position: 'absolute',
                  top: 0,
                  right: 0,
                  width: '100px',
                  height: '100px',
                  background: stat.color,
                  opacity: 0.1,
                  borderRadius: '50%',
                  transform: 'translate(30px, -30px)'
                }}></div>
                
                <div style={{ position: 'relative', zIndex: 1 }}>
                  <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between' }}>
                    <div>
                      <p style={{ fontSize: '12px', color: '#718096', marginBottom: '4px' }}>
                        {stat.label}
                      </p>
                      <p style={{ fontSize: '24px', fontWeight: 'bold', color: '#2d3748' }}>
                        {stat.value}
                      </p>
                      <span style={{
                        fontSize: '12px',
                        color: stat.trend.startsWith('+') ? '#48bb78' : '#f56565',
                        fontWeight: '600'
                      }}>
                        {stat.trend} vs último mês
                      </span>
                    </div>
                    <div style={{
                      width: '48px',
                      height: '48px',
                      background: `${stat.color}15`,
                      borderRadius: '12px',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center'
                    }}>
                      <Icon size={24} color={stat.color} />
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* Projects and Activities */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: '1fr 400px',
          gap: '20px'
        }}>
          {/* Recent Projects */}
          <div style={{
            background: 'white',
            borderRadius: '12px',
            padding: '20px',
            boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
          }}>
            <div style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              marginBottom: '16px'
            }}>
              <h2 style={{ fontSize: '18px', fontWeight: '600', color: '#2d3748' }}>
                Projetos Recentes
              </h2>
              <button style={{
                background: 'none',
                border: 'none',
                color: '#667eea',
                fontSize: '13px',
                cursor: 'pointer'
              }}>
                Ver todos
              </button>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {projects.map(project => (
                <div key={project.id} style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: '16px',
                  background: '#f7fafc',
                  borderRadius: '8px',
                  cursor: 'pointer',
                  transition: 'all 0.2s'
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.background = '#edf2f7';
                  e.currentTarget.style.transform = 'translateX(4px)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.background = '#f7fafc';
                  e.currentTarget.style.transform = 'translateX(0)';
                }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <div style={{
                      width: '10px',
                      height: '10px',
                      borderRadius: '50%',
                      background: getStatusColor(project.status.toLowerCase())
                    }}></div>
                    <div>
                      <h3 style={{ fontSize: '14px', fontWeight: '600', color: '#2d3748', margin: 0 }}>
                        {project.title}
                      </h3>
                      <p style={{ fontSize: '12px', color: '#718096', margin: '2px 0 0' }}>
                        {project.type} • {project.director}
                      </p>
                    </div>
                  </div>
                  <div style={{ textAlign: 'right' }}>
                    <p style={{ fontSize: '14px', fontWeight: '600', color: '#2d3748', margin: 0 }}>
                      {calculateProgress(project.completedDays, project.shootingDays)}%
                    </p>
                    <p style={{ fontSize: '11px', color: '#718096', margin: '2px 0 0' }}>
                      {project.completedDays}/{project.shootingDays} dias
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Recent Activities */}
          <div style={{
            background: 'white',
            borderRadius: '12px',
            padding: '20px',
            boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
          }}>
            <h2 style={{ fontSize: '18px', fontWeight: '600', color: '#2d3748', marginBottom: '16px' }}>
              Atividades Recentes
            </h2>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              {activities.map(activity => (
                <div key={activity.id} style={{
                  display: 'flex',
                  gap: '12px'
                }}>
                  <div style={{
                    width: '8px',
                    height: '8px',
                    borderRadius: '50%',
                    background: '#667eea',
                    marginTop: '6px',
                    flexShrink: 0
                  }}></div>
                  <div style={{ flex: 1 }}>
                    <p style={{ fontSize: '13px', color: '#2d3748', margin: 0 }}>
                      <strong>{activity.user}</strong> {activity.action} em <strong>{activity.project}</strong>
                    </p>
                    <p style={{ fontSize: '11px', color: '#a0aec0', marginTop: '2px' }}>
                      {activity.time}
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

  // ==================== RENDER PRINCIPAL ====================
  if (!isAuthenticated) {
    return <LoginScreen />;
  }

  return (
    <div style={{
      minHeight: '100vh',
      background: '#f7fafc',
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    }}>
      <Sidebar />
      <Header />
      
      <main style={{
        marginLeft: sidebarOpen ? '260px' : '70px',
        marginTop: '70px',
        transition: 'margin-left 0.3s ease',
        minHeight: 'calc(100vh - 70px)'
      }}>
        {activeModule === 'dashboard' && <Dashboard />}
        
        {/* Outros módulos podem ser adicionados aqui */}
        {activeModule !== 'dashboard' && (
          <div style={{ padding: '24px' }}>
            <div style={{
              background: 'white',
              borderRadius: '12px',
              padding: '32px',
              boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
              textAlign: 'center'
            }}>
              <h2 style={{ fontSize: '24px', fontWeight: 'bold', color: '#2d3748', marginBottom: '12px' }}>
                Módulo: {activeModule.charAt(0).toUpperCase() + activeModule.slice(1)}
              </h2>
              <p style={{ color: '#718096', fontSize: '14px' }}>
                Este módulo está em desenvolvimento e em breve estará disponível com funcionalidades completas.
              </p>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default CineProUltimate;