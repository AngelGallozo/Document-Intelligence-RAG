# Document Intelligence Platform

Sistema de inteligencia documental basado en LLMs para consulta de documentación privada mediante técnicas de OCR, extracción estructurada de información, recuperación semántica y Retrieval-Augmented Generation (RAG).

El proyecto permite procesar documentos PDF digitales y escaneados, extraer texto y tablas, indexar conocimiento en una base vectorial y responder preguntas utilizando modelos de lenguaje ejecutados localmente.

---

## Objetivos

- Consulta documental basada en LLMs.
- Extracción de texto desde PDFs digitales.
- OCR para documentos escaneados.
- Extracción de información estructurada mediante tablas.
- Recuperación semántica mediante embeddings.
- Arquitectura RAG para preguntas y respuestas.
- Integración con modelos locales mediante Ollama.
- Trazabilidad documental mediante referencias.
- Investigación de GraphRAG con Neo4j.

---

## Arquitectura General

```text
                ┌───────────────┐
                │     PDFs      │
                └───────┬───────┘
                        │
                        ▼
             ┌────────────────────┐
             │ Document Ingestion │
             └─────────┬──────────┘
                       │
        ┌──────────────┼───────────────┐
        │                              │
        ▼                              ▼
   Texto PDF                      OCR (Tesseract)
   (PyMuPDF)                         + OpenCV
        │                             │
        └──────────────┬──────────────┘
                       ▼
              Extracción de tablas
                  (pdfplumber)
                       │
                       ▼
                   Chunking
                       │
                       ▼
                   Embeddings
                       │
                       ▼
                   ChromaDB
                       │
                       ▼
                   Retriever
                       │
                       ▼
                   Re-Ranker
                       │
                       ▼
                     Ollama
                     Qwen3
                       │
                       ▼
                Respuesta + Fuentes
```
---

## Estructura del proyecto
```text
Document-Intelligence-RAG/
├── backend/
│   ├── app/
│   ├── data/
│   ├── requirements.txt
│   └── README.md
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── README.md
│
└── README.md
```
---

## Componentes
### Backend

Responsable de:

* Procesamiento documental.
* OCR.
* Extracción de tablas.
* Embeddings.
* ChromaDB.
* RAG.
* Ollama.
* Gestión documental.

Más información:
```text
/backend/README.md
```

### Frontend

Responsable de:

* Gestión visual de documentos.
* Interfaz conversacional.
* Visualización de respuestas.
* Visualización de fuentes y referencias.

Más información:
```text
/frontend/README.md
```
---

## Tecnologías
### Backend
* Python
* FastAPI
* PyMuPDF
* pdfplumber
* OpenCV
* Tesseract OCR
* ChromaDB
* Sentence Transformers
* Ollama
### Frontend
* Next.js
* React
* TypeScript

---

### Modelos utilizados

Embeddings
```text
intfloat/multilingual-e5-base
```
Re-ranking
```text
cross-encoder/ms-marco-MiniLM-L-6-v2
```
LLM
```text
qwen3:4b
```
---
## Estado actual
| Funcionalidad           | Estado |
| ----------------------- | ------ |
| OCR                     | ✅      |
| PDFs escaneados         | ✅      |
| Extracción de tablas    | ✅      |
| Chunking                | ✅      |
| Embeddings              | ✅      |
| ChromaDB                | ✅      |
| Recuperación semántica  | ✅      |
| Re-Ranking              | ✅      |
| Ollama                  | ✅      |
| RAG                     | ✅      |
| Trazabilidad documental | ✅      |
| Gestión documental      | ✅      |
| Frontend                | 🚧     |
| GraphRAG                | 🚧     |
| Neo4j                   | 🚧     |

---

## Roadmap
### Fase 1 - Backend RAG (Terminada)
* OCR
* Extracción de tablas
* Embeddings
* ChromaDB
* Re-ranking
* Ollama
* Gestión documental
### Fase 2 - Frontend (En proceso...)
* Next.js
* Chat estilo ChatGPT
* Gestión de documentos
* Visualización de referencias
### Fase 3 - GraphRAG
* Neo4j
* Extracción de entidades
* Grafo de conocimiento
* Recuperación híbrida
* GraphRAG

---

## Capturas

Próximamente.

---

## Licencia

Proyecto desarrollado con fines educativos, investigación y aprendizaje sobre sistemas RAG, OCR documental, recuperación semántica y GraphRAG.