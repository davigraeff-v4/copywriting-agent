"""Reuse installed FastEmbed and cached ONNX model; queries never go to an API."""
import os
from pathlib import Path
from rag_config import MODEL,FASTEMBED_VERSION,MAX_TOKENS
MODEL_CACHE={}
SIGNATURE_CACHE={}
DEFAULT_CACHE_DIR=Path(__file__).resolve().parents[1]/'.local'/'fastembed-cache'

def resolve_cache_dir(cache_dir=None):
    """Use a persistent project default, with explicit caller/env overrides."""
    configured=cache_dir if cache_dir is not None else os.environ.get('FASTEMBED_CACHE_PATH') or DEFAULT_CACHE_DIR
    return Path(configured).expanduser().resolve()

def load_model(cache_dir=None):
    import fastembed
    if fastembed.__version__!=FASTEMBED_VERSION:raise RuntimeError('embedding engine version mismatch')
    cache_dir=resolve_cache_dir(cache_dir)
    key=str(cache_dir)
    if key not in MODEL_CACHE:
        from fastembed import TextEmbedding
        model=TextEmbedding(model_name=MODEL,cache_dir=str(cache_dir),local_files_only=True,threads=2)
        if model.model.tokenizer.truncation['max_length']!=MAX_TOKENS:raise RuntimeError('embedding token limit mismatch')
        MODEL_CACHE[key]=model
    return MODEL_CACHE[key]

def counting_tokenizer(model):
    from tokenizers import Tokenizer
    tokenizer=Tokenizer.from_str(model.model.tokenizer.to_str());tokenizer.no_truncation()
    return tokenizer

def model_signature(model):
    import hashlib
    folder=Path(model.model._model_dir)
    key=str(folder)
    if key not in SIGNATURE_CACHE:
        names=['model_optimized.onnx','config.json','tokenizer.json','tokenizer_config.json','special_tokens_map.json']
        SIGNATURE_CACHE[key]={name:hashlib.sha256((folder/name).read_bytes()).hexdigest() for name in names}
    return SIGNATURE_CACHE[key]
