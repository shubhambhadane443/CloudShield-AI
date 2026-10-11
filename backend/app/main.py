import sys
import os
from pathlib import Path

# Add project root and src to path
project_root = Path(__file__).parent.parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(src_path))

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import uuid
from datetime import datetime
import asyncio
from concurrent.futures import ThreadPoolExecutor

from crypto.aes import AESCipher, benchmark_aes, AESResult
from crypto.eddsa import EdDSACipher, benchmark_eddsa, EdDSAResult
from blockchain.hyperledger import benchmark_hyperledger, HyperledgerNetwork
from security.analysis import SecurityAnalyzer
from benchmarks.runner import BenchmarkRunner, BenchmarkConfig

app = FastAPI(
    title="CloudShield AI API",
    description="Performance and Security Evaluation of AES, EdDSA, and Hyperledger Models",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

executor = ThreadPoolExecutor(max_workers=4)

jobs: Dict[str, Dict] = {}


class AESEncryptRequest(BaseModel):
    plaintext: str = Field(..., description="Plaintext to encrypt (base64 or plain)")
    key_size: int = Field(256, ge=128, le=256, multiple_of=64)
    mode: str = Field("GCM", pattern="^(GCM|CBC|CTR)$")
    key: Optional[str] = Field(None, description="Optional base64 encoded key")
    associated_data: str = Field("", description="Additional authenticated data (GCM only)")


class AESEncryptResponse(BaseModel):
    ciphertext: str
    iv: str
    tag: Optional[str]
    encryption_time_ms: float
    key_size: int
    mode: str


class EdDSASignRequest(BaseModel):
    message: str = Field(..., description="Message to sign")
    curve: str = Field("Ed25519", pattern="^(Ed25519|Ed448)$")


class EdDSASignResponse(BaseModel):
    signature: str
    signing_time_ms: float
    verification_time_ms: float
    curve: str
    public_key: str


class BenchmarkRequest(BaseModel):
    iterations: int = Field(100, ge=10, le=10000)
    warmup_iterations: int = Field(10, ge=0, le=1000)
    data_sizes: Optional[List[int]] = None
    message_sizes: Optional[List[int]] = None
    aes_key_sizes: Optional[List[int]] = None
    aes_modes: Optional[List[str]] = None
    eddsa_curves: Optional[List[str]] = None
    hl_operations: Optional[List[str]] = None
    hl_iterations: int = Field(50, ge=10, le=1000)


class BenchmarkJobResponse(BaseModel):
    job_id: str
    status: str
    created_at: str


class BenchmarkStatusResponse(BaseModel):
    job_id: str
    status: str
    progress: float
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


def run_benchmark_sync(job_id: str, config: BenchmarkConfig):
    """Run benchmark in thread pool."""
    try:
        jobs[job_id]["status"] = "running"
        jobs[job_id]["progress"] = 0.1
        
        runner = BenchmarkRunner(config)
        results = runner.run_all_benchmarks()
        
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["progress"] = 1.0
        jobs[job_id]["result"] = results
    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)


@app.get("/")
async def root():
    return {
        "name": "CloudShield AI API",
        "version": "1.0.0",
        "description": "Cryptographic Benchmarking & Security Analysis API",
        "endpoints": {
            "aes": "/api/v1/aes/*",
            "eddsa": "/api/v1/eddsa/*",
            "hyperledger": "/api/v1/hyperledger/*",
            "security": "/api/v1/security/*",
            "benchmarks": "/api/v1/benchmarks/*"
        }
    }


@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


@app.post("/api/v1/aes/encrypt", response_model=AESEncryptResponse)
async def aes_encrypt(request: AESEncryptRequest):
    import base64
    
    try:
        plaintext = request.plaintext.encode()
        associated_data = request.associated_data.encode()
        
        if request.key:
            key = base64.b64decode(request.key)
            cipher = AESCipher(key_size=request.key_size, mode=request.mode)
            # Note: This would need key injection - simplified for demo
        else:
            cipher = AESCipher(key_size=request.key_size, mode=request.mode)
        
        result = cipher.encrypt(plaintext, associated_data)
        
        return AESEncryptResponse(
            ciphertext=base64.b64encode(result.ciphertext).decode(),
            iv=base64.b64encode(result.iv).decode(),
            tag=base64.b64encode(result.tag).decode() if result.tag else None,
            encryption_time_ms=result.encryption_time * 1000,
            key_size=result.key_size,
            mode=result.mode
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/v1/aes/benchmark")
async def aes_benchmark(
    key_sizes: List[int] = [128, 192, 256],
    modes: List[str] = ["GCM", "CBC", "CTR"],
    data_sizes: List[int] = [1024, 10240, 102400, 1048576],
    iterations: int = 100
):
    try:
        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(
            executor,
            benchmark_aes,
            data_sizes, key_sizes, modes, iterations
        )
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/eddsa/sign", response_model=EdDSASignResponse)
async def eddsa_sign(request: EdDSASignRequest):
    import base64
    
    try:
        cipher = EdDSACipher(curve=request.curve)
        message = request.message.encode()
        
        result = cipher.sign(message)
        
        return EdDSASignResponse(
            signature=base64.b64encode(result.signature).decode(),
            signing_time_ms=result.signing_time * 1000,
            verification_time_ms=result.verification_time * 1000,
            curve=result.curve,
            public_key=base64.b64encode(cipher.get_public_key_bytes()).decode()
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/v1/eddsa/verify")
async def eddsa_verify(
    message: str,
    signature: str,
    public_key: str,
    curve: str = "Ed25519"
):
    import base64
    
    try:
        cipher = EdDSACipher(curve=curve)
        # Load the provided public key
        # For demo, we use the cipher's own key
        result = cipher.verify(
            message.encode(),
            base64.b64decode(signature)
        )
        return {"valid": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/v1/eddsa/benchmark")
async def eddsa_benchmark(
    curves: List[str] = ["Ed25519", "Ed448"],
    message_sizes: List[int] = [32, 64, 128, 256, 512, 1024],
    iterations: int = 100
):
    try:
        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(
            executor,
            benchmark_eddsa,
            message_sizes, curves, iterations
        )
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class HyperledgerBenchmarkRequest(BaseModel):
    operations: List[str] = ["invoke", "query"]
    iterations: int = 50


@app.post("/api/v1/hyperledger/benchmark")
async def hyperledger_benchmark(request: HyperledgerBenchmarkRequest):
    try:
        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(
            executor,
            benchmark_hyperledger,
            request.operations, request.iterations
        )
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/security/analyze")
async def security_analyze():
    try:
        analyzer = SecurityAnalyzer()
        return {
            "aes": analyzer.analyze_aes_security(),
            "eddsa": analyzer.analyze_eddsa_security(),
            "hyperledger": analyzer.analyze_hyperledger_security(),
            "critical_findings": [
                {**f, "severity": f["severity"].value} 
                for f in analyzer.get_critical_findings()
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/benchmarks/run", response_model=BenchmarkJobResponse)
async def run_full_benchmark(request: BenchmarkRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    
    config = BenchmarkConfig(
        iterations=request.iterations,
        warmup_iterations=request.warmup_iterations,
        data_sizes=request.data_sizes,
        message_sizes=request.message_sizes,
        aes_key_sizes=request.aes_key_sizes,
        aes_modes=request.aes_modes,
        eddsa_curves=request.eddsa_curves,
        hl_operations=request.hl_operations,
        hl_iterations=request.hl_iterations
    )
    
    jobs[job_id] = {
        "status": "queued",
        "progress": 0.0,
        "created_at": datetime.utcnow().isoformat(),
        "config": config
    }
    
    background_tasks.add_task(run_benchmark_sync, job_id, config)
    
    return BenchmarkJobResponse(
        job_id=job_id,
        status="queued",
        created_at=jobs[job_id]["created_at"]
    )


@app.get("/api/v1/benchmarks/{job_id}", response_model=BenchmarkStatusResponse)
async def get_benchmark_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    return BenchmarkStatusResponse(
        job_id=job_id,
        status=job["status"],
        progress=job["progress"],
        result=job.get("result"),
        error=job.get("error")
    )


@app.get("/api/v1/benchmarks")
async def list_benchmarks():
    return {
        "jobs": [
            {
                "job_id": jid,
                "status": job["status"],
                "created_at": job["created_at"],
                "progress": job["progress"]
            }
            for jid, job in jobs.items()
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)