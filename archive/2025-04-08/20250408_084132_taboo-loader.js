
const TabooLoader = {
    permissoes: [],
    carregar: async function() {
        try {
            const resposta = await fetch('../../digidata/permissions_taboo.json');
            const json = await resposta.json();
            this.permissoes = json.permissoes || [];
            console.log('🔓 Permissões Taboo carregadas:', this.permissoes);
        } catch (erro) {
            console.error('❌ Falha ao carregar permissões taboo.', erro);
        }
    }
};
TabooLoader.carregar();
