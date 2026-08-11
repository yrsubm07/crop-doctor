import { useRef, useState } from 'react'
import './App.css'

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

function App() {
  const inputRef = useRef(null)
  const [file, setFile] = useState(null)
  const [preview, setPreview] = useState('')
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const selectFile = (selected) => {
    if (!selected) return
    if (!['image/jpeg', 'image/png', 'image/webp'].includes(selected.type)) {
      setError('Please choose a JPG, PNG, or WebP image.')
      return
    }
    if (selected.size > 10 * 1024 * 1024) {
      setError('Image must be 10 MB or smaller.')
      return
    }
    setError('')
    setResult(null)
    setFile(selected)
    setPreview(URL.createObjectURL(selected))
  }

  const analyze = async () => {
    if (!file) return
    setLoading(true)
    setError('')
    setResult(null)
    try {
      const body = new FormData()
      body.append('file', file)
      const response = await fetch(`${API_URL}/api/predict`, { method: 'POST', body })
      const data = await response.json()
      if (!response.ok) throw new Error(data.detail || 'Prediction failed.')
      setResult(data)
    } catch (err) {
      setError(err.message || 'Could not reach the Crop Doctor API.')
    } finally {
      setLoading(false)
    }
  }

  const reset = () => {
    setFile(null)
    setPreview('')
    setResult(null)
    setError('')
    if (inputRef.current) inputRef.current.value = ''
  }

  return (
    <main className="app-shell">
      <header className="topbar">
        <div className="brand"><span>🌿</span> Crop Doctor</div>
        <span className="badge">AI LEAF SCREENING</span>
      </header>

      <section className="hero-copy">
        <p className="eyebrow">Farmer-first crop health assistant</p>
        <h1>Upload a leaf.<br /><em>Know what to check.</em></h1>
        <p className="subtitle">Take a clear photo of a crop leaf and get an AI-based disease screening result with confidence and alternative predictions.</p>
      </section>

      <section className="workspace">
        <div className="card upload-card">
          <div className="card-title"><span>01</span><h2>Leaf photo</h2></div>
          <input ref={inputRef} type="file" accept="image/jpeg,image/png,image/webp" hidden onChange={(e) => selectFile(e.target.files?.[0])} />
          {!preview ? (
            <button className="dropzone" onClick={() => inputRef.current?.click()} type="button">
              <span className="upload-icon">↑</span>
              <strong>Choose a leaf photo</strong>
              <small>JPG, PNG or WebP · max 10 MB</small>
            </button>
          ) : (
            <div className="preview-wrap">
              <img src={preview} alt="Selected crop leaf" />
              <button className="change" onClick={() => inputRef.current?.click()} type="button">Change photo</button>
            </div>
          )}
          <div className="tips">
            <strong>📸 Better results</strong>
            <span>Use one leaf, good daylight, and keep the diseased area visible.</span>
          </div>
          {error && <div className="error">{error}</div>}
          <div className="actions">
            <button className="primary" disabled={!file || loading} onClick={analyze} type="button">{loading ? 'Analyzing…' : 'Detect disease →'}</button>
            {file && <button className="secondary" onClick={reset} type="button">Reset</button>}
          </div>
        </div>

        <div className="card result-card">
          <div className="card-title"><span>02</span><h2>Screening result</h2></div>
          {!result && !loading && <div className="empty"><span>🩺</span><strong>Your result will appear here</strong><p>We will identify the most likely crop disease from the uploaded leaf.</p></div>}
          {loading && <div className="empty"><div className="spinner" /><strong>Analyzing leaf…</strong><p>The first run may take longer while the AI model is downloaded.</p></div>}
          {result && (
            <div className="result">
              <div className="result-head"><div><span className="label">MOST LIKELY</span><h3>{result.disease}</h3><p>{result.crop}</p></div><div className="confidence"><b>{result.confidence}%</b><span>confidence</span></div></div>
              <div className="meter"><span style={{ width: `${Math.min(result.confidence, 100)}%` }} /></div>
              <h4>Other possibilities</h4>
              <div className="alternatives">
                {result.predictions.slice(1).map((item) => <div key={item.label}><span>{item.disease}</span><b>{item.confidence}%</b></div>)}
              </div>
              <div className="warning">⚠️ {result.warning}</div>
            </div>
          )}
        </div>
      </section>

      <footer>Crop Doctor is an AI screening tool, not a replacement for professional agricultural diagnosis.</footer>
    </main>
  )
}

export default App
