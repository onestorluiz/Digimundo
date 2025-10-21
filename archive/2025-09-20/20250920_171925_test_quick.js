#!/usr/bin/env node

/**
 * TESTE RÁPIDO - Verifica se tudo está funcionando
 */

const fs = require('fs');
const path = require('path');

console.log('🔍 TESTE RÁPIDO DO SISTEMA');
console.log('===========================\n');

// 1. Verificar package.json
const pkg = JSON.parse(fs.readFileSync('package.json', 'utf-8'));
if (pkg.type === 'module') {
    console.log('❌ package.json ainda tem "type": "module"');
    console.log('   Execute: node fix_to_commonjs.js');
} else {
    console.log('✅ package.json está em modo CommonJS');
}

// 2. Testar módulos
try {
    const jwt = require('jsonwebtoken');
    console.log('✅ jsonwebtoken funciona');
} catch (e) {
    console.log('❌ jsonwebtoken erro:', e.message);
}

try {
    const bcrypt = require('bcrypt');
    console.log('✅ bcrypt funciona');
} catch (e) {
    console.log('❌ bcrypt erro:', e.message);
}

// 3. Verificar arquivos
const files = [
    'app/main.js',
    'app/server/index.js',
    'app/server/auth.js'
];

files.forEach(file => {
    if (fs.existsSync(file)) {
        const content = fs.readFileSync(file, 'utf-8');
        if (content.includes('import ') && !content.includes('// import')) {
            console.log(`⚠️ ${file} ainda usa import ESM`);
        } else if (content.includes('require(')) {
            console.log(`✅ ${file} usa require CommonJS`);
        }
    } else {
        console.log(`❌ ${file} não existe`);
    }
});

console.log('\n===========================');
console.log('Se todos estão ✅, execute: npm run dev');
console.log('Se houver ❌, execute: node fix_to_commonjs.js');
