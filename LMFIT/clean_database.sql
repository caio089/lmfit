-- ========================================
-- SCRIPT PARA LIMPAR BANCO NO SUPABASE
-- ========================================

-- 1. Deletar tabelas do Django se existirem
DROP TABLE IF EXISTS loja_roupa CASCADE;
DROP TABLE IF EXISTS loja_adminuser CASCADE;

-- 2. Limpar histórico de migrações do Django
DELETE FROM django_migrations WHERE app = 'loja';

-- 3. Deletar tabelas do sistema Django se existirem
DROP TABLE IF EXISTS django_migrations CASCADE;
DROP TABLE IF EXISTS django_content_type CASCADE;
DROP TABLE IF EXISTS django_admin_log CASCADE;
DROP TABLE IF EXISTS auth_user CASCADE;
DROP TABLE IF EXISTS auth_group CASCADE;
DROP TABLE IF EXISTS auth_permission CASCADE;
DROP TABLE IF EXISTS auth_user_groups CASCADE;
DROP TABLE IF EXISTS auth_user_user_permissions CASCADE;
DROP TABLE IF EXISTS auth_group_permissions CASCADE;
DROP TABLE IF EXISTS django_session CASCADE;

-- 4. Recriar tabela de migrações do Django
CREATE TABLE django_migrations (
    id BIGSERIAL PRIMARY KEY,
    app VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    applied TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- 5. Executar este script no Supabase SQL Editor
-- Depois execute o deploy no Render
