import { useState, useEffect, useMemo } from 'react'
import Fuse from 'fuse.js'
import { Search, Github, Terminal, Copy, Check, Filter, X } from 'lucide-react'
import './App.css'

interface PromptMetadata {
  name: string;
  display_name: string;
  description: string;
  args_description: string;
  version: string;
  last_updated: string;
  tags: string[];
  sensitive: boolean;
  category: string;
  path: string;
  prompt: string;
}

function App() {
  const [prompts, setPrompts] = useState<PromptMetadata[]>([])
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null)
  const [selectedPrompt, setSelectedPrompt] = useState<PromptMetadata | null>(null)
  const [promptArgs, setPromptArgs] = useState('')
  const [copied, setCopied] = useState(false)
  const [loading, setLoading] = useState(true)

  const hydratePrompt = (template: string, args: string) => {
    if (!template) return ''
    // Simple hydration for args
    let hydrated = template.replace(/\{\{\s*args\s*\}\}/g, args)
    hydrated = hydrated.replace(/\{\{\s*code\s*\}\}/g, args)
    hydrated = hydrated.replace(/\{\{\s*file\s*\}\}/g, args)
    
    // Clean up other placeholders if they aren't provided
    hydrated = hydrated.replace(/\{\{\s*language\s*\}\}/g, 'auto-detected')
    hydrated = hydrated.replace(/\{\{\s*context\s*\}\}/g, '')
    
    return hydrated.trim()
  }

  const handleCopy = (text: string) => {
    navigator.clipboard.writeText(text)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  useEffect(() => {
    // Clear args when selected prompt changes
    setPromptArgs('')
  }, [selectedPrompt])

  useEffect(() => {
    // In dev mode, public files are served at the root, but in prod they are under BASE_URL
    const fetchPath = import.meta.env.DEV ? '/catalog.json' : `${import.meta.env.BASE_URL}catalog.json`
    fetch(fetchPath)
      .then(res => res.json())
      .then(data => {
        setPrompts(data)
        setLoading(true) // We'll set it to false after a small delay for smoother transition
        setTimeout(() => setLoading(false), 500)
      })
      .catch(err => {
        console.error('Error fetching catalog:', err)
        setLoading(false)
      })
  }, [])

  const categories = useMemo(() => {
    const cats = new Set(prompts.map(p => p.category))
    return Array.from(cats).sort()
  }, [prompts])

  const fuse = useMemo(() => new Fuse(prompts, {
    keys: ['name', 'description', 'tags', 'category'],
    threshold: 0.3
  }), [prompts])

  const filteredPrompts = useMemo(() => {
    let result = searchQuery 
      ? fuse.search(searchQuery).map(r => r.item)
      : prompts

    if (selectedCategory) {
      result = result.filter(p => p.category === selectedCategory)
    }
    return result
  }, [fuse, prompts, searchQuery, selectedCategory])

  if (loading) {
    return (
      <div className="loading-container">
        <Terminal className="animate-pulse" size={48} />
        <p>Loading PromptBook...</p>
      </div>
    )
  }

  return (
    <div className="app">
      <header className="header">
        <div className="container">
          <div className="logo">
            <Terminal size={32} />
            <h1>PromptBook</h1>
          </div>
          <nav>
            <a href="https://github.com/ronmkr/PromptBook" target="_blank" rel="noreferrer">
              <Github size={24} />
            </a>
          </nav>
        </div>
      </header>

      <main className="container">
        <section className="hero">
          <h2>Expert Prompt Templates</h2>
          <p>Organized, versioned, and ready to use for developers, architects, and data engineers.</p>
          
          <div className="search-container">
            <Search className="search-icon" size={20} />
            <input 
              type="text" 
              placeholder="Search prompts (e.g. refactor, security, rust)..." 
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>

          <div className="categories">
            <button 
              className={selectedCategory === null ? 'active' : ''} 
              onClick={() => setSelectedCategory(null)}
            >
              All
            </button>
            {categories.map(cat => (
              <button 
                key={cat}
                className={selectedCategory === cat ? 'active' : ''}
                onClick={() => setSelectedCategory(cat)}
              >
                {cat}
              </button>
            ))}
          </div>
        </section>

        <section className="prompt-grid">
          {filteredPrompts.length > 0 ? (
            filteredPrompts.map(prompt => (
              <div 
                key={prompt.name} 
                className="prompt-card"
                onClick={() => setSelectedPrompt(prompt)}
              >
                <div className="card-header">
                  <span className="category-tag">{prompt.category}</span>
                  <span className="version-tag">v{prompt.version}</span>
                </div>
                <h3>{prompt.name}</h3>
                <p>{prompt.description}</p>
                <div className="card-footer">
                  <div className="tags">
                    {prompt.tags.slice(0, 3).map(tag => (
                      <span key={tag} className="tag">#{tag}</span>
                    ))}
                  </div>
                </div>
              </div>
            ))
          ) : (
            <div className="no-results">
              <Filter size={48} />
              <p>No prompts found matching your criteria.</p>
            </div>
          )}
        </section>
      </main>

      {selectedPrompt && (
        <div className="modal-overlay" onClick={() => setSelectedPrompt(null)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <button className="close-btn" onClick={() => setSelectedPrompt(null)}>
              <X size={24} />
            </button>
            
            <div className="modal-header">
              <span className="category-tag">{selectedPrompt.category}</span>
              <h2>{selectedPrompt.name}</h2>
              <p className="version-info">Version {selectedPrompt.version} • Updated {selectedPrompt.last_updated}</p>
            </div>

            <div className="modal-body">
              <section>
                <h4>Description</h4>
                <p>{selectedPrompt.description}</p>
              </section>

              <section>
                <h4>{selectedPrompt.args_description || 'Arguments'}</h4>
                <textarea 
                  className="args-input"
                  placeholder={`Enter ${selectedPrompt.args_description?.toLowerCase() || 'arguments'}...`}
                  value={promptArgs}
                  onChange={(e) => setPromptArgs(e.target.value)}
                  rows={3}
                />
              </section>

              <section>
                <h4>Prompt Preview</h4>
                <div className="code-block prompt-preview">
                  <pre>
                    {hydratePrompt(selectedPrompt.prompt, promptArgs)}
                  </pre>
                  <button 
                    className="copy-full-btn"
                    onClick={() => handleCopy(hydratePrompt(selectedPrompt.prompt, promptArgs))}
                  >
                    {copied ? <Check size={16} /> : <Copy size={16} />}
                  </button>
                </div>
              </section>

              <section>
                <h4>Tags</h4>
                <div className="tags">
                  {selectedPrompt.tags.map(tag => (
                    <span key={tag} className="tag">#{tag}</span>
                  ))}
                </div>
              </section>

              <div className="modal-actions">
                <a 
                  href={`https://github.com/ronmkr/PromptBook/blob/main/${selectedPrompt.path}`}
                  target="_blank" 
                  rel="noreferrer"
                  className="btn-github"
                >
                  <Github size={18} /> View Source
                </a>
              </div>
            </div>
          </div>
        </div>
      )}

      <footer className="footer">
        <div className="container">
          <p>© 2026 PromptBook • MIT License</p>
        </div>
      </footer>
    </div>
  )
}

export default App
