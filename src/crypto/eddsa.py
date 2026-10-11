"""
CloudShield AI - EdDSA Signature Module
Provides EdDSA signing/verification with multiple curves.
"""

import os
import time
from typing import Tuple, Dict, Any, Optional
from dataclasses import dataclass
from cryptography.hazmat.primitives.asymmetric import ed25519, ed448
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.utils import Prehashed
from cryptography.exceptions import InvalidSignature


@dataclass
class EdDSAResult:
    """Result of EdDSA operation."""
    signature: bytes
    signing_time: float
    verification_time: float
    curve: str
    message_size: int
    public_key_size: int
    private_key_size: int
    signature_size: int


class EdDSACipher:
    """EdDSA signing/verification with performance tracking."""
    
    SUPPORTED_CURVES = {
        "Ed25519": ed25519,
        "Ed448": ed448
    }
    
    def __init__(self, curve: str = "Ed25519"):
        if curve not in self.SUPPORTED_CURVES:
            raise ValueError(f"Curve must be one of {list(self.SUPPORTED_CURVES.keys())}")
        
        self.curve_name = curve
        self.curve_module = self.SUPPORTED_CURVES[curve]
        self.private_key = self.curve_module.Ed25519PrivateKey.generate() if curve == "Ed25519" \
            else self.curve_module.Ed448PrivateKey.generate()
        self.public_key = self.private_key.public_key()
    
    def sign(self, message: bytes) -> EdDSAResult:
        """Sign message and return result with timing."""
        start_sign = time.perf_counter()
        signature = self.private_key.sign(message)
        signing_time = time.perf_counter() - start_sign
        
        start_verify = time.perf_counter()
        self.verify(message, signature)
        verification_time = time.perf_counter() - start_verify
        
        return EdDSAResult(
            signature=signature,
            signing_time=signing_time,
            verification_time=verification_time,
            curve=self.curve_name,
            message_size=len(message),
            public_key_size=len(self.public_key.public_bytes_raw()),
            private_key_size=len(self.private_key.private_bytes_raw()),
            signature_size=len(signature)
        )
    
    def verify(self, message: bytes, signature: bytes) -> bool:
        """Verify signature."""
        try:
            self.public_key.verify(signature, message)
            return True
        except InvalidSignature:
            return False
    
    def get_public_key_bytes(self) -> bytes:
        """Get public key as raw bytes."""
        return self.public_key.public_bytes_raw()
    
    def get_private_key_bytes(self) -> bytes:
        """Get private key as raw bytes."""
        return self.private_key.private_bytes_raw()
    
    @staticmethod
    def generate_keypair(curve: str = "Ed25519") -> Tuple[bytes, bytes]:
        """Generate a new EdDSA keypair."""
        if curve not in EdDSACipher.SUPPORTED_CURVES:
            raise ValueError(f"Curve must be one of {list(EdDSACipher.SUPPORTED_CURVES.keys())}")
        
        curve_module = EdDSACipher.SUPPORTED_CURVES[curve]
        if curve == "Ed25519":
            private_key = curve_module.Ed25519PrivateKey.generate()
        else:
            private_key = curve_module.Ed448PrivateKey.generate()
        
        public_key = private_key.public_key()
        return (
            private_key.private_bytes_raw(),
            public_key.public_bytes_raw()
        )
    
    @staticmethod
    def load_private_key(private_key_bytes: bytes, curve: str = "Ed25519"):
        """Load private key from bytes."""
        curve_module = EdDSACipher.SUPPORTED_CURVES[curve]
        if curve == "Ed25519":
            return curve_module.Ed25519PrivateKey.from_private_bytes(private_key_bytes)
        else:
            return curve_module.Ed448PrivateKey.from_private_bytes(private_key_bytes)


def benchmark_eddsa(message_sizes: list, curves: list, iterations: int = 1000) -> Dict[str, Any]:
    """Run comprehensive EdDSA benchmarks."""
    results = {}
    
    for curve in curves:
        cipher = EdDSACipher(curve=curve)
        curve_results = {}
        
        for msg_size in message_sizes:
            message = os.urandom(msg_size)
            times = {"signing": [], "verification": []}
            
            for _ in range(iterations):
                result = cipher.sign(message)
                times["signing"].append(result.signing_time)
                times["verification"].append(result.verification_time)
            
            curve_results[msg_size] = {
                "avg_signing_ms": sum(times["signing"]) / len(times["signing"]) * 1000,
                "avg_verification_ms": sum(times["verification"]) / len(times["verification"]) * 1000,
                "min_signing_ms": min(times["signing"]) * 1000,
                "max_signing_ms": max(times["signing"]) * 1000,
                "signatures_per_second": 1 / (sum(times["signing"]) / len(times["signing"])),
                "public_key_size": cipher.get_public_key_bytes().__len__(),
                "signature_size": len(cipher.sign(message).signature)
            }
        
        results[f"eddsa_{curve}"] = curve_results
    
    return results