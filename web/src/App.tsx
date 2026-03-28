import { useState, useEffect, useMemo } from 'react'
import Fuse from 'fuse.js'
import { Search, Github, Terminal, Copy, Check, Filter, X, AlertCircle } from 'lucide-react'
import { z } from 'zod'
import './App.css'

// --- Types & Schemas ---

const PromptMetadataSchema = z.object({
  name: z.string(),
  display_name: z.string(),
  description: z.string(),
  args_description: z.string(),
  version: z.string(),
  last_updated: z.string(),
  tags: z.array(z.string()),
  sensitive: z.boolean(),
  category: z.string().nullable().transform(val => val ?? 'general'),
  path: z.string(),
  prompt: z.string().optional().default(''),
  concepts: z.array(z.string()).optional().default([]),
})

type PromptMetadata = z.infer<typeof PromptMetadataSchema>

interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: string
}

// --- Custom Hooks ---

function usePromptSearch(prompts: PromptMetadata[], searchQuery: string, selectedCategory: string | null) {
  const fuse = useMemo(() => new Fuse(prompts, {
    keys: [
      { name: 'name', weight: 0.5 },
      { name: 'description', weight: 0.2 },
      { name: 'tags', weight: 0.1 },
      { name: 'concepts', weight: 0.2 }
    ],
    threshold: 0.3
  }), [prompts])

  return useMemo(() => {
    let result = searchQuery 
      ? fuse.search(searchQuery).map(r => r.item)
      : prompts

    if (selectedCategory) {
      result = result.filter(p => p.category === selectedCategory)
    }
    return result
  }, [fuse, prompts, searchQuery, selectedCategory])
}

// --- Main Component ---

function App() {
  const [prompts, setPrompts] = useState<PromptMetadata[]>([])
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null)
  const [selectedPrompt, setSelectedPrompt] = useState<PromptMetadata | null>(null)
  const [promptArgs, setPromptArgs] = useState('')
  const [debouncedArgs, setDebouncedArgs] = useState('')
  const [copied, setCopied] = useState(false)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const filteredPrompts = usePromptSearch(prompts, searchQuery, selectedCategory)

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedArgs(promptArgs)
    }, 300)
    return () => clearTimeout(timer)
  }, [promptArgs])

  const hydratePrompt = (template: string, args: string): string => {
    if (!template) return ''
    // Use function as second argument to prevent replacement of $ characters in user input
    const replacer = () => args
    let hydrated = template.replace(/\{\{\s*args\s*\}\}/g, replacer)
    hydrated = hydrated.replace(/\{\{\s*code\s*\}\}/g, replacer)
    hydrated = hydrated.replace(/\{\{\s*file\s*\}\}/g, replacer)
    
    // Clean up other placeholders if they aren't provided
    hydrated = hydrated.replace(/\{\{\s*language\s*\}\}/g, 'auto-detected')
    hydrated = hydrated.replace(/\{\{\s*context\s*\}\}/g, '')
    
    return hydrated.trim()
  }

  const handleCopy = (text: string): void => {
    if (!navigator.clipboard) {
      setError('Clipboard API not available. Please use a secure context (HTTPS).')
      return
    }
    void navigator.clipboard.writeText(text)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  useEffect(() => {
    setPromptArgs('')
  }, [selectedPrompt])

  useEffect(() => {
    const loadCatalog = async () => {
      // Use relative path to work in both dev and prod regardless of base URL
      const fetchPath = 'catalog.json'
      
      try {
        const res = await fetch(fetchPath)
        if (!res.ok) {
          throw new Error(`Failed to load catalog: ${res.statusText}`)
        }
        
        const data: unknown = await res.json()
        const result = z.array(PromptMetadataSchema).safeParse(data)
        
        const response: ApiResponse<PromptMetadata[]> = result.success 
          ? { success: true, data: result.data }
          : { success: false, error: 'Catalog data format is invalid' }

        if (response.success && response.data) {
          setPrompts(response.data)
        } else {
          setError(response.error ?? 'Unknown error')
        }
      } catch (err: unknown) {
        const message = err instanceof Error ? err.message : 'An unknown error occurred'
        setError(message)
      } finally {
        setLoading(false)
      }
    }

    void loadCatalog()
  }, [])

  const categories = useMemo(() => {
    const cats = new Set(prompts.map(p => p.category))
    return Array.from(cats).sort()
  }, [prompts])

  if (loading) {
    return (
      <div className="loading-container">
        <Terminal className="animate-pulse" size={48} />
        <p>Loading PromptBook...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="loading-container error">
        <AlertCircle size={48} color="#f85149" />
        <p>{error}</p>
        <button className="btn-github" onClick={() => window.location.reload()}>
          Retry
        </button>
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
          <h2>Prompt Templates</h2>
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
                    {hydratePrompt(selectedPrompt.prompt, debouncedArgs)}
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
