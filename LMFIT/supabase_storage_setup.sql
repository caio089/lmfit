-- =============================================
-- CONFIGURAÇÃO DO STORAGE BUCKET NO SUPABASE
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
-- VERIFICAÇÕES
-- =============================================

-- Verificar se o bucket foi criado
SELECT id, name, public, file_size_limit, allowed_mime_types 
FROM storage.buckets 
WHERE id = 'roupas';

-- Verificar políticas do storage
SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual
FROM pg_policies 
WHERE tablename = 'objects' 
AND schemaname = 'storage'
AND policyname LIKE '%roupas%';
