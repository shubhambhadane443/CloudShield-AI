# CloudShield AI - API Reference

## Core Modules

### `cloudshield.crypto.aes`

#### `AESCipher`

```python
class AESCipher:
    def __init__(self, key_size: int = 256, mode: str = "GCM"):
        """
        Initialize AES cipher.
        
        Args:
            key_size: Key size in bits (128, 192, or 256)
            mode: Encryption mode ("GCM", "CBC", or "CTR")
        
        Raises:
            ValueError: If key_size or mode not supported
        """
    
    def encrypt(self, plaintext: bytes, associated_data: bytes = b"") -> AESResult:
        """
        Encrypt plaintext.
        
        Args:
            plaintext: Data to encrypt
            associated_data: Additional authenticated data (GCM only)
        
        Returns:
            AESResult with ciphertext, IV, tag, and timing
        """
    
    def decrypt(self, ciphertext: bytes, iv: bytes, tag: Optional[bytes],
                associated_data: bytes = b"") -> bytes:
        """
        Decrypt ciphertext.
        
        Args:
            ciphertext: Encrypted data
            iv: Initialization vector
            tag: Authentication tag (GCM only)
            associated_data: Additional authenticated data (GCM only)
        
        Returns:
            Decrypted plaintext
        
        Raises:
            InvalidTag: If authentication fails (GCM)
        """
    
    @staticmethod
    def generate_key(key_size: int) -> bytes:
        """Generate random AES key."""
    
    def get_key(self) -> bytes:
        """Get current encryption key."""
```

#### `AESResult`

```python
@dataclass
class AESResult:
    ciphertext: bytes          # Encrypted data
    iv: bytes                  # Initialization vector
    tag: Optional[bytes]       # Auth tag (GCM) or None
    encryption_time: float     # Seconds
    decryption_time: float     # Seconds
    key_size: int              # Key size in bits
    mode: str                  # Encryption mode
    data_size: int             # Plaintext size in bytes
```

#### `benchmark_aes`

```python
def benchmark_aes(data_sizes: list, key_sizes: list, modes: list,
                  iterations: int = 1000) -> Dict[str, Any]:
    """
    Run AES benchmarks.
    
    Args:
        data_sizes: List of data sizes in bytes
        key_sizes: List of key sizes (128, 192, 256)
        modes: List of modes ("GCM", "CBC", "CTR")
        iterations: Benchmark iterations per configuration
    
    Returns:
        Dict with results keyed by "aes_{key_size}_{mode}"
    """
```

---

### `cloudshield.crypto.eddsa`

#### `EdDSACipher`

```python
class EdDSACipher:
    def __init__(self, curve: str = "Ed25519"):
        """
        Initialize EdDSA signer/verifier.
        
        Args:
            curve: Curve name ("Ed25519" or "Ed448")
        
        Raises:
            ValueError: If curve not supported
        """
    
    def sign(self, message: bytes) -> EdDSAResult:
        """
        Sign message.
        
        Args:
            message: Message to sign
        
        Returns:
            EdDSAResult with signature and timing
        """
    
    def verify(self, message: bytes, signature: bytes) -> bool:
        """
        Verify signature.
        
        Args:
            message: Original message
            signature: Signature to verify
        
        Returns:
            True if valid, False otherwise
        """
    
    def get_public_key_bytes(self) -> bytes:
        """Get public key as raw bytes."""
    
    def get_private_key_bytes(self) -> bytes:
        """Get private key as raw bytes."""
    
    @staticmethod
    def generate_keypair(curve: str = "Ed25519") -> Tuple[bytes, bytes]:
        """
        Generate new keypair.
        
        Returns:
            Tuple of (private_key_bytes, public_key_bytes)
        """
    
    @staticmethod
    def load_private_key(private_key_bytes: bytes, curve: str = "Ed25519"):
        """Load private key from bytes."""
```

#### `EdDSAResult`

```python
@dataclass
class EdDSAResult:
    signature: bytes           # Signature bytes
    signing_time: float        # Seconds
    verification_time: float   # Seconds
    curve: str                 # Curve name
    message_size: int          # Message size in bytes
    public_key_size: int       # Public key size in bytes
    private_key_size: int      # Private key size in bytes
    signature_size: int        # Signature size in bytes
```

#### `benchmark_eddsa`

```python
def benchmark_eddsa(message_sizes: list, curves: list,
                    iterations: int = 1000) -> Dict[str, Any]:
    """
    Run EdDSA benchmarks.
    
    Args:
        message_sizes: List of message sizes in bytes
        curves: List of curves ("Ed25519", "Ed448")
        iterations: Benchmark iterations per configuration
    
    Returns:
        Dict with results keyed by "eddsa_{curve}"
    """
```

---

### `cloudshield.blockchain.hyperledger`

#### `HyperledgerNetwork`

```python
class HyperledgerNetwork:
    def __init__(self, config_path: str = "config/settings.yaml"):
        """Initialize with config path."""
    
    def setup_network(self, orgs: int = 3, peers_per_org: int = 2) -> HyperledgerResult:
        """
        Set up Fabric network (generates crypto, config, docker-compose).
        
        Returns:
            HyperledgerResult with success status and timing
        """
    
    def start_network(self) -> HyperledgerResult:
        """Start network via Docker Compose."""
    
    def deploy_chaincode(self, chaincode_path: str, name: str, 
                         version: str) -> HyperledgerResult:
        """Deploy chaincode to network."""
    
    def invoke_transaction(self, chaincode_name: str, function: str,
                          args: List[str]) -> HyperledgerResult:
        """Invoke chaincode transaction (state change)."""
    
    def query_transaction(self, chaincode_name: str, function: str,
                         args: List[str]) -> HyperledgerResult:
        """Query chaincode state (read-only)."""
    
    def shutdown_network(self) -> HyperledgerResult:
        """Shutdown network."""
```

#### `HyperledgerResult`

```python
@dataclass
class HyperledgerResult:
    operation: str             # Operation name
    success: bool              # Success status
    latency_ms: float          # Operation latency in ms
    throughput_tps: float      # Throughput in TPS
    block_height: int          # Current block height
    error: Optional[str]       # Error message if failed
```

#### `benchmark_hyperledger`

```python
def benchmark_hyperledger(operations: List[str], iterations: int = 100) 
    -> Dict[str, Any]:
    """
    Run Hyperledger benchmarks.
    
    Args:
        operations: List of operations ("invoke", "query")
        iterations: Iterations per operation
    
    Returns:
        Dict with results per operation
    """
```

---

### `cloudshield.benchmarks.runner`

#### `BenchmarkConfig`

```python
@dataclass
class BenchmarkConfig:
    iterations: int = 1000              # Benchmark iterations
    warmup_iterations: int = 100        # Warmup iterations
    data_sizes: List[int] = [...]       # AES data sizes
    message_sizes: List[int] = [...]    # EdDSA message sizes
    aes_key_sizes: List[int] = [128, 192, 256]
    aes_modes: List[str] = ["GCM", "CBC", "CTR"]
    eddsa_curves: List[str] = ["Ed25519", "Ed448"]
    hl_operations: List[str] = ["invoke", "query"]
    hl_iterations: int = 100
```

#### `BenchmarkRunner`

```python
class BenchmarkRunner:
    def __init__(self, config: BenchmarkConfig = None, 
                 output_dir: str = "./data/results"):
        """Initialize runner with config and output directory."""
    
    def run_all_benchmarks(self) -> Dict[str, Any]:
        """
        Run all benchmarks: AES, EdDSA, Hyperledger, Security.
        
        Returns:
            Complete results dictionary
        """
```

---

### `cloudshield.security.analysis`

#### `SecurityAnalyzer`

```python
class SecurityAnalyzer:
    def analyze_aes_security(self) -> Dict[str, Any]:
        """Analyze AES security posture."""
    
    def analyze_eddsa_security(self) -> Dict[str, Any]:
        """Analyze EdDSA security posture."""
    
    def analyze_hyperledger_security(self) -> Dict[str, Any]:
        """Analyze Hyperledger Fabric security posture."""
    
    def get_all_findings(self) -> List[SecurityFinding]:
        """Get all security findings."""
    
    def get_critical_findings(self) -> List[SecurityFinding]:
        """Get HIGH/VERY_HIGH severity findings only."""
```

#### `SecurityFinding`

```python
@dataclass
class SecurityFinding:
    category: str              # Finding category
    severity: SecurityLevel    # Severity level
    description: str           # Detailed description
    recommendation: str        # Mitigation recommendation
    references: List[str]      # Reference links/docs
```

#### `SecurityLevel`

```python
class SecurityLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"
```

---

## CLI Reference

### `cloudshield.py`

```bash
# Run full benchmarks
python cloudshield.py benchmark

# Run quick benchmarks
python cloudshield.py benchmark --quick

# Run with custom iterations
python cloudshield.py benchmark --iterations 500

# Run security analysis only
python cloudshield.py security

# Show help
python cloudshield.py --help
```

---

## Configuration Reference

### `config/settings.yaml`

```yaml
# Cloud provider
cloud:
  provider: "aws"           # aws, azure, gcp
  region: "us-east-1"

# Benchmark parameters
benchmark:
  iterations: 1000
  warmup_iterations: 100
  data_sizes: [1024, 10240, 102400, 1048576, 10485760]
  concurrency_levels: [1, 4, 8, 16, 32]

# AES settings
aes:
  key_sizes: [128, 192, 256]
  modes: ["GCM", "CBC", "CTR"]
  iv_size: 12

# EdDSA settings
eddsa:
  curves: ["Ed25519", "Ed448"]
  hash_algorithms: ["SHA-512", "SHAKE256"]

# Hyperledger settings
hyperledger:
  fabric_version: "2.5"
  network:
    organizations: 3
    peers_per_org: 2
    orderers: 3
  consensus: "etcdraft"

# Security thresholds
security:
  aes:
    min_key_size: 128
    recommended_key_size: 256
  eddsa:
    min_curve_security: 128

# Output settings
output:
  format: "json"
  directory: "./data/results"
  generate_plots: true
```

---

## Usage Examples

### Basic AES Encryption

```python
from cloudshield.crypto.aes import AESCipher

cipher = AESCipher(key_size=256, mode="GCM")
plaintext = b"Sensitive data"

result = cipher.encrypt(plaintext)
print(f"Encrypted in {result.encryption_time*1000:.2f} ms")
print(f"Throughput: {len(plaintext)/1024/1024/result.encryption_time:.2f} MB/s")

# Decrypt
decrypted = cipher.decrypt(result.ciphertext, result.iv, result.tag)
assert decrypted == plaintext
```

### EdDSA Signing

```python
from cloudshield.crypto.eddsa import EdDSACipher

cipher = EdDSACipher(curve="Ed25519")
message = b"Document to sign"

result = cipher.sign(message)
print(f"Signed in {result.signing_time*1000:.2f} ms")
print(f"Signature: {result.signature.hex()}")

# Verify
valid = cipher.verify(message, result.signature)
print(f"Valid: {valid}")
```

### Running Benchmarks

```python
from cloudshield.benchmarks.runner import BenchmarkRunner, BenchmarkConfig

config = BenchmarkConfig(iterations=100)
runner = BenchmarkRunner(config)
results = runner.run_all_benchmarks()

# Access results
print(results["aes"]["aes_256_GCM"][1048576]["avg_encryption_ms"])
print(results["eddsa"]["eddsa_Ed25519"][1024]["avg_signing_ms"])
```

### Security Analysis

```python
from cloudshield.security.analysis import SecurityAnalyzer

analyzer = SecurityAnalyzer()

# Get all findings
aes_security = analyzer.analyze_aes_security()
for finding in aes_security["findings"]:
    print(f"[{finding['severity']}] {finding['category']}: {finding['description']}")

# Get critical findings only
critical = analyzer.get_critical_findings()
for finding in critical:
    print(f"CRITICAL: {finding['category']} - {finding['recommendation']}")
```