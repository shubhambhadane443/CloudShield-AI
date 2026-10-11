# CloudShield AI: Performance and Security Evaluation of AES, EDDSA, and Hyperledger-based Models in Cloud Computing

## Overview
CloudShield AI is a comprehensive evaluation framework for comparing cryptographic algorithms (AES, EdDSA) and blockchain-based models (Hyperledger) in cloud computing environments. The project provides performance benchmarks, security analysis, and comparative metrics.

## Features
- **AES Evaluation**: Symmetric encryption performance and security analysis
- **EdDSA Evaluation**: Asymmetric signature scheme performance and security analysis
- **Hyperledger Fabric Evaluation**: Blockchain-based model performance in cloud deployments
- **Comparative Analysis**: Cross-algorithm performance and security metrics
- **Cloud Integration**: Deployment scripts for major cloud providers

## Project Structure
```
CloudShield AI/
├── src/                    # Source code
│   ├── crypto/            # Cryptographic implementations
│   ├── blockchain/        # Hyperledger integration
│   ├── benchmarks/        # Performance benchmarking
│   ├── security/          # Security analysis modules
│   └── cloud/             # Cloud deployment utilities
├── tests/                 # Test suites
├── docs/                  # Documentation
├── config/                # Configuration files
├── scripts/               # Deployment and utility scripts
└── data/                  # Benchmark data and results
```

## Requirements
- Python 3.9+
- Hyperledger Fabric 2.5+
- Docker & Docker Compose
- Cloud CLI tools (AWS CLI, Azure CLI, or GCP CLI)

## Installation
```bash
pip install -r requirements.txt
```

## Quick Start
```bash
# Run AES benchmarks
python src/benchmarks/aes_benchmark.py

# Run EdDSA benchmarks
python src/benchmarks/eddsa_benchmark.py

# Run Hyperledger benchmarks
python src/benchmarks/hyperledger_benchmark.py

# Generate comparative report
python src/benchmarks/comparative_analysis.py
```

## Configuration
Edit `config/settings.yaml` to configure:
- Cloud provider credentials
- Benchmark parameters
- Security analysis thresholds
- Output formats

## Documentation
- [Architecture](docs/architecture.md)
- [API Reference](docs/api_reference.md)
- [Benchmark Methodology](docs/benchmark_methodology.md)
- [Security Analysis](docs/security_analysis.md)

## License
MIT License - see LICENSE file for details