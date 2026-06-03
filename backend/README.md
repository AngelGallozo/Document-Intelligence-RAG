# Document Intelligence RAG

Sistema de consulta documental basado en LLMs capaz de procesar PDFs digitales y escaneados, extraer texto y tablas, generar embeddings semánticos, indexar contenido en una base vectorial y responder preguntas utilizando Retrieval-Augmented Generation (RAG) con modelos locales ejecutados mediante Ollama.

---

# Características

* Extracción de texto desde PDFs digitales mediante PyMuPDF.
* Detección automática de documentos escaneados.
* OCR mediante Tesseract OCR.
* Preprocesamiento de imágenes con OpenCV.
* Extracción de tablas mediante pdfplumber.
* Conversión de tablas a texto semántico para indexación.
* Segmentación inteligente de documentos.
* Generación de embeddings utilizando Sentence Transformers.
* Almacenamiento vectorial mediante ChromaDB.
* Recuperación semántica de contexto.
* Re-ranking de resultados mediante CrossEncoder.
* Generación de respuestas utilizando modelos locales con Ollama.
* Sistema de citas y trazabilidad documental.
* Gestión de documentos:

  * Subida
  * Consulta
  * Eliminación
  * Reindexación
  * Estado de indexación

---

# Arquitectura

```text
PDF
 │
 ▼
PyMuPDF
 │
 ├── Texto digital
 │
 └── OCR (si es escaneado)
         │
         ▼
     Tesseract OCR
         │
         ▼
 Limpieza de texto
         │
         ▼
 Extracción de tablas
    (pdfplumber)
         │
         ▼
 Conversión tabla → texto
         │
         ▼
 Chunking
         │
         ▼
 Embeddings
(multilingual-e5-base)
         │
         ▼
 ChromaDB
         │
         ▼
 Retriever
         │
         ▼
 Re-Ranker
(ms-marco-MiniLM)
         │
         ▼
 Prompt Builder
         │
         ▼
 Ollama
(Qwen3:4b)
         │
         ▼
 Respuesta + Citas
```

---

# Tecnologías utilizadas

## Backend

* Python 3.11+
* FastAPI
* Uvicorn

## Procesamiento documental

* PyMuPDF
* pdfplumber
* Tesseract OCR
* OpenCV

## IA y NLP

* Sentence Transformers
* CrossEncoder
* Ollama

## Base vectorial

* ChromaDB

---

# Modelos utilizados

## Embeddings

```text
intfloat/multilingual-e5-base
```

Utilizado para recuperación semántica y búsqueda vectorial.

---

## Re-ranking

```text
cross-encoder/ms-marco-MiniLM-L-6-v2
```

Utilizado para reordenar los resultados recuperados desde ChromaDB.

---

## LLM

```text
qwen3:4b
```

Ejecutado localmente mediante Ollama.

---

# Estructura del proyecto

```text
app/
│
├── api/
│   └── documents.py
│
├── models/
│   ├── chat_models.py
│   └── ocr_models.py
│
├── ocr/
│   ├── image_utils.py
│   ├── ocr_service.py
│   └── preprocessing.py
│
├── rag/
│   ├── generator.py
│   ├── prompt_builder.py
│   ├── rag_pipeline.py
│   ├── reranker.py
│   └── retriever.py
│
├── services/
│   ├── document_service.py
│   ├── embedding_service.py
│   ├── ingestion_service.py
│   ├── pdf_service.py
│   ├── preprocessing_service.py
│   ├── table_service.py
│   ├── vector_store_service.py
│   └── chunking_service.py
│
├── main.py
│
data/
│
├── pdfs/
├── processed/
├── vectordb/
├── temp_images/
└── debug_ocr/
```

---

# Flujo de ingestión documental

Endpoint:

```http
POST /upload
```

Proceso:

```text
PDF
 ↓
Guardar archivo
 ↓
Extraer texto
 ↓
Detectar documento escaneado
 ↓
OCR (si corresponde)
 ↓
Limpieza de texto
 ↓
Extracción de tablas
 ↓
Conversión tabla → texto semántico
 ↓
Chunking
 ↓
Embeddings
 ↓
ChromaDB
 ↓
Metadata
 ↓
Documento indexado
```

---

# Flujo RAG

Endpoint:

```http
POST /chat
```

Proceso:

```text
Pregunta
 ↓
Embedding de consulta
 ↓
Búsqueda vectorial
 ↓
Re-ranking
 ↓
Construcción de contexto
 ↓
Prompt
 ↓
Ollama
 ↓
Respuesta
 ↓
Fuentes y citas
```

---

# Instalación

## 1. Clonar repositorio

```bash
git clone https://github.com/usuario/document-intelligence-rag.git

cd document-intelligence-rag
```

---

## 2. Crear entorno virtual

Windows:

```bash
python -m venv venv

venv\Scripts\activate
```

Linux/Mac:

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

# Instalación de Tesseract OCR

## Windows

Descargar:

```text
https://github.com/UB-Mannheim/tesseract/wiki
```

Instalar y verificar:

```bash
tesseract --version
```

---

## Idioma español

Descargar:
```text
https://github.com/tesseract-ocr/tessdata/blob/main/spa.traineddata
```
Ubicar spa.traineddata en:
```text
..\Program Files\Tesseract-OCR\tessdata
```

Verificar:

```bash
tesseract --list-langs
```

Debe aparecer:

```text
spa
```

---

# Instalación de Ollama

Descargar:

```text
https://ollama.com/download
```

Verificar:

```bash
ollama --version
```

---

## Descargar modelo

```bash
ollama pull qwen3:4b
```

---

## Ejecutar Ollama

```bash
ollama serve
```

---

# Ejecutar la API

```bash
uvicorn app.main:app --reload
```

Swagger:

```text
http://localhost:8000/docs
```

---

# Endpoints

---

## Subir documento

```http
POST /upload
```

### Request

```text
multipart/form-data
```

### Parámetros

| Campo       | Tipo             |
| ----------- | ---------------- |
| file        | PDF              |
| ocr_profile | light / standard / -- |

En caso de que no sea un pdf con imagenes escaneadas, enviar el ocr_profile en `--`.

### Response

```json
{
  "filename": "manual_rrhh.pdf",
  "pages": 32,
  "chunks": 148,
  "tables_found": 5,
  "ocr_used": true,
  "ocr_profile": "standard"
}
```

---

## Listar documentos

```http
GET /documents
```

### Response

```json
[
  {
    "filename": "manual_rrhh.pdf",
    "processed": true,
    "size_bytes": 2458134
  }
]
```

---

## Obtener documento

```http
GET /documents/{filename}
```

---


## Obtener tablas

```http
GET /documents/{filename}/tables
```

---

## Estado de indexación

```http
GET /documents/{filename}/status
```

### Response

```json
{
  "filename": "manual_rrhh.pdf",
  "indexed": true,
  "pages": 32,
  "chunks": 148,
  "tables_found": 5,
  "ocr_used": true
}
```

---

## Eliminar documento

```http
DELETE /documents/{filename}
```

Elimina:

```text
data/pdfs
data/processed
data/chunks
ChromaDB
metadata
```

---

## Reindexar documento

```http
POST /documents/{filename}/reindex
```

Reconstruye:

```text
OCR
Tablas
Chunks
Embeddings
ChromaDB
Metadata
```

Sin necesidad de volver a subir el PDF.

---

## Búsqueda semántica
```text
GET /search
```
Query
```text
question=...
```
---

## Chat RAG

```http
POST /chat
```

### Request

```json
{
  "question": "¿Qué operadores aritméticos existen?"
}
```

### Response

```json
{
  "question": "¿Qué operadores aritméticos existen?",
  "answer": "Los operadores aritméticos son +, -, *, / [1].",
  "sources": [
    {
      "id": 1,
      "document": "Clase_03.pdf",
      "page": 6,
      "type": "table",
      "rerank_score": 4.04
    }
  ]
}
```

---

# Estado actual del proyecto

| Objetivo                           | Estado |
| ---------------------------------- | ------ |
| Consulta documental basada en LLMs | ✅      |
| OCR con Tesseract                  | ✅      |
| PDFs escaneados                    | ✅      |
| Extracción de tablas               | ✅      |
| Chunking                           | ✅      |
| Embeddings                         | ✅      |
| Recuperación semántica             | ✅      |
| ChromaDB                           | ✅      |
| RAG                                | ✅      |
| Ollama                             | ✅      |
| Re-ranking                         | ✅      |
| Citas y trazabilidad               | ✅      |
| Gestión documental                 | ✅      |
| GraphRAG                           | 🚧     |
| Neo4j                              | 🚧     |

---

# Próximas mejoras

## Frontend

* Next.js
* Chat estilo ChatGPT
* Gestión visual de documentos
* Visualización de citas

## Investigación

* Neo4j
* Extracción de entidades
* Relaciones documento-entidad
* GraphRAG
* Recuperación híbrida Vector + Grafo

---

# Licencia

Proyecto desarrollado con fines educativos, de investigación y aprendizaje sobre arquitecturas RAG, OCR documental y sistemas de recuperación semántica basados en LLMs.
