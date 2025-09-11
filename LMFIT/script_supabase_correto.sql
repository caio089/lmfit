-- ========================================
-- SCRIPT SQL CORRETO PARA LMFIT - SUPABASE
-- Baseado no modelo Django atual
-- ========================================

-- 1. APAGAR TABELAS EXISTENTES (se existirem)
DROP TABLE IF EXISTS loja_roupa CASCADE;
DROP TABLE IF EXISTS loja_adminuser CASCADE;

-- 2. TABELA PRINCIPAL - ROUPAS (conforme modelo Django)
CREATE TABLE loja_roupa (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(200) NOT NULL,
    descricao TEXT NOT NULL,
    preco DECIMAL(10,2) NOT NULL,
    categoria VARCHAR(50) NOT NULL CHECK (categoria IN ('tops', 'leggings', 'conjuntos', 'blusas', 'acessorios', 'macacao', 'macaquinho', 'short', 'regata')),
    tamanhos_disponiveis VARCHAR(20) DEFAULT 'P,M,G',
    foto_principal VARCHAR(500),
    foto_principal_storage_path VARCHAR(200),
    foto_2 VARCHAR(500),
    foto_2_storage_path VARCHAR(200),
    foto_3 VARCHAR(500),
    foto_3_storage_path VARCHAR(200),
    ativo BOOLEAN DEFAULT TRUE,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. TABELA DE USUÁRIOS ADMIN (conforme modelo Django)
CREATE TABLE loja_adminuser (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    nome VARCHAR(100) NOT NULL,
    ativo BOOLEAN DEFAULT TRUE,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. TABELAS DO DJANGO (se não existirem)
CREATE TABLE IF NOT EXISTS auth_user (
    id SERIAL PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login TIMESTAMP WITH TIME ZONE,
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    username VARCHAR(150) UNIQUE NOT NULL,
    first_name VARCHAR(150) NOT NULL DEFAULT '',
    last_name VARCHAR(150) NOT NULL DEFAULT '',
    email VARCHAR(254) NOT NULL DEFAULT '',
    is_staff BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    date_joined TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS django_session (
    session_key VARCHAR(40) PRIMARY KEY,
    session_data TEXT NOT NULL,
    expire_date TIMESTAMP WITH TIME ZONE NOT NULL
);

CREATE TABLE IF NOT EXISTS django_migrations (
    id SERIAL PRIMARY KEY,
    app VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    applied TIMESTAMP WITH TIME ZONE NOT NULL
);

CREATE TABLE IF NOT EXISTS django_content_type (
    id SERIAL PRIMARY KEY,
    app_label VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    UNIQUE(app_label, model)
);

CREATE TABLE IF NOT EXISTS auth_permission (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    content_type_id INTEGER NOT NULL REFERENCES django_content_type(id),
    codename VARCHAR(100) NOT NULL,
    UNIQUE(content_type_id, codename)
);

CREATE TABLE IF NOT EXISTS auth_group (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS auth_user_user_permissions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES auth_user(id),
    permission_id INTEGER NOT NULL REFERENCES auth_permission(id),
    UNIQUE(user_id, permission_id)
);

CREATE TABLE IF NOT EXISTS auth_user_groups (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES auth_user(id),
    group_id INTEGER NOT NULL REFERENCES auth_group(id),
    UNIQUE(user_id, group_id)
);

CREATE TABLE IF NOT EXISTS auth_group_permissions (
    id SERIAL PRIMARY KEY,
    group_id INTEGER NOT NULL REFERENCES auth_group(id),
    permission_id INTEGER NOT NULL REFERENCES auth_permission(id),
    UNIQUE(group_id, permission_id)
);

-- ========================================
-- ÍNDICES PARA PERFORMANCE
-- ========================================

CREATE INDEX IF NOT EXISTS idx_roupa_categoria ON loja_roupa(categoria);
CREATE INDEX IF NOT EXISTS idx_roupa_ativo ON loja_roupa(ativo);
CREATE INDEX IF NOT EXISTS idx_roupa_data_criacao ON loja_roupa(data_criacao);
CREATE INDEX IF NOT EXISTS idx_roupa_preco ON loja_roupa(preco);
CREATE INDEX IF NOT EXISTS idx_user_username ON auth_user(username);
CREATE INDEX IF NOT EXISTS idx_user_email ON auth_user(email);
CREATE INDEX IF NOT EXISTS idx_user_is_active ON auth_user(is_active);

-- ========================================
-- INSERIR USUÁRIO ADMIN PADRÃO
-- ========================================

-- Inserir usuário admin padrão
INSERT INTO auth_user (username, password, first_name, last_name, email, is_superuser, is_staff, is_active, date_joined)
VALUES ('admin', 'pbkdf2_sha256$600000$dummy$dummy', 'Admin', 'User', 'admin@lmfit.com', TRUE, TRUE, TRUE, NOW())
ON CONFLICT (username) DO NOTHING;

-- ========================================
-- VERIFICAR TABELAS CRIADAS
-- ========================================

SELECT 'Tabelas criadas com sucesso!' as status;
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_name LIKE 'loja_%' ORDER BY table_name;
