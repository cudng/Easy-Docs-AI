ALTER TABLE document_chunks
  ADD CONSTRAINT document_chunks_document_id_chunk_index_key
  UNIQUE (document_id, chunk_index);
