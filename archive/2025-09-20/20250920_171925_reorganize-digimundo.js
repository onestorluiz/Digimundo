#!/usr/bin/env node

/**
 * 🏗️ DIGIMUNDO PROFESSIONAL REORGANIZATION SCRIPT
 * Automated file reorganization with dependency tracking
 */

const fs = require('fs').promises;
const path = require('path');
const { exec } = require('child_process');
const { promisify } = require('util');
const execAsync = promisify(exec);

class DigimundoReorganizer {
  constructor() {
    this.baseDir = '/Users/clubproducoes/Digimundo';
    this.movedFiles = new Map(); // Track old path -> new path
    this.dependencies = new Map(); // Track file -> dependencies
    this.stats = {
      filesAnalyzed: 0,
      filesMoved: 0,
      importsUpdated: 0,
      duplicatesRemoved: 0,
      errors: []
    };
  }

  /**
   * Main reorganization flow
   */
  async reorganize() {
    console.log('🏗️ DIGIMUNDO PROFESSIONAL REORGANIZATION');
    console.log('=========================================\n');
    
    try {
      // 1. Create backup
      console.log('📦 Creating backup...');
      await this.createBackup();
      
      // 2. Analyze current structure
      console.log('\n🔍 Analyzing current structure...');
      await this.analyzeStructure();
      
      // 3. Create new directory structure
      console.log('\n📁 Creating new directory structure...');
      await this.createNewStructure();
      
      // 4. Move and reorganize files
      console.log('\n🚚 Moving files to new locations...');
      await this.moveFiles();
      
      // 5. Update all import paths
      console.log('\n🔄 Updating import paths...');
      await this.updateImports();
      
      // 6. Remove duplicates
      console.log('\n🗑️ Removing duplicate files...');
      await this.removeDuplicates();
      
      // 7. Validate structure
      console.log('\n✅ Validating new structure...');
      await this.validateStructure();
      
      // 8. Generate documentation
      console.log('\n📚 Generating documentation...');
      await this.generateDocumentation();
      
      // Print summary
      this.printSummary();
      
    } catch (error) {
      console.error('❌ Reorganization failed:', error);
      console.log('\n🔄 Restoring from backup...');
      await this.restoreBackup();
    }
  }

  /**
   * Create backup before reorganization
   */
  async createBackup() {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const backupPath = path.join(this.baseDir, `../digimundo-backup-${timestamp}.tar.gz`);
    
    await execAsync(`tar -czf ${backupPath} -C ${this.baseDir} .`);
    console.log(`  ✅ Backup created: ${backupPath}`);
    
    this.backupPath = backupPath;
  }

  /**
   * Analyze current file structure and dependencies
   */
  async analyzeStructure() {
    const files = await this.getAllFiles(this.baseDir);
    
    for (const file of files) {
      if (file.endsWith('.js') || file.endsWith('.ts')) {
        const content = await fs.readFile(file, 'utf-8');
        const deps = this.extractDependencies(content);
        this.dependencies.set(file, deps);
        this.stats.filesAnalyzed++;
      }
    }
    
    console.log(`  ✅ Analyzed ${this.stats.filesAnalyzed} files`);
  }

  /**
   * Extract dependencies from file content
   */
  extractDependencies(content) {
    const deps = [];
    
    // CommonJS requires
    const requireRegex = /require\(['"]([^'"]+)['"]\)/g;
    let match;
    while ((match = requireRegex.exec(content)) !== null) {
      deps.push({ type: 'require', path: match[1] });
    }
    
    // ES6 imports
    const importRegex = /import .* from ['"]([^'"]+)['"]/g;
    while ((match = importRegex.exec(content)) !== null) {
      deps.push({ type: 'import', path: match[1] });
    }
    
    return deps;
  }

  /**
   * Create new directory structure
   */
  async createNewStructure() {
    const dirs = [
      'apps/desktop/src/main',
      'apps/desktop/src/renderer',
      'apps/desktop/src/shared',
      'apps/web',
      'apps/cli',
      'core/agents/sabiamon',
      'core/agents/neuromon',
      'core/agents/bibliomon',
      'core/agents/scripturemon',
      'core/agents/ajamon',
      'core/agents/gestormon',
      'core/agents/shenlongmon',
      'core/consciousness',
      'core/integrations/ollama',
      'core/integrations/claude',
      'core/integrations/openai',
      'core/utils',
      'infrastructure/docker',
      'infrastructure/kubernetes',
      'infrastructure/monitoring',
      'infrastructure/scripts',
      'docs/architecture',
      'docs/api',
      'docs/guides',
      'docs/digimons',
      'tests/unit',
      'tests/integration',
      'tests/e2e',
      'data/models',
      'data/cache',
      'data/backups',
      'config/environments'
    ];
    
    for (const dir of dirs) {
      const fullPath = path.join(this.baseDir, dir);
      await fs.mkdir(fullPath, { recursive: true });
    }
    
    console.log(`  ✅ Created ${dirs.length} directories`);
  }

  /**
   * Move files to new locations based on their purpose
   */
  async moveFiles() {
    const moves = [
      // Core consciousness files
      { from: 'DIGIMUNDO_EVOLUTION.js', to: 'core/consciousness/evolution.js' },
      { from: 'SABIAMON_FUSION.js', to: 'core/agents/sabiamon/fusion.js' },
      { from: 'NEUROMON_STRATEGIC_ANALYSIS.md', to: 'docs/digimons/neuromon.md' },
      { from: 'GESTORMON_SYSTEM.js', to: 'core/agents/gestormon/system.js' },
      
      // CLI tools
      { from: 'CHAT_DIRETO.js', to: 'apps/cli/chat.js' },
      { from: 'DIGIMUNDO_TERMINAL.js', to: 'apps/cli/terminal.js' },
      { from: 'SYSTEM_DEBUG.js', to: 'apps/cli/debug.js' },
      
      // Electron app consolidation
      { from: 'DigimundoApp/src/main', to: 'apps/desktop/src/main' },
      { from: 'DigimundoApp/src/renderer', to: 'apps/desktop/src/renderer' },
      
      // Integrations
      { from: 'DigimundoApp/src/main/ollama-manager.js', to: 'core/integrations/ollama/manager.js' },
      { from: 'DigimundoApp/src/main/claude-integration.js', to: 'core/integrations/claude/index.js' },
      
      // Scripts
      { from: 'LAUNCH_DIGIMUNDO.sh', to: 'infrastructure/scripts/launch.sh' },
      { from: 'VALIDATE_DIGIMUNDO.sh', to: 'infrastructure/scripts/validate.sh' },
      { from: 'backup_refactoring.sh', to: 'infrastructure/scripts/backup.sh' },
      
      // Documentation
      { from: 'RESEARCH_PLAN_DIGIMUNDO_REFACTOR.md', to: 'docs/architecture/refactor-plan.md' },
      { from: 'DIGIMUNDO_APP_PACKAGING_STRATEGY.md', to: 'docs/guides/packaging.md' },
      { from: 'REVOLUTIONARY_ACHIEVEMENTS.md', to: 'docs/achievements.md' }
    ];
    
    for (const move of moves) {
      const fromPath = path.join(this.baseDir, move.from);
      const toPath = path.join(this.baseDir, move.to);
      
      try {
        // Check if source exists
        await fs.access(fromPath);
        
        // Create target directory if needed
        await fs.mkdir(path.dirname(toPath), { recursive: true });
        
        // Move file or directory
        await execAsync(`mv "${fromPath}" "${toPath}"`);
        
        // Track the move
        this.movedFiles.set(fromPath, toPath);
        this.stats.filesMoved++;
        
        console.log(`  ✓ Moved: ${move.from} → ${move.to}`);
      } catch (error) {
        // File doesn't exist or already moved
        continue;
      }
    }
    
    console.log(`  ✅ Moved ${this.stats.filesMoved} files`);
  }

  /**
   * Update all import paths in moved files
   */
  async updateImports() {
    for (const [oldPath, newPath] of this.movedFiles) {
      if (newPath.endsWith('.js') || newPath.endsWith('.ts')) {
        let content = await fs.readFile(newPath, 'utf-8');
        let updated = false;
        
        // Update require paths
        content = content.replace(/require\(['"]([^'"]+)['"]\)/g, (match, importPath) => {
          const newImportPath = this.resolveNewPath(importPath, oldPath, newPath);
          if (newImportPath !== importPath) {
            updated = true;
            this.stats.importsUpdated++;
            return `require('${newImportPath}')`;
          }
          return match;
        });
        
        // Update import paths
        content = content.replace(/from ['"]([^'"]+)['"]/g, (match, importPath) => {
          const newImportPath = this.resolveNewPath(importPath, oldPath, newPath);
          if (newImportPath !== importPath) {
            updated = true;
            this.stats.importsUpdated++;
            return `from '${newImportPath}'`;
          }
          return match;
        });
        
        if (updated) {
          await fs.writeFile(newPath, content);
          console.log(`  ✓ Updated imports in: ${path.basename(newPath)}`);
        }
      }
    }
    
    console.log(`  ✅ Updated ${this.stats.importsUpdated} imports`);
  }

  /**
   * Resolve new path for imports based on file moves
   */
  resolveNewPath(importPath, oldFilePath, newFilePath) {
    // Skip node_modules and absolute paths
    if (!importPath.startsWith('.') || importPath.includes('node_modules')) {
      return importPath;
    }
    
    // Resolve the absolute path of the import
    const oldDir = path.dirname(oldFilePath);
    const absoluteImport = path.resolve(oldDir, importPath);
    
    // Check if this file was moved
    const movedTo = this.movedFiles.get(absoluteImport) || 
                    this.movedFiles.get(absoluteImport + '.js') ||
                    this.movedFiles.get(absoluteImport + '/index.js');
    
    if (movedTo) {
      // Calculate new relative path
      const newDir = path.dirname(newFilePath);
      const newRelative = path.relative(newDir, movedTo);
      
      // Ensure it starts with ./ or ../
      if (!newRelative.startsWith('.')) {
        return './' + newRelative;
      }
      return newRelative;
    }
    
    return importPath;
  }

  /**
   * Remove duplicate files
   */
  async removeDuplicates() {
    const duplicates = [
      'DigimundoApp/src/main/ollama-manager-enhanced.js', // Keep only one version
      'DIGIMUNDO_ULTIMATE_DEBUGGER.js', // Merged with SYSTEM_DEBUG.js
      'DigimundoApp/test-*.js' // Old test files
    ];
    
    for (const dup of duplicates) {
      const fullPath = path.join(this.baseDir, dup);
      try {
        await fs.unlink(fullPath);
        this.stats.duplicatesRemoved++;
        console.log(`  ✓ Removed duplicate: ${dup}`);
      } catch (error) {
        // File doesn't exist
      }
    }
    
    console.log(`  ✅ Removed ${this.stats.duplicatesRemoved} duplicates`);
  }

  /**
   * Validate the new structure
   */
  async validateStructure() {
    let valid = true;
    
    // Check critical files exist
    const criticalFiles = [
      'apps/desktop/src/main/index.js',
      'core/consciousness/evolution.js',
      'core/integrations/ollama/manager.js'
    ];
    
    for (const file of criticalFiles) {
      const fullPath = path.join(this.baseDir, file);
      try {
        await fs.access(fullPath);
      } catch {
        console.log(`  ❌ Missing critical file: ${file}`);
        valid = false;
      }
    }
    
    if (valid) {
      console.log('  ✅ Structure validation passed');
    } else {
      throw new Error('Structure validation failed');
    }
  }

  /**
   * Generate comprehensive documentation
   */
  async generateDocumentation() {
    const doc = {
      timestamp: new Date().toISOString(),
      structure: {
        apps: 'All application interfaces (desktop, web, CLI)',
        core: 'Business logic, AI agents, integrations',
        infrastructure: 'DevOps, scripts, monitoring',
        docs: 'All documentation',
        tests: 'Test suites',
        data: 'Models, cache, backups',
        config: 'Configuration files'
      },
      movedFiles: Array.from(this.movedFiles.entries()).map(([from, to]) => ({
        from: from.replace(this.baseDir + '/', ''),
        to: to.replace(this.baseDir + '/', '')
      })),
      stats: this.stats,
      entryPoints: {
        desktop: 'apps/desktop/src/main/index.js',
        cli: 'apps/cli/terminal.js',
        web: 'apps/web/index.js'
      }
    };
    
    await fs.writeFile(
      path.join(this.baseDir, 'REORGANIZATION_REPORT.json'),
      JSON.stringify(doc, null, 2)
    );
    
    console.log('  ✅ Documentation generated');
  }

  /**
   * Get all files recursively
   */
  async getAllFiles(dir, fileList = []) {
    const files = await fs.readdir(dir);
    
    for (const file of files) {
      const filePath = path.join(dir, file);
      const stat = await fs.stat(filePath);
      
      if (stat.isDirectory()) {
        // Skip certain directories
        if (!file.includes('node_modules') && !file.includes('.git')) {
          await this.getAllFiles(filePath, fileList);
        }
      } else {
        fileList.push(filePath);
      }
    }
    
    return fileList;
  }

  /**
   * Restore from backup if needed
   */
  async restoreBackup() {
    if (this.backupPath) {
      await execAsync(`tar -xzf ${this.backupPath} -C ${this.baseDir}`);
      console.log('  ✅ Restored from backup');
    }
  }

  /**
   * Print summary
   */
  printSummary() {
    console.log('\n' + '='.repeat(50));
    console.log('📊 REORGANIZATION COMPLETE');
    console.log('='.repeat(50));
    console.log(`Files Analyzed: ${this.stats.filesAnalyzed}`);
    console.log(`Files Moved: ${this.stats.filesMoved}`);
    console.log(`Imports Updated: ${this.stats.importsUpdated}`);
    console.log(`Duplicates Removed: ${this.stats.duplicatesRemoved}`);
    
    if (this.stats.errors.length > 0) {
      console.log(`\n⚠️ Errors: ${this.stats.errors.length}`);
      this.stats.errors.forEach(err => console.log(`  - ${err}`));
    }
    
    console.log('\n✨ Your Digimundo project is now professionally organized!');
    console.log('📚 See REORGANIZATION_REPORT.json for details');
  }
}

// Run if executed directly
if (require.main === module) {
  const reorganizer = new DigimundoReorganizer();
  reorganizer.reorganize().catch(console.error);
}

module.exports = DigimundoReorganizer;