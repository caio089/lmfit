-- =============================================
-- SCRIPT SQL COMPLETO PARA SUPABASE
-- PODE SER EXECUTADO MÚLTIPLAS VEZES SEM ERROS
-- =============================================

-- Habilitar extensões necessárias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =============================================
-- TABELA: loja_roupa
-- =============================================
CREATE TABLE IF NOT EXISTS public.loja_roupa (
    id BIGSERIAL PRIMARY KEY,
    nome VARCHAR(200) NOT NULL,
    descricao TEXT NOT NULL,
    preco DECIMAL(10,2) NOT NULL,
    categoria VARCHAR(50) NOT NULL CHECK (categoria IN ('tops', 'leggings', 'conjuntos', 'blusas', 'acessorios', 'macacao', 'macaquinho', 'short', 'regata')),
    tamanhos_disponiveis VARCHAR(20) DEFAULT 'P,M,G',
    foto_principal VARCHAR(500) NOT NULL,
    foto_principal_storage_path VARCHAR(200),
    foto_2 VARCHAR(500),
    foto_2_storage_path VARCHAR(200),
    foto_3 VARCHAR(500),
    foto_3_storage_path VARCHAR(200),
    ativo BOOLEAN DEFAULT TRUE,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices para performance
CREATE INDEX IF NOT EXISTS idx_loja_roupa_categoria ON public.loja_roupa(categoria);
CREATE INDEX IF NOT EXISTS idx_loja_roupa_ativo ON public.loja_roupa(ativo);
CREATE INDEX IF NOT EXISTS idx_loja_roupa_data_criacao ON public.loja_roupa(data_criacao DESC);

-- =============================================
-- TABELA: loja_adminuser
-- =============================================
CREATE TABLE IF NOT EXISTS public.loja_adminuser (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    nome VARCHAR(100) NOT NULL,
    ativo BOOLEAN DEFAULT TRUE,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índice para username
CREATE INDEX IF NOT EXISTS idx_loja_adminuser_username ON public.loja_adminuser(username);

-- =============================================
-- FUNÇÃO: Atualizar data_atualizacao automaticamente
-- =============================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.data_atualizacao = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger para atualizar data_atualizacao na tabela loja_roupa
DROP TRIGGER IF EXISTS update_loja_roupa_updated_at ON public.loja_roupa;
CREATE TRIGGER update_loja_roupa_updated_at
    BEFORE UPDATE ON public.loja_roupa
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- =============================================
-- POLÍTICAS RLS (Row Level Security)
-- =============================================

-- Habilitar RLS nas tabelas
ALTER TABLE public.loja_roupa ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.loja_adminuser ENABLE ROW LEVEL SECURITY;

-- Política para loja_roupa - permitir leitura pública para roupas ativas
DROP POLICY IF EXISTS "Permitir leitura pública de roupas ativas" ON public.loja_roupa;
CREATE POLICY "Permitir leitura pública de roupas ativas" ON public.loja_roupa
    FOR SELECT USING (ativo = true);

-- Política para loja_roupa - permitir todas as operações para service_role
DROP POLICY IF EXISTS "Permitir todas operações para service_role" ON public.loja_roupa;
CREATE POLICY "Permitir todas operações para service_role" ON public.loja_roupa
    FOR ALL USING (auth.role() = 'service_role');

-- Política para loja_adminuser - permitir todas as operações para service_role
DROP POLICY IF EXISTS "Permitir todas operações para service_role" ON public.loja_adminuser;
CREATE POLICY "Permitir todas operações para service_role" ON public.loja_adminuser
    FOR ALL USING (auth.role() = 'service_role');

-- =============================================
-- DADOS INICIAIS
-- =============================================

-- Inserir usuário admin padrão (senha: admin123)
INSERT INTO public.loja_adminuser (username, password, nome, ativo) 
VALUES ('admin', 'admin123', 'Administrador', true)
ON CONFLICT (username) DO UPDATE SET
    password = EXCLUDED.password,
    nome = EXCLUDED.nome,
    ativo = EXCLUDED.ativo;

-- =============================================
-- STORAGE BUCKET
-- =============================================

-- Criar bucket para imagens das roupas
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES (
    'roupas',
    'roupas', 
    true,  -- Bucket público para permitir acesso direto às imagens
    52428800,  -- 50MB limite por arquivo
    ARRAY['image/jpeg', 'image/jpg', 'image/png', 'image/webp']  -- Tipos de arquivo permitidos
)
ON CONFLICT (id) DO UPDATE SET
    public = true,
    file_size_limit = 52428800,
    allowed_mime_types = ARRAY['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];

-- =============================================
-- POLÍTICAS DE ACESSO AO STORAGE
-- =============================================

-- Política para permitir leitura pública das imagens
DROP POLICY IF EXISTS "Permitir leitura pública das imagens" ON storage.objects;
CREATE POLICY "Permitir leitura pública das imagens" ON storage.objects
FOR SELECT USING (bucket_id = 'roupas');

-- Política para permitir upload para service_role
DROP POLICY IF EXISTS "Permitir upload para service_role" ON storage.objects;
CREATE POLICY "Permitir upload para service_role" ON storage.objects
FOR INSERT WITH CHECK (bucket_id = 'roupas' AND auth.role() = 'service_role');

-- Política para permitir atualização para service_role
DROP POLICY IF EXISTS "Permitir atualização para service_role" ON storage.objects;
CREATE POLICY "Permitir atualização para service_role" ON storage.objects
FOR UPDATE USING (bucket_id = 'roupas' AND auth.role() = 'service_role');

-- Política para permitir exclusão para service_role
DROP POLICY IF EXISTS "Permitir exclusão para service_role" ON storage.objects;
CREATE POLICY "Permitir exclusão para service_role" ON storage.objects
FOR DELETE USING (bucket_id = 'roupas' AND auth.role() = 'service_role');

-- =============================================
-- COMENTÁRIOS DAS TABELAS
-- =============================================
COMMENT ON TABLE public.loja_roupa IS 'Tabela para armazenar informações das roupas da loja';
COMMENT ON COLUMN public.loja_roupa.categoria IS 'Categoria da roupa: tops, leggings, conjuntos, blusas, acessorios, macacao, macaquinho, short, regata';
COMMENT ON COLUMN public.loja_roupa.tamanhos_disponiveis IS 'Tamanhos disponíveis separados por vírgula (ex: P,M,G)';
COMMENT ON COLUMN public.loja_roupa.foto_principal IS 'URL da foto principal da roupa';
COMMENT ON COLUMN public.loja_roupa.foto_principal_storage_path IS 'Caminho no storage do Supabase para a foto principal';

COMMENT ON TABLE public.loja_adminuser IS 'Tabela para usuários administradores da loja';
COMMENT ON COLUMN public.loja_adminuser.password IS 'Senha do administrador (em produção, usar hash)';

-- =============================================
-- VERIFICAÇÕES FINAIS
-- =============================================

-- Verificar se as tabelas foram criadas
SELECT 
    'TABELAS CRIADAS' as status,
    table_name,
    table_type
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('loja_roupa', 'loja_adminuser')
ORDER BY table_name;

-- Verificar se os índices foram criados
SELECT 
    'ÍNDICES CRIADOS' as status,
    indexname,
    tablename
FROM pg_indexes 
WHERE schemaname = 'public' 
AND tablename IN ('loja_roupa', 'loja_adminuser')
ORDER BY tablename, indexname;

-- Verificar se o bucket foi criado
SELECT 
    'BUCKET CRIADO' as status,
    id, 
    name, 
    public, 
    file_size_limit, 
    allowed_mime_types 
FROM storage.buckets 
WHERE id = 'roupas';

-- Verificar políticas do storage
SELECT 
    'POLÍTICAS STORAGE' as status,
    policyname, 
    permissive, 
    roles, 
    cmd
FROM pg_policies 
WHERE tablename = 'objects' 
AND schemaname = 'storage'
AND policyname LIKE '%roupas%';

-- Verificar usuário admin
SELECT 
    'USUÁRIO ADMIN' as status,
    username, 
    nome, 
    ativo, 
    data_criacao
FROM public.loja_adminuser 
WHERE username = 'admin';
