import { createRequire } from 'module';
const require = createRequire(import.meta.url);

console.log('\n📋 Verificação de Dependências:');
console.log('================================\n');

const modules = [
    'jsonwebtoken',
    'bcrypt',
    'express',
    'cors',
    'socket.io',
    'sqlite3',
    'dotenv',
    'axios',
    'node-fetch'
];

let allOk = true;

for (const module of modules) {
    try {
        require.resolve(module);
        console.log(`✅ ${module} - OK`);
    } catch (e) {
        console.log(`❌ ${module} - FALTANDO`);
        allOk = false;
    }
}

console.log('\n================================');
if (allOk) {
    console.log('✅ Todas as dependências estão instaladas!');
} else {
    console.log('❌ Algumas dependências estão faltando.');
    console.log('   Execute: npm install');
}
console.log('================================\n');

process.exit(allOk ? 0 : 1);
