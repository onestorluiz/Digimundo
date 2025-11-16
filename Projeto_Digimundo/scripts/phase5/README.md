# 🛠️ Phase 5 Automation Scripts

**Purpose**: Automated tooling for Fase 5 implementation

---

## 📋 Available Scripts

### 1. check_file_exists.py ✅

**Purpose**: Check if file exists before creating (prevent duplicates)

**Usage**:
```bash
python scripts/phase5/check_file_exists.py app/services/new_service.py
```

**Exit Codes**:
- `0`: File doesn't exist (safe to create)
- `1`: File exists (do NOT create)

**Example Output**:
```
✅ File does NOT exist: app/services/new_service.py
   ⚠️  WARNING: File NOT in FILE_MANIFEST.yaml
   → Consider adding to manifest before creating

   📋 Similar files found:
      - app/services/scene_service.py
      - app/services/budget_service.py

   💡 TIP: Check if one of these is what you need before creating new file
```

---

### 2. sync_manifest.py 🔄

**Purpose**: Sync FILE_MANIFEST.yaml with filesystem reality

**Usage**:
```bash
# Sync and save changes
python scripts/phase5/sync_manifest.py

# Preview changes only (dry run)
python scripts/phase5/sync_manifest.py --dry-run
```

**What it does**:
1. Checks all `planned` files → updates to `staged` if they exist
2. Checks all `implemented` files → marks as `missing` if they don't exist
3. Finds untracked files on disk
4. Updates FILE_MANIFEST.yaml automatically

**Example Output**:
```
🔄 Syncing FILE_MANIFEST.yaml with filesystem...

📊 Checking file states...

✓ Found 3 state changes:
  ✓ app/ml/__init__.py: planned → staged
  ✓ app/cache/redis_client.py: planned → staged
  ⚠  app/services/old_scene_service.py: implemented → missing

📂 Scanning for untracked files...

⚠️  Found 5 untracked files:
  - app/services/experimental_service.py
  - tests/unit/test_new_feature.py
  ...

✅ Manifest synced: 3 changes saved
```

---

### 3. validate_imports.py 🔍

**Purpose**: Validate all imports are correct after refactoring

**Usage**:
```bash
# Validate all files
python scripts/phase5/validate_imports.py

# Validate specific file
python scripts/phase5/validate_imports.py --file app/services/scene_service.py

# Auto-fix broken imports (coming soon)
python scripts/phase5/validate_imports.py --fix
```

**What it does**:
1. Scans all `.py` files in app/, tests/, celery_tasks/
2. Detects broken imports (missing modules)
3. Suggests fixes based on common migration patterns
4. Optionally auto-fixes imports

**Example Output**:
```
🔍 Validating imports...

======================================================================
IMPORT VALIDATION RESULTS
======================================================================

Total imports checked: 1,243
✅ Valid:  1,240
❌ Broken: 3

======================================================================
BROKEN IMPORTS
======================================================================

📄 app/services/scene_service.py:
  Line 10: from app.services.old_event_store import EventStore
          Error: Module not found: app.services.old_event_store
          💡 Suggested fix: from app.services.event_store_service import EventStore

📄 tests/unit/test_conflict_detection.py:
  Line 5: from app.models.old_conflict import Conflict
          Error: Module not found: app.models.old_conflict
          💡 Suggested fix: from app.models.conflict import Conflict
```

**Exit Codes**:
- `0`: All imports valid
- `1`: Broken imports found

---

### 4. show_progress.py 📊

**Purpose**: Show implementation progress from FILE_MANIFEST.yaml

**Usage**:
```bash
# Show overall progress
python scripts/phase5/show_progress.py

# Show specific phase
python scripts/phase5/show_progress.py --phase 5.1

# Show files by state
python scripts/phase5/show_progress.py --state planned

# Show detailed file-by-file progress
python scripts/phase5/show_progress.py --detailed
```

**Example Output**:
```
┌────────────────────────────────────────────────────────────────────┐
│ FASE 5 - PLATFORM EVOLUTION                                         │
│ Overall Implementation Progress                                     │
├────────────────────────────────────────────────────────────────────┤
│ Progress: ▓▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 8%       │
│                                                                     │
│ ✅ Finalized:    3 files                                            │
│ 🟡 In Progress:  0 files                                            │
│ ⏳ Planned:     34 files                                            │
│ ❌ Deprecated:   2 files                                            │
│                                                                     │
│ Total Files:    39                                                  │
└────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────┐
│ PROGRESS BY PHASE                                                   │
└────────────────────────────────────────────────────────────────────┘

Phase 5.1: Foundation
  Progress: ▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 10%
  Files: 2/20 finalized
  Status: ✅2 🟡0 ⏳18

Phase 5.2: Conflict Detection
  Progress: ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0%
  Files: 0/4 finalized
  Status: ✅0 🟡0 ⏳4
```

---

## 🔄 Recommended Workflow

### Before Creating a New File

```bash
# 1. Check if file already exists
python scripts/phase5/check_file_exists.py app/services/new_service.py

# 2. If safe, create the file
# (manually or using IDE)

# 3. Sync manifest to track new file
python scripts/phase5/sync_manifest.py
```

### After Refactoring / Migration

```bash
# 1. Validate all imports still work
python scripts/phase5/validate_imports.py

# 2. If imports broken, fix them
python scripts/phase5/validate_imports.py --fix  # (when implemented)

# 3. Run tests
pytest tests/ -v

# 4. Sync manifest to update states
python scripts/phase5/sync_manifest.py
```

### Daily Progress Check

```bash
# Show overall progress
python scripts/phase5/show_progress.py

# Show current phase progress
python scripts/phase5/show_progress.py --phase 5.1 --detailed
```

---

## 🔗 Integration with FILE_MANIFEST.yaml

All scripts read from and update `docs/fase_5/FILE_MANIFEST.yaml`.

**States**:
- `planned` - File planned but not created
- `staged` - File created but not tested
- `implemented` - File implemented with tests
- `validated` - Tests passing + code review
- `finalized` - Merged + deployed
- `deprecated` - Marked for removal
- `missing` - Was implemented but now missing (needs investigation)

---

## 📈 Future Scripts (Roadmap)

### migrate_file.py (Planned)

```bash
python scripts/phase5/migrate_file.py \
  --source app/services/old_service.py \
  --target app/services/new_service.py \
  --backup \
  --update-imports \
  --run-tests
```

**What it will do**:
1. Backup source file
2. Copy source → target
3. Update all imports in codebase
4. Archive source file
5. Run tests
6. Update FILE_MANIFEST.yaml

### archive_old_files.py (Planned)

```bash
python scripts/phase5/archive_old_files.py --dry-run
python scripts/phase5/archive_old_files.py
```

**What it will do**:
1. Find all files with `state: deprecated`
2. Move to `_archived/` directory
3. Create archive manifest
4. Update FILE_MANIFEST.yaml

### create_file_from_manifest.py (Planned)

```bash
python scripts/phase5/create_file_from_manifest.py app/services/event_store_service.py
```

**What it will do**:
1. Read FILE_MANIFEST.yaml
2. Find file spec
3. Generate file from template (if provided)
4. Create file with proper structure
5. Update manifest state to `staged`

---

## 🤝 Contributing

When adding new scripts:

1. Follow naming convention: `{action}_{target}.py`
2. Include `--help` option
3. Add to this README
4. Update FILE_MANIFEST.yaml with script path + state

---

## 📞 Support

Questions? Check:
- `FILE_MANIFEST.yaml` - Source of truth for all files
- `MIGRATION_PLAN.md` - Migration strategies
- `IMPLEMENTATION_TRACKER.md` - Progress dashboard

---

**Mantido por**: Claude Code + Equipe Digimundo
**Última Atualização**: 2025-11-16
**Versão**: 1.0
