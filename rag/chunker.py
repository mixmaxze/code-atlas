class UniversalChunker:

    def chunk_file(self, file_path, chunk_size=120):

        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        chunks = []

        for i in range(0, len(lines), chunk_size):

            chunk_lines = lines[i:i + chunk_size]

            chunk_code = "".join(chunk_lines)

            chunks.append({
                "type": "code_block",
                "name": f"{file_path}_chunk_{i}",
                "file": file_path,
                "start_line": i + 1,
                "end_line": min(i + chunk_size, len(lines)),
                "code": chunk_code
            })

        return chunks


def chunk_files(file_list):

    chunker = UniversalChunker()

    all_chunks = []

    for file in file_list:

        try:
            chunks = chunker.chunk_file(file)
            all_chunks.extend(chunks)

        except Exception as e:
            print(f"Chunking failed for {file}: {e}")

    return all_chunks
