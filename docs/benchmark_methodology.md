# CloudShield AI - Benchmark Methodology

## Overview

This document describes the methodology used for performance benchmarking and security evaluation in CloudShield AI. The benchmarks are designed to provide fair, reproducible, and meaningful comparisons between cryptographic algorithms and blockchain models.

## Benchmark Principles

### 1. Reproducibility
- Fixed random seeds where applicable
- Warmup iterations to stabilize JIT compilation
- Multiple iterations for statistical significance
- Environment documentation (Python version, OS, hardware)

### 2. Fairness
- Same data sizes across algorithms where comparable
- Identical iteration counts for similar operations
- Comparable security levels (e.g., AES-256 vs Ed25519 both ~128-bit classical)
- Real-world usage patterns (encryption + decryption, sign + verify)

### 3. Comprehensiveness
- Multiple data/message sizes
- Multiple key sizes and curves
- Multiple modes of operation
- Concurrency testing
- Security analysis alongside performance

## AES Benchmarks

### Test Parameters
| Parameter | Values |
|-----------|--------|
| Key Sizes | 128, 192, 256 bits |
| Modes | GCM, CBC, CTR |
| Data Sizes | 1 KB, 10 KB, 100 KB, 1 MB, 10 MB |
| Iterations | 1,000 (default) |
| Warmup | 100 iterations |

### Metrics Collected
- **Encryption Time**: Wall-clock time for encryption operation
- **Decryption Time**: Wall-clock time for decryption operation
- **Throughput**: MB/s = (data_size / 1024 / 1024) / avg_time
- **Min/Max Latency**: Outlier detection

### Mode-Specific Notes
- **GCM**: Includes authentication tag generation/verification
- **CBC**: Includes PKCS7 padding overhead
- **CTR**: Stream mode, no padding overhead

### Real-World Considerations
- IV generation included in timing (12 bytes for GCM, 16 for CBC/CTR)
- Key setup not included (assumes persistent keys)
- Associated data authentication for GCM (empty in benchmarks)

## EdDSA Benchmarks

### Test Parameters
| Parameter | Values |
|-----------|--------|
| Curves | Ed25519, Ed448 |
| Message Sizes | 32, 64, 128, 256, 512, 1024 bytes |
| Iterations | 1,000 (default) |
| Warmup | 100 iterations |

### Metrics Collected
- **Signing Time**: Time to generate signature
- **Verification Time**: Time to verify signature
- **Signatures/Second**: 1 / avg_signing_time
- **Key Sizes**: Public/private key and signature sizes

### Curve Characteristics
- **Ed25519**: 32-byte keys, 64-byte signatures, ~128-bit security
- **Ed448**: 57-byte keys, 114-byte signatures, ~224-bit security

### Real-World Considerations
- Deterministic signing (no entropy per signature)
- No separate hash step (built into EdDSA)
- Point decompression validation included

## Hyperledger Fabric Benchmarks

### Test Parameters
| Parameter | Values |
|-----------|--------|
| Operations | Invoke, Query |
| Iterations | 100 (default) |
| Network | 3 orgs, 2 peers/org, 3 orderers (Raft) |
| Chaincode | Simple key-value store |

### Metrics Collected
- **Latency**: End-to-end transaction time (ms)
- **Throughput**: Transactions per second (TPS)
- **Success Rate**: Successful transactions / total

### Network Configuration
- Consensus: Raft (crash fault tolerant)
- TLS: Enabled for all communication
- Endorsement: AND policy (2 orgs required)
- Block size: 10 MB max
- Block timeout: 2 seconds

### Limitations (Simulation Mode)
Current benchmarks simulate Fabric operations without full network deployment:
- Network setup/teardown: ~100ms simulated
- Chaincode deployment: ~50ms simulated
- Invoke: ~10ms simulated latency
- Query: ~5ms simulated latency

For production benchmarks, deploy actual Fabric network using:
```bash
# Generate crypto material
cryptogen generate --config=network/crypto-config.yaml

# Generate genesis block
configtxgen -profile OrdererGenesis -outputBlock network/channel-artifacts/genesis.block

# Generate channel config
configtxgen -profile Channel -outputCreateChannelTx network/channel-artifacts/channel.tx

# Start network
docker-compose -f network/docker-compose.yaml up -d
```

## Security Analysis Methodology

### Finding Classification

| Severity | Criteria |
|----------|----------|
| VERY_HIGH | Fundamental design flaw, immediate exploitation risk |
| HIGH | Significant vulnerability, practical exploitation possible |
| MEDIUM | Theoretical weakness, requires specific conditions |
| LOW | Informational, long-term consideration |

### Analysis Categories

1. **Key Management**: Generation, storage, rotation, destruction
2. **Algorithm Selection**: Appropriate use of primitives
3. **Implementation**: Side-channels, constant-time, validation
4. **Protocol**: Nonce reuse, replay, downgrade attacks
5. **Quantum Resistance**: Post-quantum security assessment
6. **Compliance**: Standards adherence (FIPS, GDPR, etc.)

### Quantum Security Assessment

| Algorithm | Classical Security | Quantum Security (Grover/Shor) | Recommendation |
|-----------|-------------------|-------------------------------|----------------|
| AES-128 | 128-bit | 64-bit (Grover) | Legacy only |
| AES-192 | 192-bit | 96-bit (Grover) | Transitioning |
| AES-256 | 256-bit | 128-bit (Grover) | **Preferred** |
| Ed25519 | 128-bit | 0-bit (Shor) | Migrate for long-term |
| Ed448 | 224-bit | 0-bit (Shor) | Migrate for long-term |
| Fabric ECDSA | 128-bit | 0-bit (Shor) | Monitor PQC standards |

## Statistical Rigor

### Iteration Counts
- Minimum 100 iterations for microbenchmarks
- Minimum 1000 for stable averages
- Warmup iterations excluded from statistics

### Outlier Handling
- Min/max reported alongside average
- Consider median for skewed distributions
- Coefficient of variation for consistency check

### Confidence
- Standard deviation available in raw data
- Percentiles (p50, p95, p99) for latency analysis
- Sample size justification in results

## Environment Specification

### Required Documentation
For each benchmark run, record:

```
Platform: Windows/Linux/macOS
Python Version: 3.x.x
CPU: Model, cores, frequency
Memory: Amount, speed
Storage: Type (SSD/HDD), available space
Libraries: OpenSSL version, cryptography backend
```

### Cloud Environment
When running in cloud:
- Instance type (e.g., AWS c6i.xlarge)
- Region/AZ
- Network configuration
- Shared vs dedicated tenancy

## Result Interpretation

### Performance Comparison Guidelines

1. **Throughput vs Latency**: Different use cases prioritize differently
   - Bulk encryption: Maximize throughput (MB/s)
   - Real-time signing: Minimize latency (ms)

2. **Security vs Performance Trade-offs**
   - AES-256-GCM: Best balance for most cloud storage
   - AES-128-GCM: Acceptable for low-value data
   - Ed25519: Best signature performance/security ratio
   - Ed448: When 224-bit security margin required

3. **Blockchain Overhead**
   - Fabric adds 10-50ms latency vs centralized DB
   - TPS limited by consensus (100-1000 typical)
   - Justified by audit trail, multi-party trust

### When to Use Each

| Use Case | Recommended |
|----------|-------------|
| Cloud data encryption | AES-256-GCM |
| API authentication | Ed25519 signatures |
| Document signing | Ed25519 |
| Long-term archival | Ed448 + AES-256 |
| Multi-party audit log | Hyperledger Fabric |
| High-throughput cache | AES-128-CTR |
| Regulated data (HIPAA) | AES-256-GCM + Fabric |

## Validation

### Cross-Validation
- Compare with OpenSSL speed benchmarks
- Verify against cryptography library benchmarks
- Cross-reference with academic literature

### Regression Testing
- CI/CD runs benchmarks on each commit
- Alert on >10% performance regression
- Track trends over time

## Reporting

### Standard Outputs
1. **JSON Results**: Machine-readable, all raw data
2. **Text Summary**: Human-readable key metrics
3. **Comparative Analysis**: Cross-algorithm insights
4. **Security Report**: Findings and recommendations

### Visualization (Future)
- Latency distributions (histograms)
- Throughput vs data size (line charts)
- Security vs performance (scatter plots)
- Radar charts for multi-dimensional comparison