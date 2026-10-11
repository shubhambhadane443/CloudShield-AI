import React, { useState, useEffect, useRef, Component } from 'react'
import axios from 'axios'
import {
  Shield, Cpu, Zap, Database, Lock, Play, RefreshCw,
  ChevronDown, ChevronUp, ExternalLink, AlertTriangle,
  CheckCircle, XCircle, Loader2, BarChart2, Key, Hash,
  WifiOff, Bug, AlertCircle
} from 'lucide-react'

const API_BASE = '/api/v1'

const api = axios.create({
  baseURL: API_BASE,
  timeout: 30000
})

// Health check uses root path (not under /api/v1)
const healthApi = axios.create({
  baseURL: '/api',
  timeout: 10000
})

// Add response interceptor for better error handling
api.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error.config?.url, error.response?.status, error.message)
    return Promise.reject(error)
  }
)

// Error Boundary to catch render errors
class ErrorBoundary extends Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false, error: null, errorInfo: null }
  }

  static getDerivedStateFromError(error) {
    return { hasError: true }
  }

  componentDidCatch(error, errorInfo) {
    this.setState({ error, errorInfo })
    console.error('Render Error:', error, errorInfo)
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{ padding: '40px', color: 'white', fontFamily: 'system-ui', textAlign: 'center' }}>
          <AlertCircle size={48} style={{ color: '#ef4444', marginBottom: '16px' }} />
          <h2>Something went wrong</h2>
          <pre style={{ textAlign: 'left', background: '#1e293b', padding: '16px', borderRadius: '8px', overflow: 'auto', maxWidth: '600px', margin: '20px auto' }}>
            {this.state.error?.toString()}
            {this.state.errorInfo?.componentStack}
          </pre>
          <button 
            onClick={() => this.setState({ hasError: false, error: null, errorInfo: null })}
            style={{ padding: '10px 20px', background: '#3b82f6', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer' }}
          >
            Try Again
          </button>
        </div>
      )
    }
    return this.props.children
  }
}

function formatNumber(num) {
  if (num >= 1e9) return (num / 1e9).toFixed(2) + 'B'
  if (num >= 1e6) return (num / 1e6).toFixed(2) + 'M'
  if (num >= 1e3) return (num / 1e3).toFixed(2) + 'K'
  return num.toFixed(2)
}

function formatBytes(bytes) {
  if (bytes >= 1e9) return (bytes / 1e9).toFixed(2) + ' GB'
  if (bytes >= 1e6) return (bytes / 1e6).toFixed(2) + ' MB'
  if (bytes >= 1e3) return (bytes / 1e3).toFixed(2) + ' KB'
  return bytes + ' B'
}

function MetricCard({ label, value, unit, icon: Icon, color }) {
  return (
    <div className="metric">
      <div className="metric-label" style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
        <Icon size={14} style={{ color }} />
        {label}
      </div>
      <div className="metric-value" style={{ color }}>
        {value}
        <span className="metric-unit">{unit}</span>
      </div>
    </div>
  )
}

function AESPanel() {
  const [plaintext, setPlaintext] = useState('Hello, CloudShield AI!')
  const [keySize, setKeySize] = useState(256)
  const [mode, setMode] = useState('GCM')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleEncrypt = async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await api.post('/aes/encrypt', {
        plaintext,
        key_size: keySize,
        mode
      })
      setResult(res.data)
    } catch (err) {
      setError(err.response?.data?.detail || err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleBenchmark = async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await api.post('/aes/benchmark', {
        key_sizes: [128, 192, 256],
        modes: ['GCM', 'CBC', 'CTR'],
        data_sizes: [1024, 10240, 102400, 1048576],
        iterations: 100
      })
      setResult({ benchmark: res.data.results })
    } catch (err) {
      setError(err.response?.data?.detail || err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="card">
      <h2><Key className="icon" size={20} /> AES Encryption</h2>
      
      <div className="form-group">
        <label className="label">Plaintext</label>
        <textarea 
          className="input mono" 
          value={plaintext} 
          onChange={(e) => setPlaintext(e.target.value)}
          rows={3}
          placeholder="Enter text to encrypt..."
        />
      </div>

      <div className="form-row">
        <div className="form-group">
          <label className="label">Key Size</label>
          <select className="input" value={keySize} onChange={(e) => setKeySize(parseInt(e.target.value))}>
            <option value={128}>128 bits</option>
            <option value={192}>192 bits</option>
            <option value={256}>256 bits</option>
          </select>
        </div>
        <div className="form-group">
          <label className="label">Mode</label>
          <select className="input" value={mode} onChange={(e) => setMode(e.target.value)}>
            <option value="GCM">GCM (Authenticated)</option>
            <option value="CBC">CBC</option>
            <option value="CTR">CTR</option>
          </select>
        </div>
      </div>

      <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
        <button className="btn btn-primary" onClick={handleEncrypt} disabled={loading}>
          <Hash size={16} /> Encrypt
        </button>
        <button className="btn btn-secondary" onClick={handleBenchmark} disabled={loading}>
          <BarChart2 size={16} /> Benchmark
        </button>
      </div>

      {loading && <div className="loading"><div className="spinner" />Processing...</div>}

      {error && <div className="error-message">{error}</div>}

      {result && !result.benchmark && (
        <div className="result-card" style={{ marginTop: '16px' }}>
          <div className="result-header">
            <span className="result-title">Encryption Result</span>
            <span className="badge badge-success">{result.mode}</span>
          </div>
          <div className="result-metrics">
            <MetricCard label="Encryption Time" value={result.encryption_time_ms.toFixed(2)} unit=" ms" icon={Zap} color="var(--accent)" />
            <MetricCard label="Key Size" value={result.key_size} unit=" bits" icon={Key} color="var(--success)" />
            <MetricCard label="IV Length" value={result.iv.length * 8} unit=" bits" icon={Hash} color="var(--warning)" />
          </div>
        </div>
      )}

      {result?.benchmark && (
        <div style={{ marginTop: '16px' }}>
          <h3 style={{ marginBottom: '12px', color: 'var(--fg-secondary)' }}>Benchmark Results (100 iterations)</h3>
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Configuration</th>
                  <th>Avg Encrypt (ms)</th>
                  <th>Avg Decrypt (ms)</th>
                  <th>Throughput (MB/s)</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(result.benchmark).map(([key, data]) => (
                  <tr key={key}>
                    <td className="mono">{key}</td>
                    {data[1048576] ? (
                      <>
                        <td>{data[1048576].avg_encryption_ms.toFixed(2)}</td>
                        <td>{data[1048576].avg_decryption_ms.toFixed(2)}</td>
                        <td>{data[1048576].throughput_mbps.toFixed(2)}</td>
                      </>
                    ) : (
                      <>
                        <td colSpan={3} style={{ color: 'var(--fg-muted)' }}>No 1MB data</td>
                      </>
                    )}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}

function EdDSAPanel() {
  const [message, setMessage] = useState('Document to sign')
  const [curve, setCurve] = useState('Ed25519')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSign = async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await api.post('/eddsa/sign', { message, curve })
      setResult(res.data)
    } catch (err) {
      setError(err.response?.data?.detail || err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleBenchmark = async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await api.post('/eddsa/benchmark', {
        curves: ['Ed25519', 'Ed448'],
        message_sizes: [32, 64, 128, 256, 512, 1024],
        iterations: 100
      })
      setResult({ benchmark: res.data.results })
    } catch (err) {
      setError(err.response?.data?.detail || err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="card">
      <h2><Zap className="icon" size={20} /> EdDSA Signatures</h2>
      
      <div className="form-group">
        <label className="label">Message</label>
        <textarea 
          className="input mono" 
          value={message} 
          onChange={(e) => setMessage(e.target.value)}
          rows={3}
          placeholder="Enter message to sign..."
        />
      </div>

      <div className="form-group">
        <label className="label">Curve</label>
        <select className="input" value={curve} onChange={(e) => setCurve(e.target.value)}>
          <option value="Ed25519">Ed25519 (128-bit security, 64-byte sig)</option>
          <option value="Ed448">Ed448 (224-bit security, 114-byte sig)</option>
        </select>
      </div>

      <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
        <button className="btn btn-primary" onClick={handleSign} disabled={loading}>
          <Zap size={16} /> Sign
        </button>
        <button className="btn btn-secondary" onClick={handleBenchmark} disabled={loading}>
          <BarChart2 size={16} /> Benchmark
        </button>
      </div>

      {loading && <div className="loading"><div className="spinner" />Processing...</div>}
      {error && <div className="error-message">{error}</div>}

      {result && !result.benchmark && (
        <div className="result-card" style={{ marginTop: '16px' }}>
          <div className="result-header">
            <span className="result-title">Signature Generated</span>
            <span className="badge badge-success">{result.curve}</span>
          </div>
          <div className="result-metrics">
            <MetricCard label="Sign Time" value={result.signing_time_ms.toFixed(2)} unit=" ms" icon={Zap} color="var(--accent)" />
            <MetricCard label="Verify Time" value={result.verification_time_ms.toFixed(2)} unit=" ms" icon={CheckCircle} color="var(--success)" />
            <MetricCard label="Sig Size" value={result.signature.length * 3 / 4} unit=" bytes" icon={Hash} color="var(--warning)" />
          </div>
          <div style={{ marginTop: '12px' }}>
            <label className="label">Signature (base64)</label>
            <input 
              className="input mono" 
              value={result.signature} 
              readOnly 
              onClick={(e) => e.target.select()}
            />
          </div>
        </div>
      )}

      {result?.benchmark && (
        <div style={{ marginTop: '16px' }}>
          <h3 style={{ marginBottom: '12px', color: 'var(--fg-secondary)' }}>Benchmark Results (100 iterations)</h3>
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Curve</th>
                  <th>Avg Sign (ms)</th>
                  <th>Avg Verify (ms)</th>
                  <th>Signatures/sec</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(result.benchmark).map(([key, data]) => (
                  <tr key={key}>
                    <td className="mono">{key}</td>
                    {data[1024] ? (
                      <>
                        <td>{data[1024].avg_signing_ms.toFixed(2)}</td>
                        <td>{data[1024].avg_verification_ms.toFixed(2)}</td>
                        <td>{formatNumber(data[1024].signatures_per_second)}</td>
                      </>
                    ) : (
                      <>
                        <td colSpan={3} style={{ color: 'var(--fg-muted)' }}>No 1KB data</td>
                      </>
                    )}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}

function HyperledgerPanel() {
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleBenchmark = async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await api.post('/hyperledger/benchmark', {
        operations: ['invoke', 'query'],
        iterations: 50
      })
      setResult(res.data.results)
    } catch (err) {
      setError(err.response?.data?.detail || err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="card">
      <h2><Database className="icon" size={20} /> Hyperledger Fabric</h2>
      
      <p style={{ color: 'var(--fg-muted)', marginBottom: '16px', fontSize: '14px' }}>
        Simulated Fabric network: 3 orgs, 2 peers/org, Raft consensus
      </p>

      <button className="btn btn-primary" onClick={handleBenchmark} disabled={loading}>
        {loading ? (
          <>
            <Loader2 className="spinner" size={16} /> Running...
          </>
        ) : (
          <>
            <Play size={16} /> Run Benchmark
          </>
        )}
      </button>

      {error && <div className="error-message" style={{ marginTop: '16px' }}>{error}</div>}

      {result && (
        <div style={{ marginTop: '16px' }}>
          <h3 style={{ marginBottom: '12px', color: 'var(--fg-secondary)' }}>Benchmark Results (50 iterations)</h3>
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Operation</th>
                  <th>Avg Latency (ms)</th>
                  <th>Throughput (TPS)</th>
                  <th>Success Rate</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(result).map(([op, data]) => (
                  <tr key={op}>
                    <td className="mono">{op}</td>
                    <td>{data.avg_latency_ms?.toFixed(2) || 'N/A'}</td>
                    <td>{data.avg_throughput_tps?.toFixed(0) || 'N/A'}</td>
                    <td>
                      <span className="badge badge-success">
                        {(data.success_rate * 100).toFixed(1)}%
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}

function SecurityPanel() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [activeTab, setActiveTab] = useState('aes')

  const tabs = [
    { id: 'aes', label: 'AES', icon: Key },
    { id: 'eddsa', label: 'EdDSA', icon: Zap },
    { id: 'hyperledger', label: 'Hyperledger', icon: Database },
    { id: 'critical', label: 'Critical', icon: AlertTriangle }
  ]

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'very_high': return 'badge-error'
      case 'high': return 'badge-error'
      case 'medium': return 'badge-warning'
      case 'low': return 'badge-info'
      default: return 'badge-info'
    }
  }

  const renderFindings = (findings) => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
      {findings.map((f, i) => (
        <div key={i} className="result-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '8px' }}>
            <div>
              <span className={`badge ${getSeverityColor(f.severity)}`}>{f.severity.replace('_', ' ')}</span>
              <span className="badge badge-info" style={{ marginLeft: '8px' }}>{f.category}</span>
            </div>
          </div>
          <p style={{ color: 'var(--fg-secondary)', marginBottom: '8px' }}>{f.description}</p>
          <p style={{ color: 'var(--accent)', fontSize: '13px' }}>
            <strong>Recommendation:</strong> {f.recommendation}
          </p>
        </div>
      ))}
    </div>
  )

  const fetchSecurity = async () => {
    setLoading(true)
    try {
      const res = await api.get('/security/analyze')
      setData(res.data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchSecurity()
  }, [])

  if (loading) return <div className="loading"><div className="spinner" />Loading security analysis...</div>

  return (
    <div className="card" style={{ gridColumn: '1 / -1' }}>
      <h2><Lock className="icon" size={20} /> Security Analysis</h2>
      
      <div className="tabs">
        {tabs.map(tab => (
          <button
            key={tab.id}
            className={`tab ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => setActiveTab(tab.id)}
          >
            <tab.icon size={16} style={{ marginRight: '6px' }} />
            {tab.label}
          </button>
        ))}
      </div>

      <div className="tab-panel" style={{ display: activeTab === 'aes' ? 'block' : 'none' }}>
        {data?.aes && renderFindings(data.aes.findings)}
      </div>
      <div className="tab-panel" style={{ display: activeTab === 'eddsa' ? 'block' : 'none' }}>
        {data?.eddsa && renderFindings(data.eddsa.findings)}
      </div>
      <div className="tab-panel" style={{ display: activeTab === 'hyperledger' ? 'block' : 'none' }}>
        {data?.hyperledger && renderFindings(data.hyperledger.findings)}
      </div>
      <div className="tab-panel" style={{ display: activeTab === 'critical' ? 'block' : 'none' }}>
        {data?.critical_findings && renderFindings(data.critical_findings)}
      </div>
    </div>
  )
}

const ResultsDisplay = ({ result }) => {
  if (!result) return <div>No results available</div>

  return (
    <div>
      <h4 style={{ marginBottom: '16px', color: 'var(--accent)' }}>AES Results</h4>
      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>Configuration</th>
              <th>Avg Encrypt (ms)</th>
              <th>Avg Decrypt (ms)</th>
              <th>Throughput (MB/s)</th>
            </tr>
          </thead>
          <tbody>
            {Object.entries(result.aes || {}).map(([key, data]) => (
              <tr key={key}>
                <td className="mono">{key}</td>
                {data[1048576] ? (
                  <>
                    <td>{data[1048576].avg_encryption_ms.toFixed(2)}</td>
                    <td>{data[1048576].avg_decryption_ms.toFixed(2)}</td>
                    <td>{data[1048576].throughput_mbps.toFixed(2)}</td>
                  </>
                ) : (
                  <td colSpan={3} style={{ color: 'var(--fg-muted)' }}>No 1MB data</td>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <h4 style={{ marginTop: '24px', marginBottom: '16px', color: 'var(--accent)' }}>EdDSA Results</h4>
      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>Curve</th>
              <th>Avg Sign (ms)</th>
              <th>Avg Verify (ms)</th>
              <th>Signatures/sec</th>
            </tr>
          </thead>
          <tbody>
            {Object.entries(result.eddsa || {}).map(([key, data]) => (
              <tr key={key}>
                <td className="mono">{key}</td>
                {data[1024] ? (
                  <>
                    <td>{data[1024].avg_signing_ms.toFixed(2)}</td>
                    <td>{data[1024].avg_verification_ms.toFixed(2)}</td>
                    <td>{data[1024].signatures_per_second.toFixed(0)}</td>
                  </>
                ) : (
                  <td colSpan={3} style={{ color: 'var(--fg-muted)' }}>No 1KB data</td>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <h4 style={{ marginTop: '24px', marginBottom: '16px', color: 'var(--accent)' }}>Hyperledger Results</h4>
      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>Operation</th>
              <th>Avg Latency (ms)</th>
              <th>Throughput (TPS)</th>
              <th>Success Rate</th>
            </tr>
          </thead>
          <tbody>
            {Object.entries(result.hyperledger || {}).map(([op, data]) => (
              <tr key={op}>
                <td className="mono">{op}</td>
                <td>{data.avg_latency_ms?.toFixed(2) || 'N/A'}</td>
                <td>{data.avg_throughput_tps?.toFixed(0) || 'N/A'}</td>
                <td>
                  <span className="badge badge-success">
                    {(data.success_rate * 100).toFixed(1)}%
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <h4 style={{ marginTop: '24px', marginBottom: '16px', color: 'var(--accent)' }}>Recommendations</h4>
      <ul style={{ paddingLeft: '20px' }}>
        {(result.comparative?.recommendations || []).map((rec, i) => (
          <li key={i} style={{ marginBottom: '8px', color: 'var(--fg-secondary)' }}>{rec}</li>
        ))}
      </ul>
    </div>
  )
}
function FullBenchmarkPanel() {
  const [jobs, setJobs] = useState([])
  const [loading, setLoading] = useState(false)
  const [iterations, setIterations] = useState(100)
  const [selectedJob, setSelectedJob] = useState(null)
  const pollInterval = useRef(null)

  useEffect(() => {
    fetchJobs()
    pollInterval.current = setInterval(fetchJobs, 2000)
    return () => clearInterval(pollInterval.current)
  }, [])

  const fetchJobs = async () => {
    try {
      const res = await api.get('/benchmarks')
      setJobs(res.data.jobs)
    } catch (err) {
      console.error(err)
    }
  }

  const viewJobResults = async (jobId) => {
    try {
      const res = await api.get(`/benchmarks/${jobId}`)
      setSelectedJob(res.data)
    } catch (err) {
      console.error(err)
      alert('Failed to fetch results: ' + err.message)
    }
  }

  const closeResults = () => {
    setSelectedJob(null)
  }

  const startBenchmark = async () => {
    setLoading(true)
    try {
      const res = await api.post('/benchmarks/run', {
        iterations,
        warmup_iterations: 10,
        hl_iterations: 20
      })
      fetchJobs()
    } catch (err) {
      alert(err.response?.data?.detail || err.message)
    } finally {
      setLoading(false)
    }
  }

  const getJobStatus = (job) => {
    if (job.status === 'completed') return <span className="badge badge-success">Completed</span>
    if (job.status === 'running') return <span className="badge badge-warning">Running</span>
    if (job.status === 'failed') return <span className="badge badge-error">Failed</span>
    return <span className="badge badge-info">Queued</span>
  }

  // Results Modal
  if (selectedJob) {
    return (
      <div className="modal-overlay" onClick={closeResults}>
        <div className="modal" onClick={(e) => e.stopPropagation()}>
          <div className="modal-header">
            <h3>Benchmark Results - {selectedJob.job_id.slice(0, 8)}...</h3>
            <button className="modal-close" onClick={closeResults}>&times;</button>
          </div>
          <div className="modal-body">
            {selectedJob.error ? (
              <div className="error-message">{selectedJob.error}</div>
            ) : selectedJob.result ? (
              <ResultsDisplay result={selectedJob.result} />
            ) : (
              <div className="loading"><div className="spinner" />Loading results...</div>
            )}
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="card" style={{ gridColumn: '1 / -1' }}>
      <h2><Cpu className="icon" size={20} /> Full Benchmark Suite</h2>
      
      <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '24px', flexWrap: 'wrap' }}>
        <div className="form-group" style={{ marginBottom: 0 }}>
          <label className="label">Iterations</label>
          <input
            type="number"
            className="input mono"
            value={iterations}
            onChange={(e) => setIterations(Math.max(10, Math.min(1000, parseInt(e.target.value) || 100)))}
            min={10}
            max={1000}
            style={{ width: '120px' }}
          />
        </div>
        <button className="btn btn-primary" onClick={startBenchmark} disabled={loading}>
          {loading ? <Loader2 className="spinner" size={16} /> : <Play size={16} />}
          Start Full Benchmark
        </button>
      </div>

      <div className="job-list">
        {jobs.length === 0 ? (
          <p style={{ color: 'var(--fg-muted)', textAlign: 'center', padding: '40px' }}>
            No benchmark jobs yet. Click "Start Full Benchmark" to run comprehensive tests.
          </p>
        ) : (
          jobs.map(job => (
            <div key={job.job_id} className="job-item">
              <div className="job-info">
                <span className="job-id">{job.job_id.slice(0, 8)}...</span>
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px', fontSize: '13px' }}>
                  {getJobStatus(job)}
                  <span style={{ color: 'var(--fg-muted)' }}>
                    {job.progress > 0 ? `${Math.round(job.progress * 100)}%` : 'Pending'}
                  </span>
                </div>
              </div>
              {job.status === 'completed' && (
                <button className="btn btn-secondary" style={{ fontSize: '12px', padding: '6px 12px' }}>
                  <ExternalLink size={14} /> View Results
                </button>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  )
}

function App() {
  const [health, setHealth] = useState(null)
  const [apiError, setApiError] = useState(null)

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const res = await healthApi.get('/health')
        setHealth(res.data)
        setApiError(null)
      } catch (err) {
        setHealth({ status: 'error' })
        setApiError(err.message)
      }
    }
    checkHealth()
    const interval = setInterval(checkHealth, 30000)
    return () => clearInterval(interval)
  }, [])

  // Show error banner if API is unreachable
  if (health?.status === 'error') {
    return (
      <div className="container" style={{ paddingTop: '60px', textAlign: 'center' }}>
        <div className="card" style={{ maxWidth: '600px', margin: '0 auto' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '12px', marginBottom: '16px' }}>
            <WifiOff size={48} style={{ color: 'var(--error)' }} />
            <h2 style={{ color: 'var(--error)' }}>Cannot Connect to Backend</h2>
          </div>
          <p style={{ color: 'var(--fg-secondary)', marginBottom: '24px' }}>
            The frontend cannot reach the backend API at <code>http://localhost:8000</code>.
          </p>
          <div style={{ textAlign: 'left', background: 'var(--bg-primary)', padding: '16px', borderRadius: '8px', marginBottom: '24px', fontSize: '13px' }}>
            <strong>Troubleshooting:</strong>
            <ul style={{ marginTop: '8px', paddingLeft: '20px' }}>
              <li>Ensure backend is running: <code>cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000</code></li>
              <li>Check backend health: <a href="http://localhost:8000/health" target="_blank" rel="noopener">http://localhost:8000/health</a></li>
              <li>Check browser console (F12) for CORS or network errors</li>
              <li>Restart frontend: <code>cd frontend && npm run dev</code></li>
            </ul>
          </div>
          <button className="btn btn-primary" onClick={() => window.location.reload()}>
            <RefreshCw size={16} /> Retry Connection
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="container">
      <header className="header">
        <h1><Shield className="icon" size={32} /> CloudShield AI</h1>
        <div className="status">
          <span className="status-dot" style={{ background: health?.status === 'healthy' ? 'var(--success)' : 'var(--error)' }} />
          {health?.status === 'healthy' ? 'API Connected' : 'API Disconnected'}
        </div>
      </header>

      {apiError && (
        <div className="error-message" style={{ marginBottom: '24px' }}>
          <Bug size={16} style={{ marginRight: '8px', verticalAlign: 'middle' }} />
          API Error: {apiError} — Check console (F12) for details
        </div>
      )}

      <div className="grid">
        <AESPanel />
        <EdDSAPanel />
        <HyperledgerPanel />
      </div>

      <SecurityPanel />
      <FullBenchmarkPanel />
    </div>
  )
}

function AppWithErrorBoundary() {
  return (
    <ErrorBoundary>
      <App />
    </ErrorBoundary>
  )
}

export default AppWithErrorBoundary