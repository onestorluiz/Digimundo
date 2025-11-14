# 💻 CINEPROD - GUIA TÉCNICO DE IMPLEMENTAÇÃO
## Arquitetura, Código e Best Practices

**Data:** 27/10/2025  
**Público:** Time de desenvolvimento

---

## 📋 ÍNDICE

1. [Arquitetura do Sistema](#arquitetura)
2. [Stack Detalhado](#stack)
3. [Estrutura de Pastas](#estrutura)
4. [Exemplos de Código](#codigo)
5. [Database Schema](#database)
6. [APIs e Integrações](#apis)
7. [Performance & Scalability](#performance)
8. [Security Best Practices](#security)
9. [Testing Strategy](#testing)
10. [DevOps & Deployment](#devops)

---

## 🏗️ ARQUITETURA DO SISTEMA {#arquitetura}

### Visão Geral (High-Level)

```
┌─────────────────────────────────────────────────────────────────┐
│                         USUÁRIOS                                 │
│                  (Web Browser / Mobile)                          │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ HTTPS
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      CLOUDFLARE                                  │
│                  (CDN + DDoS Protection)                         │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND (React)                              │
│   ┌──────────────────────────────────────────────────────┐     │
│   │  • Next.js ou Vite + React                           │     │
│   │  • State: Zustand                                    │     │
│   │  • UI: Tailwind + shadcn/ui                          │     │
│   │  • Real-time: Socket.io client                       │     │
│   └──────────────────────────────────────────────────────┘     │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ REST API + WebSockets
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI)                             │
│   ┌──────────────────────────────────────────────────────┐     │
│   │  • FastAPI (Python 3.11+)                            │     │
│   │  • Auth: JWT + OAuth2                                │     │
│   │  • Real-time: Socket.io server                       │     │
│   │  • Tasks: Celery + Redis                             │     │
│   │  • Cache: Redis                                      │     │
│   └──────────────────────────────────────────────────────┘     │
└───────┬──────────────────────────┬────────────────┬─────────────┘
        │                          │                │
        │                          │                │
        ▼                          ▼                ▼
┌──────────────┐      ┌──────────────────┐  ┌──────────────┐
│  PostgreSQL  │      │   Redis Cache    │  │  File Store  │
│   Database   │      │   + Queue        │  │  (S3/R2)     │
└──────────────┘      └──────────────────┘  └──────────────┘
        │                                            │
        │                                            │
        ▼                                            ▼
┌──────────────┐                           ┌──────────────┐
│  Backup      │                           │  CDN         │
│  (Daily)     │                           │  (Assets)    │
└──────────────┘                           └──────────────┘

EXTERNAL SERVICES:
├─ SendGrid (Email)
├─ Twilio (SMS)
├─ OpenWeather API
├─ Google Maps API
├─ Stripe (Payments)
└─ Sentry (Monitoring)
```

---

## 🔧 STACK DETALHADO {#stack}

### Frontend Stack

```javascript
// package.json (Frontend)
{
  "name": "cineprod-frontend",
  "version": "1.0.0",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext .ts,.tsx",
    "test": "vitest"
  },
  "dependencies": {
    // Core
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    
    // State Management
    "zustand": "^4.4.7",
    "@tanstack/react-query": "^5.14.0",
    
    // UI Components
    "@radix-ui/react-*": "^1.0.0", // All Radix primitives
    "tailwindcss": "^3.3.6",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.0.0",
    
    // Forms & Validation
    "react-hook-form": "^7.49.2",
    "zod": "^3.22.4",
    "@hookform/resolvers": "^3.3.2",
    
    // Rich Text Editor
    "lexical": "^0.12.5", // ou Draft.js
    "lexical-react": "^0.12.5",
    
    // Drag & Drop
    "@dnd-kit/core": "^6.1.0",
    "@dnd-kit/sortable": "^8.0.0",
    
    // Real-time
    "socket.io-client": "^4.5.4",
    
    // Utilities
    "date-fns": "^2.30.0",
    "axios": "^1.6.2",
    "react-hot-toast": "^2.4.1",
    
    // PDF Generation
    "@react-pdf/renderer": "^3.1.14",
    
    // Charts
    "recharts": "^2.10.3"
  },
  "devDependencies": {
    "@types/react": "^18.2.43",
    "@types/react-dom": "^18.2.17",
    "@vitejs/plugin-react": "^4.2.1",
    "vite": "^5.0.7",
    "typescript": "^5.3.3",
    "eslint": "^8.55.0",
    "prettier": "^3.1.1",
    "vitest": "^1.0.4",
    "@testing-library/react": "^14.1.2"
  }
}
```

### Backend Stack

```python
# requirements.txt (Backend)

# Core Framework
fastapi==0.109.0
uvicorn[standard]==0.25.0
python-multipart==0.0.6

# Database
sqlalchemy==2.0.25
alembic==1.13.1
psycopg2-binary==2.9.9
asyncpg==0.29.0

# Cache & Queue
redis==5.0.1
celery==5.3.4

# Auth & Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0

# Real-time
python-socketio==5.10.0

# Validation
pydantic==2.5.3
pydantic-settings==2.1.0

# Email
sendgrid==6.11.0

# PDF Generation
reportlab==4.0.7
weasyprint==60.1

# File Upload
python-magic==0.4.27

# External APIs
httpx==0.26.0
requests==2.31.0

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0

# Monitoring
sentry-sdk==1.39.1

# Development
black==23.12.1
flake8==7.0.0
mypy==1.7.1
```

---

## 📁 ESTRUTURA DE PASTAS {#estrutura}

### Frontend Structure

```
cineprod-frontend/
├── public/
│   ├── favicon.ico
│   └── assets/
├── src/
│   ├── components/
│   │   ├── ui/                    # shadcn components
│   │   │   ├── button.tsx
│   │   │   ├── input.tsx
│   │   │   └── ...
│   │   ├── layout/                # Layout components
│   │   │   ├── Header.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   └── MainLayout.tsx
│   │   ├── script/                # Script editor components
│   │   │   ├── ScriptEditor.tsx
│   │   │   ├── ScriptToolbar.tsx
│   │   │   └── ScriptFormatting.tsx
│   │   ├── breakdown/             # Breakdown components
│   │   │   ├── BreakdownView.tsx
│   │   │   ├── ElementTag.tsx
│   │   │   └── ElementsManager.tsx
│   │   ├── stripboard/            # Stripboard components
│   │   │   ├── StripboardView.tsx
│   │   │   ├── SceneStrip.tsx
│   │   │   └── StripboardControls.tsx
│   │   └── callsheet/             # Call sheet components
│   │       ├── CallSheetBuilder.tsx
│   │       ├── CallSheetPreview.tsx
│   │       └── RecipientManager.tsx
│   ├── pages/
│   │   ├── Dashboard.tsx
│   │   ├── Projects.tsx
│   │   ├── Script.tsx
│   │   ├── Breakdown.tsx
│   │   ├── Stripboard.tsx
│   │   ├── CallSheets.tsx
│   │   └── Settings.tsx
│   ├── stores/                    # Zustand stores
│   │   ├── authStore.ts
│   │   ├── projectStore.ts
│   │   ├── scriptStore.ts
│   │   └── ...
│   ├── hooks/                     # Custom hooks
│   │   ├── useAuth.ts
│   │   ├── useScript.ts
│   │   ├── useRealtime.ts
│   │   └── ...
│   ├── services/                  # API services
│   │   ├── api.ts                 # Axios instance
│   │   ├── auth.service.ts
│   │   ├── project.service.ts
│   │   ├── script.service.ts
│   │   └── ...
│   ├── types/                     # TypeScript types
│   │   ├── index.ts
│   │   ├── script.types.ts
│   │   ├── project.types.ts
│   │   └── ...
│   ├── utils/                     # Utilities
│   │   ├── formatting.ts
│   │   ├── validation.ts
│   │   ├── dates.ts
│   │   └── ...
│   ├── lib/                       # Configuration
│   │   ├── socket.ts
│   │   └── constants.ts
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
├── .env.example
├── .eslintrc.js
├── .prettierrc
├── tsconfig.json
├── vite.config.ts
├── tailwind.config.js
└── package.json
```

### Backend Structure

```
cineprod-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app
│   ├── config.py                  # Configuration
│   ├── database.py                # Database connection
│   ├── dependencies.py            # FastAPI dependencies
│   ├── models/                    # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── project.py
│   │   ├── script.py
│   │   ├── breakdown.py
│   │   ├── callsheet.py
│   │   └── ...
│   ├── schemas/                   # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── project.py
│   │   ├── script.py
│   │   └── ...
│   ├── api/                       # API routes
│   │   ├── __init__.py
│   │   ├── deps.py                # Route dependencies
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py
│   │       ├── projects.py
│   │       ├── scripts.py
│   │       ├── breakdown.py
│   │       ├── callsheets.py
│   │       └── ...
│   ├── services/                  # Business logic
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── script_service.py
│   │   ├── pdf_service.py
│   │   ├── email_service.py
│   │   └── ...
│   ├── utils/                     # Utilities
│   │   ├── __init__.py
│   │   ├── security.py
│   │   ├── formatting.py
│   │   └── ...
│   ├── core/                      # Core functionality
│   │   ├── __init__.py
│   │   ├── security.py            # JWT, hashing
│   │   └── config.py              # Settings
│   ├── tasks/                     # Celery tasks
│   │   ├── __init__.py
│   │   ├── pdf_tasks.py
│   │   └── email_tasks.py
│   └── websockets/                # Socket.io handlers
│       ├── __init__.py
│       └── handlers.py
├── alembic/                       # Database migrations
│   ├── versions/
│   └── env.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_auth.py
│   └── ...
├── .env.example
├── .gitignore
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 💾 DATABASE SCHEMA {#database}

### Core Tables (PostgreSQL)

```sql
-- Users & Authentication
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    avatar_url VARCHAR(500),
    is_active BOOLEAN DEFAULT true,
    is_verified BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);

-- Workspaces (Multi-tenancy)
CREATE TABLE workspaces (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    owner_id UUID REFERENCES users(id) ON DELETE CASCADE,
    slug VARCHAR(100) UNIQUE NOT NULL,
    plan_tier VARCHAR(50) DEFAULT 'free',
    settings JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Workspace Members
CREATE TABLE workspace_members (
    workspace_id UUID REFERENCES workspaces(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(50) DEFAULT 'member',
    permissions JSONB DEFAULT '[]',
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (workspace_id, user_id)
);

-- Projects
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID REFERENCES workspaces(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    type VARCHAR(50), -- 'feature', 'short', 'commercial', 'doc'
    status VARCHAR(50) DEFAULT 'development',
    settings JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_projects_workspace ON projects(workspace_id);

-- Project Members
CREATE TABLE project_members (
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(50) DEFAULT 'member',
    permissions JSONB DEFAULT '[]',
    PRIMARY KEY (project_id, user_id)
);

-- Scripts
CREATE TABLE scripts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    version INTEGER DEFAULT 1,
    content JSONB NOT NULL, -- Lexical/Draft.js state
    content_text TEXT, -- Plain text for search
    is_current BOOLEAN DEFAULT true,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_scripts_project ON scripts(project_id);
CREATE INDEX idx_scripts_current ON scripts(project_id, is_current) WHERE is_current = true;

-- Scenes
CREATE TABLE scenes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    script_id UUID REFERENCES scripts(id) ON DELETE CASCADE,
    scene_number VARCHAR(20) NOT NULL,
    heading VARCHAR(500),
    int_ext VARCHAR(10), -- 'INT', 'EXT', 'INT/EXT'
    location VARCHAR(255),
    time_of_day VARCHAR(50), -- 'DAY', 'NIGHT', 'DAWN', etc
    page_count DECIMAL(4,2),
    content JSONB,
    notes TEXT,
    sort_order INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_scenes_script ON scenes(script_id);
CREATE INDEX idx_scenes_sort ON scenes(script_id, sort_order);

-- Elements (Breakdown)
CREATE TABLE elements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL, -- 'cast', 'props', 'wardrobe', etc
    name VARCHAR(255) NOT NULL,
    description TEXT,
    notes TEXT,
    images JSONB DEFAULT '[]',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_elements_project ON elements(project_id);
CREATE INDEX idx_elements_type ON elements(project_id, type);

-- Scene Elements (Many-to-Many)
CREATE TABLE scene_elements (
    scene_id UUID REFERENCES scenes(id) ON DELETE CASCADE,
    element_id UUID REFERENCES elements(id) ON DELETE CASCADE,
    quantity INTEGER DEFAULT 1,
    notes TEXT,
    PRIMARY KEY (scene_id, element_id)
);

-- Stripboard
CREATE TABLE stripboard_strips (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    scene_id UUID REFERENCES scenes(id) ON DELETE SET NULL,
    position INTEGER NOT NULL,
    color VARCHAR(20),
    shoot_day INTEGER,
    is_company_move BOOLEAN DEFAULT false,
    is_day_break BOOLEAN DEFAULT false,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_stripboard_project ON stripboard_strips(project_id);
CREATE INDEX idx_stripboard_position ON stripboard_strips(project_id, position);

-- Call Sheets
CREATE TABLE call_sheets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    shoot_date DATE NOT NULL,
    call_time TIME,
    general_notes TEXT,
    weather JSONB,
    status VARCHAR(50) DEFAULT 'draft',
    sent_at TIMESTAMP,
    scenes JSONB DEFAULT '[]',
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_callsheets_project ON call_sheets(project_id);
CREATE INDEX idx_callsheets_date ON call_sheets(project_id, shoot_date);

-- Contacts (CRM)
CREATE TABLE contacts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID REFERENCES workspaces(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(50),
    role VARCHAR(100),
    department VARCHAR(100),
    day_rate DECIMAL(10,2),
    notes TEXT,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_contacts_workspace ON contacts(workspace_id);
CREATE INDEX idx_contacts_email ON contacts(email);

-- Call Sheet Recipients
CREATE TABLE call_sheet_recipients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    call_sheet_id UUID REFERENCES call_sheets(id) ON DELETE CASCADE,
    contact_id UUID REFERENCES contacts(id) ON DELETE CASCADE,
    call_time TIME,
    private_notes TEXT,
    confirmed_at TIMESTAMP,
    viewed_at TIMESTAMP
);

-- Locations
CREATE TABLE locations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    address TEXT,
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    contact_info JSONB,
    cost_info JSONB,
    photos JSONB DEFAULT '[]',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Budget & Finance
CREATE TABLE budgets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    total_budget DECIMAL(12,2),
    departments JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE expenses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    budget_id UUID REFERENCES budgets(id) ON DELETE CASCADE,
    category VARCHAR(100),
    description TEXT,
    amount DECIMAL(10,2) NOT NULL,
    expense_date DATE,
    receipt_url VARCHAR(500),
    vendor VARCHAR(255),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Media Files
CREATE TABLE media_files (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    file_url VARCHAR(500) NOT NULL,
    file_type VARCHAR(50),
    file_size BIGINT,
    mime_type VARCHAR(100),
    uploaded_by UUID REFERENCES users(id),
    folder_path VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Collaboration
CREATE TABLE comments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_type VARCHAR(50) NOT NULL,
    entity_id UUID NOT NULL,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    mentions JSONB DEFAULT '[]',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_comments_entity ON comments(entity_type, entity_id);

-- Activity Log
CREATE TABLE activities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50),
    entity_id UUID,
    details JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_activities_project ON activities(project_id, created_at DESC);
```

---

## 🔌 EXEMPLOS DE CÓDIGO {#codigo}

### 1. Script Editor Component (React)

```typescript
// components/script/ScriptEditor.tsx
import React, { useCallback, useEffect } from 'react';
import { useLexicalComposerContext } from '@lexical/react/LexicalComposerContext';
import { $getRoot, $createParagraphNode, $createTextNode } from 'lexical';
import { useScriptStore } from '@/stores/scriptStore';
import { debounce } from '@/utils/debounce';

interface ScriptEditorProps {
  scriptId: string;
  projectId: string;
}

export function ScriptEditor({ scriptId, projectId }: ScriptEditorProps) {
  const [editor] = useLexicalComposerContext();
  const { updateScript, saveScript } = useScriptStore();

  // Auto-save debounced
  const debouncedSave = useCallback(
    debounce((content: any) => {
      saveScript(scriptId, content);
    }, 2000),
    [scriptId]
  );

  // Listen to editor changes
  useEffect(() => {
    return editor.registerUpdateListener(({ editorState }) => {
      editorState.read(() => {
        const json = editorState.toJSON();
        updateScript(scriptId, json);
        debouncedSave(json);
      });
    });
  }, [editor, scriptId]);

  // Script formatting shortcuts
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Tab') {
        event.preventDefault();
        // Insert 4 spaces or handle formatting
        editor.update(() => {
          const selection = $getSelection();
          if ($isRangeSelection(selection)) {
            selection.insertText('    ');
          }
        });
      }
    };

    editor.getRootElement()?.addEventListener('keydown', handleKeyDown);
    return () => {
      editor.getRootElement()?.removeEventListener('keydown', handleKeyDown);
    };
  }, [editor]);

  return (
    <div className="script-editor">
      {/* Editor interface aqui */}
    </div>
  );
}
```

### 2. Breakdown Select-and-Tag

```typescript
// components/breakdown/ElementTagger.tsx
import React, { useState } from 'react';
import { useSelection } from '@/hooks/useSelection';
import { ELEMENT_COLORS } from '@/lib/constants';

interface ElementTaggerProps {
  sceneId: string;
  onTagElement: (element: ElementTag) => void;
}

export function ElementTagger({ sceneId, onTagElement }: ElementTaggerProps) {
  const [showPopover, setShowPopover] = useState(false);
  const [popoverPosition, setPopoverPosition] = useState({ x: 0, y: 0 });
  const selectedText = useSelection();

  const handleSelection = () => {
    const selection = window.getSelection();
    if (!selection || selection.toString().trim() === '') return;

    const range = selection.getRangeAt(0);
    const rect = range.getBoundingClientRect();
    
    setPopoverPosition({
      x: rect.left + rect.width / 2,
      y: rect.top - 10
    });
    setShowPopover(true);
  };

  const handleTagElement = (type: string) => {
    const selection = window.getSelection();
    if (!selection) return;

    const selectedText = selection.toString();
    
    onTagElement({
      sceneId,
      type,
      name: selectedText,
      color: ELEMENT_COLORS[type]
    });

    // Highlight selected text with color
    const range = selection.getRangeAt(0);
    const span = document.createElement('span');
    span.style.backgroundColor = ELEMENT_COLORS[type];
    span.style.padding = '2px 4px';
    span.style.borderRadius = '3px';
    span.className = `element-tag element-tag-${type}`;
    span.textContent = selectedText;
    
    range.deleteContents();
    range.insertNode(span);
    
    setShowPopover(false);
  };

  return (
    <div onMouseUp={handleSelection}>
      {showPopover && (
        <div 
          className="element-popover"
          style={{
            position: 'fixed',
            left: popoverPosition.x,
            top: popoverPosition.y,
            transform: 'translateX(-50%) translateY(-100%)'
          }}
        >
          <button onClick={() => handleTagElement('cast')}>Cast</button>
          <button onClick={() => handleTagElement('props')}>Props</button>
          <button onClick={() => handleTagElement('wardrobe')}>Wardrobe</button>
          {/* More buttons... */}
        </div>
      )}
    </div>
  );
}
```

### 3. Backend API Example (FastAPI)

```python
# app/api/v1/scripts.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app import schemas, models
from app.api import deps
from app.services import script_service

router = APIRouter()

@router.post("/", response_model=schemas.Script)
async def create_script(
    project_id: UUID,
    script_in: schemas.ScriptCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """Create new script for project"""
    
    # Check if user has access to project
    project = db.query(models.Project).filter(
        models.Project.id == project_id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Check permissions
    if not deps.has_project_access(current_user, project, "write"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Create script
    script = script_service.create_script(
        db=db,
        project_id=project_id,
        script_data=script_in,
        user_id=current_user.id
    )
    
    return script

@router.get("/{script_id}", response_model=schemas.Script)
async def get_script(
    script_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """Get script by ID"""
    
    script = db.query(models.Script).filter(
        models.Script.id == script_id
    ).first()
    
    if not script:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Script not found"
        )
    
    # Check permissions
    if not deps.has_project_access(current_user, script.project, "read"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return script

@router.patch("/{script_id}", response_model=schemas.Script)
async def update_script(
    script_id: UUID,
    script_update: schemas.ScriptUpdate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """Update script content"""
    
    script = db.query(models.Script).filter(
        models.Script.id == script_id
    ).first()
    
    if not script:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Script not found"
        )
    
    # Check permissions
    if not deps.has_project_access(current_user, script.project, "write"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Update script
    updated_script = script_service.update_script(
        db=db,
        script=script,
        script_data=script_update,
        user_id=current_user.id
    )
    
    return updated_script

@router.post("/{script_id}/breakdown", response_model=schemas.Breakdown)
async def create_breakdown(
    script_id: UUID,
    scene_number: str,
    element_tags: List[schemas.ElementTagCreate],
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """Create breakdown tags for a scene"""
    
    # Implementation here...
    pass
```

### 4. Real-Time Collaboration (Socket.io)

```python
# app/websockets/handlers.py
from socketio import AsyncServer
from app.core.security import decode_token
import logging

logger = logging.getLogger(__name__)

sio = AsyncServer(async_mode='asgi', cors_allowed_origins='*')

# Store active connections
active_connections = {}

@sio.event
async def connect(sid, environ, auth):
    """Handle client connection"""
    
    try:
        # Verify JWT token
        token = auth.get('token')
        if not token:
            return False
        
        user_data = decode_token(token)
        
        # Store user info
        active_connections[sid] = {
            'user_id': user_data['user_id'],
            'project_id': None
        }
        
        logger.info(f"User {user_data['user_id']} connected: {sid}")
        return True
        
    except Exception as e:
        logger.error(f"Connection error: {e}")
        return False

@sio.event
async def disconnect(sid):
    """Handle client disconnection"""
    
    if sid in active_connections:
        user_data = active_connections[sid]
        project_id = user_data.get('project_id')
        
        if project_id:
            # Notify others in the project
            await sio.emit(
                'user_left',
                {
                    'user_id': user_data['user_id'],
                    'project_id': project_id
                },
                room=project_id,
                skip_sid=sid
            )
        
        del active_connections[sid]
        logger.info(f"User disconnected: {sid}")

@sio.event
async def join_project(sid, data):
    """Join a project room"""
    
    project_id = data.get('project_id')
    if not project_id:
        return {'error': 'Project ID required'}
    
    # Add to room
    sio.enter_room(sid, project_id)
    active_connections[sid]['project_id'] = project_id
    
    # Notify others
    await sio.emit(
        'user_joined',
        {
            'user_id': active_connections[sid]['user_id'],
            'project_id': project_id
        },
        room=project_id,
        skip_sid=sid
    )
    
    return {'success': True}

@sio.event
async def script_update(sid, data):
    """Broadcast script update to project members"""
    
    project_id = data.get('project_id')
    script_id = data.get('script_id')
    changes = data.get('changes')
    
    if not all([project_id, script_id, changes]):
        return {'error': 'Missing required fields'}
    
    # Broadcast to all except sender
    await sio.emit(
        'script_changed',
        {
            'script_id': script_id,
            'changes': changes,
            'user_id': active_connections[sid]['user_id']
        },
        room=project_id,
        skip_sid=sid
    )
    
    return {'success': True}

@sio.event
async def cursor_position(sid, data):
    """Broadcast cursor position for real-time collaboration"""
    
    project_id = data.get('project_id')
    position = data.get('position')
    
    if not all([project_id, position]):
        return {'error': 'Missing required fields'}
    
    await sio.emit(
        'cursor_moved',
        {
            'user_id': active_connections[sid]['user_id'],
            'position': position
        },
        room=project_id,
        skip_sid=sid
    )
    
    return {'success': True}
```

### 5. PDF Generation (Call Sheet)

```python
# app/services/pdf_service.py
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
from datetime import datetime
from typing import Dict, Any

class CallSheetPDFService:
    
    @staticmethod
    def generate_call_sheet(data: Dict[str, Any]) -> bytes:
        """Generate call sheet PDF"""
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a2e'),
            spaceAfter=20,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#16213e'),
            spaceAfter=10,
            spaceBefore=15
        )
        
        # Title
        story.append(Paragraph("CALL SHEET", title_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Production Info
        info_data = [
            ['Projeto:', data.get('project_name', '')],
            ['Data de Filmagem:', data.get('shoot_date', '')],
            ['Horário Geral:', data.get('call_time', '')],
            ['Diretor:', data.get('director', '')],
            ['Produtor:', data.get('producer', '')]
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Shooting Schedule
        story.append(Paragraph("CRONOGRAMA DE FILMAGEM", heading_style))
        
        schedule_data = [['Hora', 'Cena', 'Descrição', 'Localização']]
        schedule_data[0] = [Paragraph('<b>%s</b>' % x, styles['Normal']) 
                           for x in schedule_data[0]]
        
        for scene in data.get('scenes', []):
            schedule_data.append([
                scene.get('time', ''),
                scene.get('scene_number', ''),
                scene.get('description', ''),
                scene.get('location', '')
            ])
        
        schedule_table = Table(
            schedule_data,
            colWidths=[1*inch, 0.8*inch, 2.5*inch, 1.7*inch]
        )
        schedule_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#16213e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        
        story.append(schedule_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Cast List
        story.append(Paragraph("ELENCO", heading_style))
        
        cast_data = [['Personagem', 'Ator', 'Horário', 'Confirmado']]
        cast_data[0] = [Paragraph('<b>%s</b>' % x, styles['Normal']) 
                       for x in cast_data[0]]
        
        for cast in data.get('cast', []):
            confirmed = '✓' if cast.get('confirmed') else '✗'
            cast_data.append([
                cast.get('character', ''),
                cast.get('actor', ''),
                cast.get('call_time', ''),
                confirmed
            ])
        
        cast_table = Table(
            cast_data,
            colWidths=[2*inch, 2*inch, 1.2*inch, 1*inch]
        )
        cast_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#16213e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (3, 1), (3, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        
        story.append(cast_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Weather & Emergency
        story.append(Paragraph("INFORMAÇÕES IMPORTANTES", heading_style))
        
        emergency_data = [
            ['Clima:', data.get('weather', {}).get('description', 'N/A')],
            ['Temperatura:', f"{data.get('weather', {}).get('temp', 'N/A')}°C"],
            ['Hospital Mais Próximo:', data.get('nearest_hospital', 'N/A')],
            ['Endereço:', data.get('hospital_address', 'N/A')]
        ]
        
        emergency_table = Table(emergency_data, colWidths=[2*inch, 4*inch])
        emergency_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        story.append(emergency_table)
        
        # Notes
        if data.get('notes'):
            story.append(Spacer(1, 0.2*inch))
            story.append(Paragraph("OBSERVAÇÕES", heading_style))
            story.append(Paragraph(data['notes'], styles['Normal']))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
```

---

## 🔒 SECURITY BEST PRACTICES {#security}

### 1. Authentication Implementation

```python
# app/core/security.py
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash password"""
    return pwd_context.hash(password)

def decode_token(token: str) -> dict:
    """Decode and verify JWT token"""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        raise ValueError("Invalid token")
```

### 2. Rate Limiting

```python
# app/middleware/rate_limit.py
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
import redis
from datetime import datetime, timedelta

redis_client = redis.Redis(host='localhost', port=6379, db=0)

async def rate_limit_middleware(request: Request, call_next):
    """Rate limiting middleware"""
    
    # Get client IP
    client_ip = request.client.host
    
    # Rate limit: 100 requests per minute
    key = f"rate_limit:{client_ip}"
    current_count = redis_client.get(key)
    
    if current_count is None:
        redis_client.setex(key, 60, 1)
    elif int(current_count) >= 100:
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={"detail": "Rate limit exceeded"}
        )
    else:
        redis_client.incr(key)
    
    response = await call_next(request)
    return response
```

### 3. Input Validation (Pydantic)

```python
# app/schemas/script.py
from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime

class ScriptCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: Dict[str, Any]
    
    @validator('title')
    def title_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip()
    
    @validator('content')
    def content_valid_json(cls, v):
        if not isinstance(v, dict):
            raise ValueError('Content must be a valid JSON object')
        return v

class ScriptUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    content: Optional[Dict[str, Any]] = None
    
    class Config:
        extra = 'forbid'  # Don't allow extra fields

class Script(BaseModel):
    id: UUID
    project_id: UUID
    title: str
    version: int
    content: Dict[str, Any]
    is_current: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
```

---

## ⚡ PERFORMANCE & SCALABILITY {#performance}

### 1. Database Optimization

```python
# app/services/script_service.py (Optimized queries)
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

async def get_project_with_scripts(db: Session, project_id: UUID):
    """Get project with all scripts (optimized)"""
    
    # Use selectinload to avoid N+1 queries
    stmt = (
        select(models.Project)
        .options(
            selectinload(models.Project.scripts)
            .selectinload(models.Script.scenes)
        )
        .where(models.Project.id == project_id)
    )
    
    result = await db.execute(stmt)
    project = result.scalars().first()
    
    return project

# Add database indexes
# CREATE INDEX idx_scripts_project_current ON scripts(project_id, is_current) WHERE is_current = true;
# CREATE INDEX idx_scenes_script_sort ON scenes(script_id, sort_order);
```

### 2. Caching Strategy

```python
# app/services/cache_service.py
import redis
import json
from typing import Any, Optional
from datetime import timedelta

redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

class CacheService:
    
    @staticmethod
    def get(key: str) -> Optional[Any]:
        """Get value from cache"""
        value = redis_client.get(key)
        if value:
            return json.loads(value)
        return None
    
    @staticmethod
    def set(key: str, value: Any, ttl: int = 300):
        """Set value in cache with TTL"""
        redis_client.setex(
            key,
            ttl,
            json.dumps(value, default=str)
        )
    
    @staticmethod
    def delete(key: str):
        """Delete key from cache"""
        redis_client.delete(key)
    
    @staticmethod
    def invalidate_pattern(pattern: str):
        """Invalidate all keys matching pattern"""
        keys = redis_client.keys(pattern)
        if keys:
            redis_client.delete(*keys)

# Usage
async def get_project(project_id: UUID, db: Session):
    """Get project with caching"""
    
    cache_key = f"project:{project_id}"
    cached = CacheService.get(cache_key)
    
    if cached:
        return cached
    
    # Fetch from database
    project = db.query(models.Project).filter(
        models.Project.id == project_id
    ).first()
    
    if project:
        CacheService.set(cache_key, project.dict(), ttl=600)
    
    return project
```

### 3. Async Task Queue (Celery)

```python
# app/tasks/pdf_tasks.py
from celery import Celery
from app.services.pdf_service import CallSheetPDFService
from app.services.email_service import EmailService

celery_app = Celery('cineprod', broker='redis://localhost:6379/0')

@celery_app.task
def generate_and_send_callsheet(call_sheet_id: str):
    """Generate PDF and send emails (async task)"""
    
    # This runs in background
    # 1. Fetch call sheet data
    # 2. Generate PDF
    # 3. Send emails to all recipients
    
    from app.database import SessionLocal
    from app.models import CallSheet
    
    db = SessionLocal()
    
    try:
        call_sheet = db.query(CallSheet).filter(
            CallSheet.id == call_sheet_id
        ).first()
        
        if not call_sheet:
            return {"error": "Call sheet not found"}
        
        # Generate PDF
        pdf_bytes = CallSheetPDFService.generate_call_sheet(
            call_sheet.to_dict()
        )
        
        # Send emails
        recipients = call_sheet.recipients
        for recipient in recipients:
            EmailService.send_callsheet(
                to_email=recipient.contact.email,
                pdf_attachment=pdf_bytes,
                call_sheet_data=call_sheet.to_dict()
            )
        
        # Update status
        call_sheet.sent_at = datetime.utcnow()
        call_sheet.status = 'sent'
        db.commit()
        
        return {"success": True, "recipients_count": len(recipients)}
        
    finally:
        db.close()
```

---

## 🧪 TESTING STRATEGY {#testing}

### 1. Unit Tests (Backend)

```python
# tests/test_script_service.py
import pytest
from uuid import uuid4
from app.services import script_service
from app.schemas import ScriptCreate

@pytest.fixture
def sample_script_data():
    return ScriptCreate(
        title="Test Script",
        content={"type": "doc", "content": []}
    )

@pytest.fixture
def sample_project(db_session):
    from app.models import Project, Workspace
    
    workspace = Workspace(name="Test Workspace")
    db_session.add(workspace)
    db_session.commit()
    
    project = Project(
        workspace_id=workspace.id,
        name="Test Project"
    )
    db_session.add(project)
    db_session.commit()
    
    return project

def test_create_script(db_session, sample_project, sample_script_data):
    """Test script creation"""
    
    script = script_service.create_script(
        db=db_session,
        project_id=sample_project.id,
        script_data=sample_script_data,
        user_id=uuid4()
    )
    
    assert script.id is not None
    assert script.title == "Test Script"
    assert script.version == 1
    assert script.is_current is True

def test_update_script_content(db_session, sample_project, sample_script_data):
    """Test script update"""
    
    script = script_service.create_script(
        db=db_session,
        project_id=sample_project.id,
        script_data=sample_script_data,
        user_id=uuid4()
    )
    
    new_content = {"type": "doc", "content": [{"type": "paragraph"}]}
    updated_script = script_service.update_script(
        db=db_session,
        script=script,
        script_data={"content": new_content},
        user_id=uuid4()
    )
    
    assert updated_script.content == new_content
    assert updated_script.version == 2
```

### 2. Integration Tests (API)

```python
# tests/test_api_scripts.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_script_endpoint(test_user_token, test_project):
    """Test script creation API"""
    
    response = client.post(
        f"/api/v1/scripts/",
        json={
            "project_id": str(test_project.id),
            "title": "New Script",
            "content": {"type": "doc", "content": []}
        },
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Script"
    assert "id" in data

def test_get_script_unauthorized(test_project):
    """Test that unauthorized access is denied"""
    
    response = client.get(f"/api/v1/scripts/{uuid4()}")
    assert response.status_code == 401
```

### 3. E2E Tests (Frontend)

```typescript
// tests/e2e/script-editor.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Script Editor', () => {
  test.beforeEach(async ({ page }) => {
    // Login
    await page.goto('/login');
    await page.fill('input[name="email"]', 'test@example.com');
    await page.fill('input[name="password"]', 'password123');
    await page.click('button[type="submit"]');
    
    // Navigate to script
    await page.goto('/projects/test-project/script');
  });

  test('should create new script', async ({ page }) => {
    await page.click('[data-testid="new-script-button"]');
    await page.fill('[data-testid="script-title-input"]', 'Test Script');
    await page.click('[data-testid="create-button"]');
    
    await expect(page.locator('[data-testid="script-title"]')).toHaveText('Test Script');
  });

  test('should format script correctly', async ({ page }) => {
    const editor = page.locator('[data-testid="script-editor"]');
    
    await editor.click();
    await page.keyboard.type('INT. OFFICE - DAY');
    await page.keyboard.press('Enter');
    
    // Check if formatted as scene heading
    const heading = page.locator('.scene-heading');
    await expect(heading).toBeVisible();
  });

  test('should auto-save changes', async ({ page }) => {
    const editor = page.locator('[data-testid="script-editor"]');
    
    await editor.click();
    await page.keyboard.type('Some content here');
    
    // Wait for auto-save indicator
    await expect(page.locator('[data-testid="save-indicator"]')).toHaveText('Saved');
  });
});
```

---

## 🚀 DEVOPS & DEPLOYMENT {#devops}

### 1. Docker Setup

```dockerfile
# Dockerfile (Backend)
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY ./app /app/app

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```dockerfile
# Dockerfile (Frontend)
FROM node:18-alpine AS builder

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci

# Copy source
COPY . .

# Build
RUN npm run build

# Production image
FROM nginx:alpine

# Copy built assets
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### 2. Docker Compose (Development)

```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: cineprod
      POSTGRES_PASSWORD: cineprod_password
      POSTGRES_DB: cineprod_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    env_file:
      - ./backend/.env
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis
    volumes:
      - ./backend/app:/app/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
    ports:
      - "5173:5173"
    volumes:
      - ./frontend/src:/app/src
      - ./frontend/public:/app/public
    command: npm run dev -- --host

  celery:
    build:
      context: ./backend
      dockerfile: Dockerfile
    env_file:
      - ./backend/.env
    depends_on:
      - postgres
      - redis
    command: celery -A app.tasks.celery_app worker --loglevel=info

volumes:
  postgres_data:
```

### 3. CI/CD Pipeline (GitHub Actions)

```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test-backend:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test_db
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      
      - name: Run tests
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/test_db
        run: |
          cd backend
          pytest --cov=app --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  test-frontend:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: |
          cd frontend
          npm ci
      
      - name: Run linter
        run: |
          cd frontend
          npm run lint
      
      - name: Run tests
        run: |
          cd frontend
          npm run test
      
      - name: Build
        run: |
          cd frontend
          npm run build

  deploy:
    needs: [test-backend, test-frontend]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to production
        run: |
          # Deploy script here
          echo "Deploying to production..."
```

---

## 📝 CONCLUSÃO

Este guia técnico fornece uma base sólida para a implementação do CineProd. Principais takeaways:

1. **Arquitetura escalável** com separação clara frontend/backend
2. **Stack moderno** (React + FastAPI) testado em produção
3. **Real-time collaboration** via WebSockets
4. **Security-first** com JWT, rate limiting, validação
5. **Performance otimizada** com caching e queries eficientes
6. **DevOps robusto** com Docker e CI/CD

**Próximos passos técnicos:**
1. Setup do repositório com esta estrutura
2. Configurar ambientes (dev, staging, prod)
3. Implementar autenticação primeiro
4. Construir features iterativamente
5. Testar continuamente
6. Monitorar e otimizar

Boa sorte com a implementação! 🚀

---

*Documento técnico versão 1.0 - 27/10/2025*
