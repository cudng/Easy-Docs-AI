-- Initial schema: documents, chats, chat_documents, messages
-- Includes RLS policies, indexes, and updated_at trigger.

-- =========================================================================
-- Shared trigger function: bump updated_at on UPDATE
-- =========================================================================
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;


-- =========================================================================
-- documents
-- =========================================================================
CREATE TYPE document_status AS ENUM ('uploading', 'ready', 'failed');

CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    file_name TEXT NOT NULL CHECK (char_length(file_name) <= 255),
    storage_path TEXT NOT NULL CHECK (char_length(storage_path) <= 255),
    size_bytes INTEGER NOT NULL CHECK (size_bytes > 0 AND size_bytes <= 5242880),
    status document_status NOT NULL DEFAULT 'uploading',
    file_hash CHAR(64) NOT NULL,
    UNIQUE (user_id, file_hash)
);

ALTER TABLE documents ENABLE ROW LEVEL SECURITY;

CREATE INDEX idx_documents_user_id ON documents(user_id);

CREATE POLICY "Users can view own documents"
  ON documents FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own documents"
  ON documents FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own documents"
  ON documents FOR UPDATE
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own documents"
  ON documents FOR DELETE
  USING (auth.uid() = user_id);


-- =========================================================================
-- chats
-- =========================================================================
CREATE TABLE chats (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    title VARCHAR(75) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TRIGGER chats_set_updated_at
BEFORE UPDATE ON chats
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();

ALTER TABLE chats ENABLE ROW LEVEL SECURITY;

CREATE INDEX idx_chats_user_id ON chats(user_id);

CREATE POLICY "Users can view own chats"
  ON chats FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own chats"
  ON chats FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own chats"
  ON chats FOR UPDATE
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own chats"
  ON chats FOR DELETE
  USING (auth.uid() = user_id);


-- =========================================================================
-- chat_documents (junction)
-- =========================================================================
CREATE TABLE chat_documents (
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    chat_id UUID NOT NULL REFERENCES chats(id) ON DELETE CASCADE,
    PRIMARY KEY (chat_id, document_id)
);

ALTER TABLE chat_documents ENABLE ROW LEVEL SECURITY;

CREATE INDEX idx_chat_documents_document_id ON chat_documents(document_id);

CREATE POLICY "Users can view own chat_documents"
  ON chat_documents FOR SELECT
  USING (
    EXISTS (SELECT 1 FROM chats WHERE chats.id = chat_id AND chats.user_id = auth.uid())
  );

CREATE POLICY "Users can insert own chat_documents"
  ON chat_documents FOR INSERT
  WITH CHECK (
    EXISTS (SELECT 1 FROM chats WHERE chats.id = chat_id AND chats.user_id = auth.uid())
    AND
    EXISTS (SELECT 1 FROM documents WHERE documents.id = document_id AND documents.user_id = auth.uid())
  );

CREATE POLICY "Users can delete own chat_documents"
  ON chat_documents FOR DELETE
  USING (
    EXISTS (SELECT 1 FROM chats WHERE chats.id = chat_id AND chats.user_id = auth.uid())
  );


-- =========================================================================
-- messages
-- =========================================================================
CREATE TYPE sender AS ENUM ('user', 'ai');

CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chat_id UUID NOT NULL REFERENCES chats(id) ON DELETE CASCADE,
    sender sender NOT NULL,
    content TEXT NOT NULL CHECK (
        (sender = 'user' AND char_length(content) <= 8000)
        OR
        (sender = 'ai' AND char_length(content) <= 16000)
    ),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);

ALTER TABLE messages ENABLE ROW LEVEL SECURITY;

CREATE INDEX idx_messages_chat_id ON messages(chat_id);

CREATE POLICY "Users can view own messages"
  ON messages FOR SELECT
  USING (
    EXISTS (SELECT 1 FROM chats WHERE chats.id = chat_id AND chats.user_id = auth.uid())
  );

CREATE POLICY "Users can insert own messages"
  ON messages FOR INSERT
  WITH CHECK (
    EXISTS (SELECT 1 FROM chats WHERE chats.id = chat_id AND chats.user_id = auth.uid())
  );
