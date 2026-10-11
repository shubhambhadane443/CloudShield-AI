#!/usr/bin/env python3
"""
CloudShield AI - Main CLI Entry Point
Command-line interface for running benchmarks and analysis.
"""

import argparse
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from benchmarks.runner import BenchmarkRunner, BenchmarkConfig, main as run_benchmarks
from security.analysis import SecurityAnalyzer


def run_security_analysis():
    """Run security analysis only."""
    analyzer = SecurityAnalyzer()
    
    print("CloudShield AI Security Analysis")
    print("=" * 50)
    
    # AES Analysis
    print("\n1. AES Security Analysis")
    aes_result = analyzer.analyze_aes_security()
    print(f"   Overall Rating: {aes_result['overall_rating']}")
    print(f"   Key Sizes: {list(aes_result['key_sizes'].keys())}")
    print(f"   Modes: {list(aes_result['modes'].keys())}")
    print(f"   Findings: {len(aes_result['findings'])}")
    print(f"   Compliance: {list(aes_result['compliance'].keys())}")
    
    # EdDSA Analysis
    print("\n2. EdDSA Security Analysis")
    eddsa_result = analyzer.analyze_eddsa_security()
    print(f"   Overall Rating: {eddsa_result['overall_rating']}")
    print(f"   Curves: {list(eddsa_result['curves'].keys())}")
    print(f"   Findings: {len(eddsa_result['findings'])}")
    print(f"   Compliance: {list(eddsa_result['compliance'].keys())}")
    
    # Hyperledger Analysis
    print("\n3. Hyperledger Security Analysis")
    hl_result = analyzer.analyze_hyperledger_security()
    print(f"   Overall Rating: {hl_result['overall_rating']}")
    print(f"   Consensus Options: {list(hl_result['consensus'].keys())}")
    print(f"   Findings: {len(hl_result['findings'])}")
    print(f"   Compliance: {list(hl_result['compliance'].keys())}")
    
    # Critical findings
    print("\n4. Critical Findings (HIGH/VERY_HIGH)")
    critical = analyzer.get_critical_findings()
    for i, finding in enumerate(critical, 1):
        print(f"   {i}. [{finding['severity'].value.upper()}] {finding['category']}")
        print(f"      {finding['description']}")
        print(f"      Recommendation: {finding['recommendation']}")


def run_quick_benchmark():
    """Run quick benchmark with reduced iterations."""
    config = BenchmarkConfig(
        iterations=50,
        warmup_iterations=5,
        hl_iterations=5
    )
    
    runner = BenchmarkRunner(config)
    results = runner.run_all_benchmarks()
    print(runner._generate_summary())


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="CloudShield AI - Cryptographic Benchmark and Security Analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  cloudshield benchmark          # Run full benchmarks
  cloudshield benchmark --quick  # Run quick benchmarks
  cloudshield security           # Run security analysis only
  cloudshield --help             # Show this help
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Benchmark command
    bench_parser = subparsers.add_parser("benchmark", help="Run performance benchmarks")
    bench_parser.add_argument("--quick", action="store_true", help="Run quick benchmarks")
    bench_parser.add_argument("--iterations", type=int, default=1000, help="Number of iterations")
    bench_parser.add_argument("--output", type=str, default="./data/results", help="Output directory")
    
    # Security command
    sec_parser = subparsers.add_parser("security", help="Run security analysis")
    
    # Version command
    parser.add_argument("--version", action="version", version="CloudShield AI 1.0.0")
    
    args = parser.parse_args()
    
    if args.command == "benchmark":
        if args.quick:
            run_quick_benchmark()
        else:
            config = BenchmarkConfig(iterations=args.iterations)
            runner = BenchmarkRunner(config, output_dir=args.output)
            runner.run_all_benchmarks()
    elif args.command == "security":
        run_security_analysis()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()