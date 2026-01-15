/**
 * Example React Components for Spam Classifier Frontend Integration
 * 
 * These are ready-to-use components that demonstrate:
 * - User authentication (signup/signin)
 * - API key management
 * - Spam detection functionality
 * 
 * Copy these to your project and customize as needed.
 */

import { useState, useEffect } from 'react';
import { authApi, spamApi, handleApiError, ApiKey, AnalysisResult } from './api';

// ============================================
// 1. SIGNUP FORM COMPONENT
// ============================================

export function SignupForm() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState(false);
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setSuccess(false);
        setLoading(true);

        // Validate password length
        if (password.length < 6) {
            setError('Password must be at least 6 characters');
            setLoading(false);
            return;
        }

        try {
            const response = await authApi.signup({ email, password });
            setSuccess(true);
            console.log('User created:', response.data.user);
            alert('Account created! Please sign in.');
        } catch (err) {
            setError(handleApiError(err));
        } finally {
            setLoading(false);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="auth-form">
            <h2>Create Account</h2>

            <div className="form-group">
                <label htmlFor="signup-email">Email</label>
                <input
                    id="signup-email"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    placeholder="your@email.com"
                />
            </div>

            <div className="form-group">
                <label htmlFor="signup-password">Password</label>
                <input
                    id="signup-password"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    minLength={6}
                    placeholder="Minimum 6 characters"
                />
            </div>

            {error && <p className="error-message">{error}</p>}
            {success && <p className="success-message">Account created successfully!</p>}

            <button type="submit" disabled={loading}>
                {loading ? 'Creating Account...' : 'Sign Up'}
            </button>

            <p className="form-footer">
                Already have an account? <a href="/login">Sign In</a>
            </p>
        </form>
    );
}

// ============================================
// 2. LOGIN FORM COMPONENT
// ============================================

export function LoginForm() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            const response = await authApi.signin({ email, password });
            const { access_token } = response.data;

            // Store the token
            localStorage.setItem('access_token', access_token);

            // Redirect to dashboard or home
            window.location.href = '/dashboard';
        } catch (err) {
            setError(handleApiError(err));
        } finally {
            setLoading(false);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="auth-form">
            <h2>Sign In</h2>

            <div className="form-group">
                <label htmlFor="login-email">Email</label>
                <input
                    id="login-email"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    placeholder="your@email.com"
                />
            </div>

            <div className="form-group">
                <label htmlFor="login-password">Password</label>
                <input
                    id="login-password"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    placeholder="Your password"
                />
            </div>

            {error && <p className="error-message">{error}</p>}

            <button type="submit" disabled={loading}>
                {loading ? 'Signing In...' : 'Sign In'}
            </button>

            <p className="form-footer">
                Don't have an account? <a href="/signup">Sign Up</a>
            </p>
        </form>
    );
}

// ============================================
// 3. API KEY MANAGEMENT COMPONENT
// ============================================

export function ApiKeyManager() {
    const [apiKeys, setApiKeys] = useState<ApiKey[]>([]);
    const [keyName, setKeyName] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [copiedKey, setCopiedKey] = useState<string | null>(null);

    useEffect(() => {
        loadApiKeys();
    }, []);

    const loadApiKeys = async () => {
        try {
            const response = await authApi.listApiKeys();
            setApiKeys(response.data);
        } catch (err) {
            setError(handleApiError(err));
        }
    };

    const createKey = async () => {
        setLoading(true);
        setError('');

        try {
            const response = await authApi.createApiKey({
                name: keyName || 'Default Key'
            });

            setApiKeys([...apiKeys, response.data]);
            setKeyName('');

            // Auto-copy the new key
            await copyToClipboard(response.data.key);
            alert(`New API Key created and copied to clipboard:\n${response.data.key}`);
        } catch (err) {
            setError(handleApiError(err));
        } finally {
            setLoading(false);
        }
    };

    const revokeKey = async (key: string) => {
        if (!confirm('Are you sure you want to revoke this API key? This action cannot be undone.')) {
            return;
        }

        try {
            await authApi.deleteApiKey(key);
            setApiKeys(apiKeys.filter(k => k.key !== key));
        } catch (err) {
            setError(handleApiError(err));
        }
    };

    const copyToClipboard = async (text: string) => {
        try {
            await navigator.clipboard.writeText(text);
            setCopiedKey(text);
            setTimeout(() => setCopiedKey(null), 2000);
        } catch (err) {
            console.error('Failed to copy to clipboard:', err);
        }
    };

    return (
        <div className="api-key-manager">
            <h2>API Key Management</h2>

            <p className="info-text">
                API keys are required to use the spam detection API. Each key has a rate limit of 5 requests per minute.
            </p>

            {/* Create New Key Section */}
            <div className="create-key-section">
                <h3>Create New API Key</h3>
                <div className="create-key-form">
                    <input
                        type="text"
                        placeholder="Key name (e.g., 'Production App')"
                        value={keyName}
                        onChange={(e) => setKeyName(e.target.value)}
                        maxLength={50}
                    />
                    <button onClick={createKey} disabled={loading}>
                        {loading ? 'Creating...' : '+ Create Key'}
                    </button>
                </div>
            </div>

            {error && <p className="error-message">{error}</p>}

            {/* List Existing Keys */}
            <div className="keys-list-section">
                <h3>Your API Keys ({apiKeys.length})</h3>

                {apiKeys.length === 0 ? (
                    <div className="empty-state">
                        <p>No API keys yet. Create one to get started!</p>
                    </div>
                ) : (
                    <ul className="keys-list">
                        {apiKeys.map((key) => (
                            <li key={key.key} className="key-item">
                                <div className="key-info">
                                    <div className="key-header">
                                        <strong className="key-name">{key.name}</strong>
                                        <small className="key-date">
                                            Created: {new Date(key.created_at).toLocaleDateString()}
                                        </small>
                                    </div>

                                    <div className="key-value">
                                        <code className="key-code">{key.key}</code>
                                        <button
                                            className="copy-btn"
                                            onClick={() => copyToClipboard(key.key)}
                                            title="Copy to clipboard"
                                        >
                                            {copiedKey === key.key ? '✓ Copied' : '📋 Copy'}
                                        </button>
                                    </div>
                                </div>

                                <button
                                    className="revoke-btn"
                                    onClick={() => revokeKey(key.key)}
                                    title="Revoke this key"
                                >
                                    🗑️ Revoke
                                </button>
                            </li>
                        ))}
                    </ul>
                )}
            </div>
        </div>
    );
}

// ============================================
// 4. SPAM DETECTION COMPONENT
// ============================================

interface SpamDetectorProps {
    userApiKey?: string; // Optional: Can be selected from a dropdown
}

export function SpamDetector({ userApiKey }: SpamDetectorProps) {
    const [text, setText] = useState('');
    const [apiKeyInput, setApiKeyInput] = useState(userApiKey || '');
    const [result, setResult] = useState<AnalysisResult | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    // Update internal key when prop changes
    useEffect(() => {
        if (userApiKey) {
            setApiKeyInput(userApiKey);
        }
    }, [userApiKey]);

    const analyzeText = async () => {
        if (!text.trim()) {
            setError('Please enter some text to analyze');
            return;
        }

        if (!apiKeyInput.trim()) {
            setError('Please enter your API key');
            return;
        }

        setLoading(true);
        setError('');
        setResult(null);

        try {
            const response = await spamApi.detectSpam(text, apiKeyInput);
            setResult(response.data);
        } catch (err) {
            setError(handleApiError(err));
        } finally {
            setLoading(false);
        }
    };

    const clearResults = () => {
        setText('');
        setResult(null);
        setError('');
    };

    return (
        <div className="spam-detector">
            <h2>Spam Detection</h2>

            {/* API Key Input (if not provided via props) */}
            {!userApiKey && (
                <div className="form-group">
                    <label htmlFor="api-key-input">API Key</label>
                    <input
                        id="api-key-input"
                        type="text"
                        placeholder="Enter your API key (sc_...)"
                        value={apiKeyInput}
                        onChange={(e) => setApiKeyInput(e.target.value)}
                    />
                    <small>Don't have a key? Create one in API Key Management.</small>
                </div>
            )}

            {/* Text Input */}
            <div className="form-group">
                <label htmlFor="text-input">Text to Analyze</label>
                <textarea
                    id="text-input"
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    placeholder="Paste message, email, or SMS content here..."
                    rows={6}
                    style={{ width: '100%', resize: 'vertical' }}
                />
                <small>{text.length} characters</small>
            </div>

            {/* Action Buttons */}
            <div className="button-group">
                <button
                    onClick={analyzeText}
                    disabled={loading || !text.trim() || !apiKeyInput.trim()}
                    className="primary-btn"
                >
                    {loading ? '🔍 Analyzing...' : '🔍 Check for Spam'}
                </button>

                {(text || result) && (
                    <button onClick={clearResults} className="secondary-btn">
                        Clear
                    </button>
                )}
            </div>

            {/* Error Display */}
            {error && (
                <div className="error-message">
                    <strong>Error:</strong> {error}
                </div>
            )}

            {/* Results Display */}
            {result && (
                <div className={`result-card ${result.is_spam ? 'spam' : 'safe'}`}>
                    <div className="result-header">
                        <h3>
                            {result.is_spam ? '⚠️ Spam Detected' : '✅ Looks Safe'}
                        </h3>
                        <div className="confidence-badge">
                            Confidence: {result.confidence}%
                        </div>
                    </div>

                    <div className="result-body">
                        <h4>Analysis Summary:</h4>
                        <pre className="response-text">{result.response_text}</pre>

                        {/* Detailed Information */}
                        {result.details && Object.keys(result.details).length > 0 && (
                            <details className="result-details">
                                <summary>View Detailed Analysis</summary>
                                <pre className="details-json">
                                    {JSON.stringify(result.details, null, 2)}
                                </pre>
                            </details>
                        )}
                    </div>
                </div>
            )}

            {/* Example Messages */}
            <div className="examples-section">
                <h4>Try These Examples:</h4>
                <ul>
                    <li>
                        <button onClick={() => setText('Congratulations! You won $1000. Click here: http://suspicious-site.com/claim')}>
                            Suspicious Link Example
                        </button>
                    </li>
                    <li>
                        <button onClick={() => setText('Hi mom, just checking in. How are you doing today?')}>
                            Safe Message Example
                        </button>
                    </li>
                </ul>
            </div>
        </div>
    );
}

// ============================================
// 5. LOGOUT BUTTON COMPONENT
// ============================================

export function LogoutButton() {
    const handleLogout = () => {
        if (confirm('Are you sure you want to log out?')) {
            localStorage.removeItem('access_token');
            window.location.href = '/login';
        }
    };

    return (
        <button onClick={handleLogout} className="logout-btn">
            🚪 Logout
        </button>
    );
}

// ============================================
// EXAMPLE CSS (Optional - customize as needed)
// ============================================

const exampleStyles = `
.auth-form {
  max-width: 400px;
  margin: 2rem auto;
  padding: 2rem;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.error-message {
  color: #dc3545;
  background: #f8d7da;
  padding: 0.75rem;
  border-radius: 4px;
  margin: 1rem 0;
}

.success-message {
  color: #155724;
  background: #d4edda;
  padding: 0.75rem;
  border-radius: 4px;
  margin: 1rem 0;
}

.result-card.spam {
  border-left: 4px solid #dc3545;
  background: #fff5f5;
}

.result-card.safe {
  border-left: 4px solid #28a745;
  background: #f0fff4;
}

.confidence-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  background: #007bff;
  color: white;
  border-radius: 12px;
  font-size: 0.875rem;
}
`;
