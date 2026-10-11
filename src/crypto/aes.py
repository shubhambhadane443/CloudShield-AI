"""
CloudShield AI - AES Encryption Module
Provides AES encryption/decryption with multiple modes and key sizes.
"""

import os
import time
from typing import Tuple, Dict, Any, Optional
from dataclasses import dataclass
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend


@dataclass
class AESResult:
    """Result of AES operation."""
    ciphertext: bytes
    iv: bytes
    tag: Optional[bytes]
    encryption_time: float
    decryption_time: float
    key_size: int
    mode: str
    data_size: int


class AESCipher:
    """AES encryption/decryption with performance tracking."""
    
    SUPPORTED_MODES = ["GCM", "CBC", "CTR"]
    SUPPORTED_KEY_SIZES = [128, 192, 256]
    
    def __init__(self, key_size: int = 256, mode: str = "GCM"):
        if key_size not in self.SUPPORTED_KEY_SIZES:
            raise ValueError(f"Key size must be one of {self.SUPPORTED_KEY_SIZES}")
        if mode not in self.SUPPORTED_MODES:
            raise ValueError(f"Mode must be one of {self.SUPPORTED_MODES}")
        
        self.key_size = key_size
        self.mode = mode
        self.key = os.urandom(key_size // 8)
        self.backend = default_backend()
    
    def encrypt(self, plaintext: bytes, associated_data: bytes = b"") -> AESResult:
        """Encrypt plaintext and return result with timing."""
        iv = os.urandom(12 if self.mode == "GCM" else 16)
        
        start_enc = time.perf_counter()
        
        if self.mode == "GCM":
            cipher = Cipher(
                algorithms.AES(self.key),
                modes.GCM(iv),
                backend=self.backend
            )
            encryptor = cipher.encryptor()
            encryptor.authenticate_additional_data(associated_data)
            ciphertext = encryptor.update(plaintext) + encryptor.finalize()
            tag = encryptor.tag
        elif self.mode == "CBC":
            padder = padding.PKCS7(128).padder()
            padded_data = padder.update(plaintext) + padder.finalize()
            cipher = Cipher(
                algorithms.AES(self.key),
                modes.CBC(iv),
                backend=self.backend
            )
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(padded_data) + encryptor.finalize()
            tag = None
        else:  # CTR
            cipher = Cipher(
                algorithms.AES(self.key),
                modes.CTR(iv),
                backend=self.backend
            )
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(plaintext) + encryptor.finalize()
            tag = None
        
        encryption_time = time.perf_counter() - start_enc
        
        # Decrypt to verify and measure decryption time
        start_dec = time.perf_counter()
        self.decrypt(ciphertext, iv, tag, associated_data)
        decryption_time = time.perf_counter() - start_dec
        
        return AESResult(
            ciphertext=ciphertext,
            iv=iv,
            tag=tag,
            encryption_time=encryption_time,
            decryption_time=decryption_time,
            key_size=self.key_size,
            mode=self.mode,
            data_size=len(plaintext)
        )
    
    def decrypt(self, ciphertext: bytes, iv: bytes, tag: Optional[bytes], 
                associated_data: bytes = b"") -> bytes:
        """Decrypt ciphertext."""
        if self.mode == "GCM":
            cipher = Cipher(
                algorithms.AES(self.key),
                modes.GCM(iv, tag),
                backend=self.backend
            )
            decryptor = cipher.decryptor()
            decryptor.authenticate_additional_data(associated_data)
            return decryptor.update(ciphertext) + decryptor.finalize()
        elif self.mode == "CBC":
            cipher = Cipher(
                algorithms.AES(self.key),
                modes.CBC(iv),
                backend=self.backend
            )
            decryptor = cipher.decryptor()
            padded = decryptor.update(ciphertext) + decryptor.finalize()
            unpadder = padding.PKCS7(128).unpadder()
            return unpadder.update(padded) + unpadder.finalize()
        else:  # CTR
            cipher = Cipher(
                algorithms.AES(self.key),
                modes.CTR(iv),
                backend=self.backend
            )
            decryptor = cipher.decryptor()
            return decryptor.update(ciphertext) + decryptor.finalize()
    
    @staticmethod
    def generate_key(key_size: int) -> bytes:
        """Generate a random AES key."""
        if key_size not in AESCipher.SUPPORTED_KEY_SIZES:
            raise ValueError(f"Key size must be one of {AESCipher.SUPPORTED_KEY_SIZES}")
        return os.urandom(key_size // 8)
    
    def get_key(self) -> bytes:
        """Return the current key."""
        return self.key


def benchmark_aes(data_sizes: list, key_sizes: list, modes: list, 
                  iterations: int = 1000) -> Dict[str, Any]:
    """Run comprehensive AES benchmarks."""
    results = {}
    
    for key_size in key_sizes:
        for mode in modes:
            cipher = AESCipher(key_size=key_size, mode=mode)
            key_results = {}
            
            for data_size in data_sizes:
                plaintext = os.urandom(data_size)
                times = {"encryption": [], "decryption": []}
                
                for _ in range(iterations):
                    result = cipher.encrypt(plaintext)
                    times["encryption"].append(result.encryption_time)
                    times["decryption"].append(result.decryption_time)
                
                key_results[data_size] = {
                    "avg_encryption_ms": sum(times["encryption"]) / len(times["encryption"]) * 1000,
                    "avg_decryption_ms": sum(times["decryption"]) / len(times["decryption"]) * 1000,
                    "min_encryption_ms": min(times["encryption"]) * 1000,
                    "max_encryption_ms": max(times["encryption"]) * 1000,
                    "throughput_mbps": (data_size / 1024 / 1024) / 
                                      (sum(times["encryption"]) / len(times["encryption"]))
                }
            
            results[f"aes_{key_size}_{mode}"] = key_results
    
    return results