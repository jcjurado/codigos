import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from logging_config import get_logger

load_dotenv(override=True)

DOCS_DIR    = "./docs"
CHROMA_DIR  = "./chroma_db"
EMBED_MODEL = "models/gemini-embedding-001"
TOP_K       = 4

logger = get_logger("Config RAG")

def cargar_documentos(ruta: str = DOCS_DIR):
    documentos = []

    pdf_loader = DirectoryLoader(ruta, glob="**/*.pdf", loader_cls=PyPDFLoader)
    pdfs = pdf_loader.load()
    documentos.extend(pdfs)
    logger.info(f"✅ {len(pdfs)} páginas PDF cargadas")
    txt_loader = DirectoryLoader(
        ruta,
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )
    txts = txt_loader.load()
    documentos.extend(txts)
    logger.info(f"✅ {len(txts)} archivos TXT cargados")

    logger.info(f"📄 Total: {len(documentos)} documentos")
    return documentos


def dividir_documentos(documentos):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documentos)
    logger.info(f"✅ {len(chunks)} chunks generados")
    return chunks


def get_embeddings():
    return GoogleGenerativeAIEmbeddings(
        model=EMBED_MODEL,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )


def crear_vectorstore(chunks, persist_directory: str = CHROMA_DIR):
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=get_embeddings(),
        persist_directory=persist_directory
    )
    logger.info(f"✅ Vector store creado en '{persist_directory}'")
    return vectorstore


def cargar_vectorstore(persist_directory: str = CHROMA_DIR):
    return Chroma(
        persist_directory=persist_directory,
        embedding_function=get_embeddings()
    )


class RAG:
    def __init__(self, docs_dir: str = DOCS_DIR, chroma_dir: str = CHROMA_DIR):
        if os.path.exists(chroma_dir):
            logger.info("📂 Cargando vector store existente...")
            self.vectorstore = cargar_vectorstore(chroma_dir)
        else:
            logger.info("📂 Indexando documentos por primera vez...")
            documentos = cargar_documentos(docs_dir)
            chunks     = dividir_documentos(documentos)
            self.vectorstore = crear_vectorstore(chunks, chroma_dir)

        self.retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": TOP_K}
        )
        logger.info("🤖 RAG listo\n")

    def buscar(self, query: str) -> str:
        docs = self.retriever.invoke(query)
        if not docs:
            return ""
        fragmentos = []
        for i, doc in enumerate(docs, 1):
            fuente = doc.metadata.get("source", "desconocida")
            pagina = doc.metadata.get("page", "")
            ubicacion = f"p.{pagina}" if pagina != "" else "resumen"
            fragmentos.append(f"[Fragmento {i} | {fuente} {ubicacion}]\n{doc.page_content}")
        return "\n\n".join(fragmentos)

    def reindexar(self, docs_dir: str = DOCS_DIR, chroma_dir: str = CHROMA_DIR):
        documentos = cargar_documentos(docs_dir)
        chunks     = dividir_documentos(documentos)
        self.vectorstore = crear_vectorstore(chunks, chroma_dir)
        self.retriever   = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": TOP_K}
        )
        logger.info("🔄 Re-indexación completada")