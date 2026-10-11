"""
CloudShield AI - Test Suite
Basic tests for cryptographic modules.
"""

import pytest
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from crypto.aes import AESCipher, AESResult
from crypto.eddsa import EdDSACipher, EdDSAResult
from security.analysis import SecurityAnalyzer, SecurityLevel


class TestAES:
    """Tests for AES encryption."""
    
    def test_aes_256_gcm_encrypt_decrypt(self):
        """Test AES-256-GCM encryption and decryption."""
        cipher = AESCipher(key_size=256, mode="GCM")
        plaintext = b"Test message for AES-256-GCM"
        
        result = cipher.encrypt(plaintext)
        
        assert isinstance(result, AESResult)
        assert result.ciphertext != plaintext
        assert result.iv is not None
        assert result.tag is not None
        assert result.key_size == 256
        assert result.mode == "GCM"
        assert result.data_size == len(plaintext)
        
        # Verify decryption works
        decrypted = cipher.decrypt(result.ciphertext, result.iv, result.tag)
        assert decrypted == plaintext
    
    def test_aes_128_cbc(self):
        """Test AES-128-CBC encryption."""
        cipher = AESCipher(key_size=128, mode="CBC")
        plaintext = b"Test message for AES-128-CBC"
        
        result = cipher.encrypt(plaintext)
        
        assert result.key_size == 128
        assert result.mode == "CBC"
        assert result.tag is None  # CBC doesn't have auth tag
        
        decrypted = cipher.decrypt(result.ciphertext, result.iv, result.tag)
        assert decrypted == plaintext
    
    def test_aes_256_ctr(self):
        """Test AES-256-CTR encryption."""
        cipher = AESCipher(key_size=256, mode="CTR")
        plaintext = b"Test message for AES-256-CTR"
        
        result = cipher.encrypt(plaintext)
        
        assert result.key_size == 256
        assert result.mode == "CTR"
        assert result.tag is None
        
        decrypted = cipher.decrypt(result.ciphertext, result.iv, result.tag)
        assert decrypted == plaintext
    
    def test_invalid_key_size(self):
        """Test that invalid key sizes raise ValueError."""
        with pytest.raises(ValueError):
            AESCipher(key_size=512, mode="GCM")
    
    def test_invalid_mode(self):
        """Test that invalid modes raise ValueError."""
        with pytest.raises(ValueError):
            AESCipher(key_size=256, mode="INVALID")


class TestEdDSA:
    """Tests for EdDSA signatures."""
    
    def test_ed25519_sign_verify(self):
        """Test Ed25519 signing and verification."""
        cipher = EdDSACipher(curve="Ed25519")
        message = b"Test message for Ed25519"
        
        result = cipher.sign(message)
        
        assert isinstance(result, EdDSAResult)
        assert result.signature is not None
        assert result.curve == "Ed25519"
        assert result.message_size == len(message)
        assert result.public_key_size == 32
        assert result.private_key_size == 32
        assert result.signature_size == 64
        
        # Verify signature
        assert cipher.verify(message, result.signature) is True
        
        # Verify wrong message fails
        assert cipher.verify(b"Wrong message", result.signature) is False
    
    def test_ed448_sign_verify(self):
        """Test Ed448 signing and verification."""
        cipher = EdDSACipher(curve="Ed448")
        message = b"Test message for Ed448"
        
        result = cipher.sign(message)
        
        assert result.curve == "Ed448"
        assert result.public_key_size == 57
        assert result.private_key_size == 57
        assert result.signature_size == 114
        
        assert cipher.verify(message, result.signature) is True
    
    def test_invalid_curve(self):
        """Test that invalid curves raise ValueError."""
        with pytest.raises(ValueError):
            EdDSACipher(curve="InvalidCurve")
    
    def test_keypair_generation(self):
        """Test keypair generation."""
        priv, pub = EdDSACipher.generate_keypair("Ed25519")
        
        assert len(priv) == 32
        assert len(pub) == 32
        assert priv != pub
    
    def test_load_private_key(self):
        """Test loading private key from bytes."""
        cipher = EdDSACipher(curve="Ed25519")
        priv_bytes = cipher.get_private_key_bytes()
        
        loaded_key = EdDSACipher.load_private_key(priv_bytes, "Ed25519")
        assert loaded_key is not None


class TestSecurityAnalysis:
    """Tests for security analysis."""
    
    def test_aes_security_analysis(self):
        """Test AES security analysis runs."""
        analyzer = SecurityAnalyzer()
        result = analyzer.analyze_aes_security()
        
        assert result["algorithm"] == "AES"
        assert result["overall_rating"] == "HIGH"
        assert "key_sizes" in result
        assert "modes" in result
        assert "findings" in result
        assert len(result["findings"]) > 0
    
    def test_eddsa_security_analysis(self):
        """Test EdDSA security analysis runs."""
        analyzer = SecurityAnalyzer()
        result = analyzer.analyze_eddsa_security()
        
        assert result["algorithm"] == "EdDSA"
        assert result["overall_rating"] == "VERY_HIGH"
        assert "curves" in result
        assert "findings" in result
        assert len(result["findings"]) > 0
    
    def test_hyperledger_security_analysis(self):
        """Test Hyperledger security analysis runs."""
        analyzer = SecurityAnalyzer()
        result = analyzer.analyze_hyperledger_security()
        
        assert result["platform"] == "Hyperledger Fabric"
        assert result["overall_rating"] == "HIGH"
        assert "consensus" in result
        assert "findings" in result
        assert len(result["findings"]) > 0
    
    def test_critical_findings(self):
        """Test getting critical findings."""
        analyzer = SecurityAnalyzer()
        critical = analyzer.get_critical_findings()
        
        assert len(critical) > 0
        for finding in critical:
            assert finding["severity"] in [SecurityLevel.HIGH, SecurityLevel.VERY_HIGH]


class TestBenchmarkRunner:
    """Tests for benchmark runner."""
    
    def test_benchmark_config_defaults(self):
        """Test benchmark config has sensible defaults."""
        from benchmarks.runner import BenchmarkConfig
        
        config = BenchmarkConfig()
        
        assert config.iterations > 0
        assert config.warmup_iterations >= 0
        assert len(config.data_sizes) > 0
        assert len(config.aes_key_sizes) > 0
        assert len(config.aes_modes) > 0
        assert len(config.eddsa_curves) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])