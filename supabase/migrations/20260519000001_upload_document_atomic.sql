CREATE OR REPLACE FUNCTION upload_document_atomic(
    p_file_name text,
    p_storage_path text,
    p_size_bytes integer,
    p_file_hash char(64),
    p_chat_id uuid,
    p_chunks jsonb
) RETURNS uuid
LANGUAGE plpgsql
SECURITY INVOKER
SET search_path = public
AS $$
DECLARE
    v_document_id uuid;
BEGIN
    INSERT INTO documents (user_id, file_name, storage_path, size_bytes, file_hash, status)
    VALUES (auth.uid(), p_file_name, p_storage_path, p_size_bytes, p_file_hash, 'ready')
    RETURNING id INTO v_document_id;

    INSERT INTO document_chunks (document_id, chunk_index, content, embedding)
    SELECT
        v_document_id,
        (row_number() OVER ()) - 1,
        chunk->>'content',
        (chunk->>'embedding')::vector(2048)
    FROM jsonb_array_elements(p_chunks) AS chunk;

    INSERT INTO chat_documents (chat_id, document_id)
    VALUES (p_chat_id, v_document_id);

    RETURN v_document_id;
END;
$$;

GRANT EXECUTE ON FUNCTION upload_document_atomic(text, text, integer, char, uuid, jsonb) TO authenticated;
