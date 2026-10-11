"""
CloudShield AI - Benchmark Runner
Orchestrates benchmarks for all cryptographic algorithms.
"""

import json
import time
from typing import Dict, Any, List
from pathlib import Path
from dataclasses import dataclass, asdict

from src.crypto.aes import AESCipher, benchmark_aes
from src.crypto.eddsa import EdDSACipher, benchmark_eddsa
from src.blockchain.hyperledger import benchmark_hyperledger
from src.security.analysis import SecurityAnalyzer


@dataclass
class BenchmarkConfig:
    """Configuration for benchmark runs."""
    iterations: int = 1000
    warmup_iterations: int = 100
    data_sizes: List[int] = None
    message_sizes: List[int] = None
    aes_key_sizes: List[int] = None
    aes_modes: List[str] = None
    eddsa_curves: List[str] = None
    hl_operations: List[str] = None
    hl_iterations: int = 100
    
    def __post_init__(self):
        if self.data_sizes is None:
            self.data_sizes = [1024, 10240, 102400, 1048576, 10485760]
        if self.message_sizes is None:
            self.message_sizes = [32, 64, 128, 256, 512, 1024]
        if self.aes_key_sizes is None:
            self.aes_key_sizes = [128, 192, 256]
        if self.aes_modes is None:
            self.aes_modes = ["GCM", "CBC", "CTR"]
        if self.eddsa_curves is None:
            self.eddsa_curves = ["Ed25519", "Ed448"]
        if self.hl_operations is None:
            self.hl_operations = ["invoke", "query"]


class BenchmarkRunner:
    """Main benchmark orchestration class."""
    
    def __init__(self, config: BenchmarkConfig = None, output_dir: str = "./data/results"):
        self.config = config or BenchmarkConfig()
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.results = {}
        self.security_analyzer = SecurityAnalyzer()
    
    def run_all_benchmarks(self) -> Dict[str, Any]:
        """Run all benchmarks and return combined results."""
        print("Starting CloudShield AI Benchmarks...")
        print("=" * 50)
        
        # Run AES benchmarks
        print("\n1. Running AES Benchmarks...")
        self.results["aes"] = self._run_aes_benchmarks()
        
        # Run EdDSA benchmarks
        print("\n2. Running EdDSA Benchmarks...")
        self.results["eddsa"] = self._run_eddsa_benchmarks()
        
        # Run Hyperledger benchmarks
        print("\n3. Running Hyperledger Benchmarks...")
        self.results["hyperledger"] = self._run_hyperledger_benchmarks()
        
        # Run security analysis
        print("\n4. Running Security Analysis...")
        self.results["security"] = self._run_security_analysis()
        
        # Generate comparative analysis
        print("\n5. Generating Comparative Analysis...")
        self.results["comparative"] = self._generate_comparative_analysis()
        
        # Save results
        self._save_results()
        
        print("\n" + "=" * 50)
        print("All benchmarks completed!")
        return self.results
    
    def _run_aes_benchmarks(self) -> Dict[str, Any]:
        """Run AES benchmarks with warmup."""
        # Warmup
        cipher = AESCipher(key_size=256, mode="GCM")
        for _ in range(self.config.warmup_iterations):
            cipher.encrypt(b"warmup" * 100)
        
        # Actual benchmarks
        return benchmark_aes(
            data_sizes=self.config.data_sizes,
            key_sizes=self.config.aes_key_sizes,
            modes=self.config.aes_modes,
            iterations=self.config.iterations
        )
    
    def _run_eddsa_benchmarks(self) -> Dict[str, Any]:
        """Run EdDSA benchmarks with warmup."""
        # Warmup
        cipher = EdDSACipher(curve="Ed25519")
        for _ in range(self.config.warmup_iterations):
            cipher.sign(b"warmup" * 10)
        
        # Actual benchmarks
        return benchmark_eddsa(
            message_sizes=self.config.message_sizes,
            curves=self.config.eddsa_curves,
            iterations=self.config.iterations
        )
    
    def _run_hyperledger_benchmarks(self) -> Dict[str, Any]:
        """Run Hyperledger benchmarks."""
        return benchmark_hyperledger(
            operations=self.config.hl_operations,
            iterations=self.config.hl_iterations
        )
    
    def _run_security_analysis(self) -> Dict[str, Any]:
        """Run security analysis on all algorithms."""
        return {
            "aes": self.security_analyzer.analyze_aes_security(),
            "eddsa": self.security_analyzer.analyze_eddsa_security(),
            "hyperledger": self.security_analyzer.analyze_hyperledger_security()
        }
    
    def _generate_comparative_analysis(self) -> Dict[str, Any]:
        """Generate comparative analysis across all algorithms."""
        comparative = {
            "performance_comparison": {},
            "security_comparison": {},
            "recommendations": []
        }
        
        # Performance comparison for 1MB data
        if "aes" in self.results:
            aes_256_gcm = self.results["aes"].get("aes_256_GCM", {})
            if 1048576 in aes_256_gcm:
                comparative["performance_comparison"]["aes_256_gcm_1mb"] = aes_256_gcm[1048576]
        
        if "eddsa" in self.results:
            eddsa_25519 = self.results["eddsa"].get("eddsa_Ed25519", {})
            if 1024 in eddsa_25519:
                comparative["performance_comparison"]["eddsa_ed25519_1kb"] = eddsa_25519[1024]
        
        if "hyperledger" in self.results:
            hl_invoke = self.results["hyperledger"].get("invoke", {})
            comparative["performance_comparison"]["hyperledger_invoke"] = hl_invoke
        
        # Security comparison
        if "security" in self.results:
            comparative["security_comparison"] = self.results["security"]
        
        # Generate recommendations
        comparative["recommendations"] = self._generate_recommendations()
        
        return comparative
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on benchmark results."""
        recommendations = []
        
        # AES recommendations
        if "aes" in self.results:
            recommendations.append(
                "AES-256-GCM recommended for high-security data encryption in cloud storage. "
                "Provides authenticated encryption with excellent performance."
            )
            recommendations.append(
                "AES-128-GCM suitable for less sensitive data with lower computational overhead."
            )
        
        # EdDSA recommendations
        if "eddsa" in self.results:
            recommendations.append(
                "Ed25519 recommended for digital signatures - excellent performance, "
                "strong security (128-bit), and resistance to side-channel attacks."
            )
            recommendations.append(
                "Ed448 provides higher security margin (224-bit) for long-term protection "
                "but with ~2x computational cost."
            )
        
        # Hyperledger recommendations
        if "hyperledger" in self.results:
            recommendations.append(
                "Hyperledger Fabric suitable for multi-party cloud deployments requiring "
                "audit trails and tamper-proof logs. Trade-off: higher latency vs. centralized DB."
            )
            recommendations.append(
                "Consider Raft consensus for production deployments; Kafka for high-throughput needs."
            )
        
        # Cross-cutting recommendations
        recommendations.append(
            "Hybrid approach: Use AES-256-GCM for data encryption, Ed25519 for authentication, "
            "Hyperledger for audit logging in multi-tenant cloud environments."
        )
        
        return recommendations
    
    def _save_results(self):
        """Save benchmark results to files."""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        
        # Save JSON
        json_file = self.output_dir / f"benchmark_results_{timestamp}.json"
        with open(json_file, "w") as f:
            json.dump(self.results, f, indent=2, default=str)
        
        # Save summary
        summary_file = self.output_dir / f"benchmark_summary_{timestamp}.txt"
        with open(summary_file, "w") as f:
            f.write(self._generate_summary())
        
        print(f"\nResults saved to {json_file}")
        print(f"Summary saved to {summary_file}")
    
    def _generate_summary(self) -> str:
        """Generate human-readable summary."""
        lines = [
            "CloudShield AI Benchmark Summary",
            "=" * 40,
            ""
        ]
        
        if "aes" in self.results:
            lines.append("AES Results:")
            for key, data in self.results["aes"].items():
                if 1048576 in data:
                    d = data[1048576]
                    lines.append(f"  {key}: {d['avg_encryption_ms']:.2f} ms encrypt, "
                                f"{d['throughput_mbps']:.2f} MB/s")
            lines.append("")
        
        if "eddsa" in self.results:
            lines.append("EdDSA Results:")
            for key, data in self.results["eddsa"].items():
                if 1024 in data:
                    d = data[1024]
                    lines.append(f"  {key}: {d['avg_signing_ms']:.2f} ms sign, "
                                f"{d['signatures_per_second']:.0f} sig/s")
            lines.append("")
        
        if "hyperledger" in self.results:
            lines.append("Hyperledger Results:")
            for op, data in self.results["hyperledger"].items():
                if "avg_latency_ms" in data:
                    lines.append(f"  {op}: {data['avg_latency_ms']:.2f} ms latency, "
                                f"{data['avg_throughput_tps']:.0f} TPS")
            lines.append("")
        
        if "comparative" in self.results and "recommendations" in self.results["comparative"]:
            lines.append("Recommendations:")
            for rec in self.results["comparative"]["recommendations"]:
                lines.append(f"  - {rec}")
        
        return "\n".join(lines)


def main():
    """Main entry point for benchmarks."""
    config = BenchmarkConfig(
        iterations=100,  # Reduced for quick testing
        warmup_iterations=10,
        hl_iterations=10
    )
    
    runner = BenchmarkRunner(config)
    results = runner.run_all_benchmarks()
    
    # Print summary
    print(runner._generate_summary())


if __name__ == "__main__":
    main()