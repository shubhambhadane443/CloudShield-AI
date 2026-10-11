"""
CloudShield AI - Security Analysis Module
Provides security analysis for cryptographic algorithms and blockchain models.
"""

from typing import Dict, Any, List
from dataclasses import dataclass
from enum import Enum


class SecurityLevel(Enum):
    """Security strength levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


@dataclass
class SecurityFinding:
    """Security analysis finding."""
    category: str
    severity: SecurityLevel
    description: str
    recommendation: str
    references: List[str]


class SecurityAnalyzer:
    """Security analysis for cryptographic algorithms and blockchain."""
    
    def __init__(self):
        self.findings = []
    
    def analyze_aes_security(self) -> Dict[str, Any]:
        """Analyze AES security posture."""
        findings = [
            SecurityFinding(
                category="Key Management",
                severity=SecurityLevel.HIGH,
                description="AES security critically depends on key secrecy. "
                           "Key rotation policies must be enforced.",
                recommendation="Implement automated key rotation every 90 days. "
                              "Use HSMs for key storage in production.",
                references=["NIST SP 800-38D", "NIST SP 800-57"]
            ),
            SecurityFinding(
                category="Mode Selection",
                severity=SecurityLevel.HIGH,
                description="GCM mode provides authenticated encryption but has "
                           "strict IV uniqueness requirements.",
                recommendation="Use 96-bit IVs with deterministic construction "
                              "(counter-based) or 12-byte random IVs. "
                              "Never reuse IV with same key.",
                references=["NIST SP 800-38D", "RFC 5288"]
            ),
            SecurityFinding(
                category="Data Limits",
                severity=SecurityLevel.MEDIUM,
                description="GCM has a 64GB limit per key (2^36 blocks). "
                           "Exceeding this breaks security guarantees.",
                recommendation="Enforce key rotation before 64GB encrypted. "
                              "Monitor data volume per key.",
                references=["NIST SP 800-38D Section 8.3"]
            ),
            SecurityFinding(
                category="Side-Channel Resistance",
                severity=SecurityLevel.MEDIUM,
                description="Software AES implementations vulnerable to "
                           "timing and cache attacks.",
                recommendation="Use hardware AES-NI instructions. "
                              "Consider constant-time implementations.",
                references=["Intel AES-NI", "CHES 2010 side-channel research"]
            ),
            SecurityFinding(
                category="Quantum Resistance",
                severity=SecurityLevel.LOW,
                description="AES-256 provides 128-bit post-quantum security "
                           "(Grover's algorithm reduces to 128-bit).",
                recommendation="AES-256 is quantum-resistant for foreseeable future. "
                              "No immediate action needed.",
                references=["NIST PQC standardization", "Grover's algorithm analysis"]
            )
        ]
        
        return {
            "algorithm": "AES",
            "overall_rating": "HIGH",
            "key_sizes": {
                128: {"security_bits": 128, "quantum_bits": 64, "recommended": "legacy_only"},
                192: {"security_bits": 192, "quantum_bits": 96, "recommended": "transitioning"},
                256: {"security_bits": 256, "quantum_bits": 128, "recommended": "preferred"}
            },
            "modes": {
                "GCM": {"authenticated": True, "nonce_misuse_resistant": False, "recommended": True},
                "CBC": {"authenticated": False, "nonce_misuse_resistant": False, "recommended": False},
                "CTR": {"authenticated": False, "nonce_misuse_resistant": False, "recommended": False},
                "CCM": {"authenticated": True, "nonce_misuse_resistant": False, "recommended": True},
                "OCB": {"authenticated": True, "nonce_misuse_resistant": True, "recommended": True}
            },
            "findings": [f.__dict__ for f in findings],
            "compliance": {
                "FIPS_140_2": True,
                "FIPS_140_3": True,
                "Common_Criteria": True,
                "PCI_DSS": True,
                "GDPR": True
            }
        }
    
    def analyze_eddsa_security(self) -> Dict[str, Any]:
        """Analyze EdDSA security posture."""
        findings = [
            SecurityFinding(
                category="Curve Selection",
                severity=SecurityLevel.HIGH,
                description="Ed25519 provides 128-bit security. Ed448 provides "
                           "224-bit security for long-term protection.",
                recommendation="Use Ed25519 for most applications. "
                              "Use Ed448 for long-term archival (>20 years).",
                references=["RFC 8032", "NIST SP 800-186"]
            ),
            SecurityFinding(
                category="Side-Channel Resistance",
                severity=SecurityLevel.HIGH,
                description="EdDSA designed with side-channel resistance. "
                           "No secret-dependent branches or memory access.",
                recommendation="Prefer EdDSA over ECDSA for side-channel resistance. "
                              "Use constant-time implementations.",
                references=["RFC 8032", "Bernstein et al. Ed25519 paper"]
            ),
            SecurityFinding(
                category="Randomness Requirements",
                severity=SecurityLevel.HIGH,
                description="EdDSA is deterministic - no per-signature randomness needed. "
                           "Eliminates entropy failure attacks.",
                recommendation="No additional entropy source needed for signing. "
                              "Simplifies implementation and improves security.",
                references=["RFC 8032 Section 5.1.6"]
            ),
            SecurityFinding(
                category="Quantum Resistance",
                severity=SecurityLevel.LOW,
                description="EdDSA based on elliptic curve discrete log - "
                           "broken by Shor's algorithm.",
                recommendation="Plan migration to post-quantum signatures (e.g., Dilithium, "
                              "Falcon) for long-term secrets. Ed25519 safe for "
                              "ephemeral/authentication use.",
                references=["NIST PQC Round 3", "Shor's algorithm"]
            ),
            SecurityFinding(
                category="Implementation Pitfalls",
                severity=SecurityLevel.MEDIUM,
                description="Point decompression validation critical. "
                           "Invalid curve points can leak private key.",
                recommendation="Always validate public keys before use. "
                              "Use well-tested libraries (libsodium, cryptography).",
                references=["RFC 8032 Section 5.1.3", "Invalid curve attacks"]
            )
        ]
        
        return {
            "algorithm": "EdDSA",
            "overall_rating": "VERY_HIGH",
            "curves": {
                "Ed25519": {
                    "security_bits": 128,
                    "quantum_bits": 0,
                    "signature_size": 64,
                    "public_key_size": 32,
                    "private_key_size": 32,
                    "recommended": "general_purpose"
                },
                "Ed448": {
                    "security_bits": 224,
                    "quantum_bits": 0,
                    "signature_size": 114,
                    "public_key_size": 57,
                    "private_key_size": 57,
                    "recommended": "high_security_long_term"
                }
            },
            "findings": [f.__dict__ for f in findings],
            "compliance": {
                "FIPS_186_5": True,
                "RFC_8032": True,
                "TLS_1.3": True,
                "SSH": True,
                "JWT": True
            }
        }
    
    def analyze_hyperledger_security(self) -> Dict[str, Any]:
        """Analyze Hyperledger Fabric security posture."""
        findings = [
            SecurityFinding(
                category="Consensus Security",
                severity=SecurityLevel.HIGH,
                description="Raft consensus provides crash fault tolerance only. "
                           "Byzantine fault tolerance requires BFT-SMaRt or similar.",
                recommendation="Use Raft for trusted consortium networks. "
                              "Consider BFT ordering service for untrusted participants.",
                references=["Hyperledger Fabric Raft docs", "BFT-SMaRt"]
            ),
            SecurityFinding(
                category="Endorsement Policy",
                severity=SecurityLevel.HIGH,
                description="Endorsement policies define trust assumptions. "
                           "Weak policies allow malicious endorsements.",
                recommendation="Use AND policies for multi-party agreement. "
                              "Require signatures from majority of organizations.",
                references=["Fabric Endorsement Policies", "Fabric Architecture"]
            ),
            SecurityFinding(
                category="Channel Privacy",
                severity=SecurityLevel.MEDIUM,
                description="Channels provide data isolation but metadata "
                           "(channel existence, participants) may leak.",
                recommendation="Use private data collections for sensitive data. "
                              "Limit channel membership visibility.",
                references=["Fabric Private Data", "Fabric Channels"]
            ),
            SecurityFinding(
                category="Chaincode Security",
                severity=SecurityLevel.HIGH,
                description="Chaincode runs in isolated containers but shares "
                           "host kernel. Vulnerable chaincode affects all peers.",
                recommendation="Audit chaincode thoroughly. "
                              "Use sandboxing (gVisor, Kata Containers). "
                              "Implement chaincode upgrade policies.",
                references=["Fabric Chaincode Security", "Container Security"]
            ),
            SecurityFinding(
                category="Identity Management",
                severity=SecurityLevel.HIGH,
                description="X.509 certificates manage identities. "
                           "Certificate revocation and rotation critical.",
                recommendation="Implement automated certificate rotation. "
                              "Use short-lived certificates (24-48h). "
                              "Integrate with external IdP (LDAP, OIDC).",
                references=["Fabric CA", "X.509 Certificate Management"]
            ),
            SecurityFinding(
                category="Quantum Resistance",
                severity=SecurityLevel.LOW,
                description="Fabric uses ECDSA/P256 for TLS and signatures. "
                           "Vulnerable to quantum attacks.",
                recommendation="Monitor NIST PQC standardization. "
                              "Plan migration to post-quantum TLS and signatures. "
                              "Fabric 3.0+ expected to support PQC.",
                references=["NIST PQC", "Hyperledger Fabric Roadmap"]
            )
        ]
        
        return {
            "platform": "Hyperledger Fabric",
            "version": "2.5+",
            "overall_rating": "HIGH",
            "consensus": {
                "Raft": {"byzantine_tolerant": False, "crash_tolerant": True, "recommended": "trusted_networks"},
                "Kafka": {"byzantine_tolerant": False, "crash_tolerant": True, "recommended": "deprecated"},
                "BFT-SMaRt": {"byzantine_tolerant": True, "crash_tolerant": True, "recommended": "untrusted_networks"}
            },
            "security_features": {
                "channels": "Data isolation between participant groups",
                "private_data": "Confidential data within channels",
                "endorsement_policies": "Configurable trust models",
                "identity_msp": "X.509-based identity management",
                "tls": "Mutual TLS for all communication",
                "audit_logging": "Immutable transaction ledger"
            },
            "findings": [f.__dict__ for f in findings],
            "compliance": {
                "GDPR": "With private data collections",
                "HIPAA": "With proper configuration",
                "SOX": "With immutable audit trail",
                "PCI_DSS": "With network segmentation",
                "ISO_27001": "With proper controls"
            }
        }
    
    def get_all_findings(self) -> List[SecurityFinding]:
        """Get all security findings across all analyses."""
        all_findings = []
        for analysis in [self.analyze_aes_security(), 
                        self.analyze_eddsa_security(), 
                        self.analyze_hyperledger_security()]:
            all_findings.extend(analysis["findings"])
        return all_findings
    
    def get_critical_findings(self) -> List[SecurityFinding]:
        """Get only critical/high severity findings."""
        all_findings = self.get_all_findings()
        return [f for f in all_findings 
                if f["severity"] in [SecurityLevel.HIGH, SecurityLevel.VERY_HIGH]]