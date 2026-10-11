# CloudShield AI - Architecture Documentation

## System Overview

CloudShield AI is a modular framework for evaluating cryptographic algorithms and blockchain-based models in cloud computing environments. The system consists of five main components:

```
┌─────────────────────────────────────────────────────────────┐
│                      CloudShield AI                         │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌────────────┐  ┌────────────┐  ┌────────┐  │
│  │  Crypto  │  │ Blockchain │  │ Benchmarks │  │Security│  │
│  │  Module  │  │  Module    │  │  Module    │  │ Module │  │
│  └────┬─────┘  └─────┬──────┘  └─────┬──────┘  └────┬───┘  │
│       │              │               │               │      │
│       └──────────────┼───────────────┼───────────────┘      │
│                      ▼                                           │
│            ┌─────────────────┐                                 │
│            │ BenchmarkRunner │                                 │
│            │  (Orchestrator) │                                 │
│            └────────┬────────┘                                 │
│                     ▼                                           │
│            ┌─────────────────┐                                 │
│            │  Results/Output │                                 │
│            └─────────────────┘                                 │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Crypto Module (`src/crypto/`)

Provides implementations of cryptographic algorithms with performance tracking:

- **AES** (`aes.py`): Symmetric encryption with GCM, CBC, CTR modes
  - Key sizes: 128, 192, 256 bits
  - Authenticated encryption (GCM)
  - Performance timing for encryption/decryption

- **EdDSA** (`eddsa.py`): Asymmetric digital signatures
  - Curves: Ed25519 (128-bit security), Ed448 (224-bit security)
  - Deterministic signing (no per-signature randomness)
  - Side-channel resistant design

### 2. Blockchain Module (`src/blockchain/`)

Hyperledger Fabric integration for blockchain-based evaluation:

- **Network Management** (`hyperledger.py`):
  - Network setup with configurable organizations/peers
  - Docker Compose generation for Fabric deployment
  - Chaincode deployment and lifecycle management
  - Transaction invocation and querying

- **Simulated Operations** (for benchmarking without full Fabric):
  - Invoke transactions (state changes)
  - Query transactions (read-only)
  - Latency and throughput measurement

### 3. Benchmarks Module (`src/benchmarks/`)

Orchestrates and runs performance evaluations:

- **BenchmarkRunner** (`runner.py`):
  - Configurable benchmark parameters
  - Warmup iterations for JIT optimization
  - Multi-algorithm comparison
  - Results persistence (JSON + summary)
  - Comparative analysis generation

- **BenchmarkConfig**: Dataclass for all benchmark parameters

### 4. Security Module (`src/security/`)

Comprehensive security analysis:

- **SecurityAnalyzer** (`analysis.py`):
  - Algorithm-specific security findings
  - Severity classification (LOW/MEDIUM/HIGH/VERY_HIGH)
  - Compliance mapping (FIPS, GDPR, HIPAA, etc.)
  - Quantum resistance assessment
  - Recommendations generation

### 5. Cloud Module (`src/cloud/`)

Cloud deployment utilities (placeholder for future expansion):
- AWS/Azure/GCP deployment scripts
- Infrastructure as Code templates
- Monitoring and logging integration

## Data Flow

```
Configuration (config/settings.yaml)
         │
         ▼
┌────────────────────────┐
│   BenchmarkRunner      │
│  (Reads Config)        │
└───────────┬────────────┘
            │
    ┌───────┼───────┬─────────────┐
    ▼       ▼       ▼             ▼
  AES     EdDSA  Hyperledger   Security
Benchmark Benchmark Benchmark   Analysis
    │       │       │             │
    └───────┼───────┼─────────────┘
            ▼
    ┌───────────────┐
    │ Comparative   │
    │ Analysis      │
    └───────┬───────┘
            ▼
    ┌───────────────┐
    │ Results Output│
    │ (JSON, TXT)   │
    └───────────────┘
```

## Configuration

All settings in `config/settings.yaml`:

- Cloud provider credentials and region
- Benchmark parameters (iterations, data sizes, concurrency)
- Algorithm-specific settings (key sizes, curves, modes)
- Security thresholds
- Output formats and directories

## Extending the Framework

### Adding New Algorithms

1. Create new module in `src/crypto/` (e.g., `chacha20.py`)
2. Implement cipher class with `encrypt()`/`decrypt()` or `sign()`/`verify()`
3. Add benchmark function
4. Register in `src/crypto/__init__.py`
5. Add security analysis in `SecurityAnalyzer`

### Adding New Blockchain Platforms

1. Create new module in `src/blockchain/`
2. Implement network management class
3. Add benchmark functions
4. Register in `src/blockchain/__init__.py`

### Custom Benchmarks

Extend `BenchmarkConfig` with new parameters and modify `BenchmarkRunner` to include new benchmark functions.

## Performance Considerations

- Warmup iterations reduce JIT compilation noise
- Multiple data sizes show scaling behavior
- Concurrency levels test parallel performance
- Results include min/max/avg for statistical validity
- Throughput calculated as MB/s or operations/sec

## Security Considerations

- Keys generated using OS CSPRNG (`os.urandom`)
- No hardcoded secrets or keys
- Constant-time operations where possible
- Side-channel resistance documented
- Quantum resistance assessed per algorithm