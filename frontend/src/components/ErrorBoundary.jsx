import React from 'react'

/**
 * ErrorBoundary Component
 * Catches React errors and displays a user-friendly error message
 */
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false, error: null, errorInfo: null }
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error }
  }

  componentDidCatch(error, errorInfo) {
    console.error('🚨 React Error Boundary caught an error:', error)
    console.error('🚨 Error Info:', errorInfo)
    console.error('🚨 Component Stack:', errorInfo.componentStack)
    this.setState({ errorInfo })
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-terminal-bg flex items-center justify-center p-6">
          <div className="max-w-2xl w-full bg-terminal-red bg-opacity-10 border border-terminal-red rounded-lg p-8">
            <h1 className="text-2xl font-bold text-terminal-red mb-4">
              ⚠️ Something Went Wrong
            </h1>
            <p className="text-terminal-text mb-4">
              The application encountered an error. Check the browser console (F12) for detailed error information.
            </p>

            {/* Error Message */}
            <div className="bg-terminal-bg p-4 rounded mb-4">
              <p className="text-sm text-terminal-text-dim mb-2">Error Message:</p>
              <pre className="text-xs text-terminal-red overflow-auto">
                {this.state.error?.toString()}
              </pre>
            </div>

            {/* Component Stack (collapsed by default) */}
            {this.state.errorInfo && (
              <details className="bg-terminal-bg p-4 rounded mb-4">
                <summary className="text-sm text-terminal-text-dim cursor-pointer hover:text-terminal-orange">
                  Component Stack (click to expand)
                </summary>
                <pre className="text-xs text-terminal-text-dim mt-2 overflow-auto max-h-40">
                  {this.state.errorInfo.componentStack}
                </pre>
              </details>
            )}

            {/* Action Buttons */}
            <div className="flex gap-3">
              <button
                onClick={() => window.location.reload()}
                className="px-4 py-2 bg-terminal-orange text-white rounded hover:bg-opacity-80 transition-colors"
              >
                Reload Page
              </button>
              <button
                onClick={() => this.setState({ hasError: false, error: null, errorInfo: null })}
                className="px-4 py-2 bg-terminal-border text-terminal-text rounded hover:bg-terminal-text-dim transition-colors"
              >
                Try Again
              </button>
            </div>

            {/* Help Text */}
            <div className="mt-6 pt-4 border-t border-terminal-border">
              <p className="text-xs text-terminal-text-dim">
                If this error persists:
              </p>
              <ul className="text-xs text-terminal-text-dim mt-2 space-y-1 list-disc list-inside">
                <li>Open browser console (F12) and check for errors</li>
                <li>Verify backend is running on http://localhost:8000</li>
                <li>Check network tab for failed API requests</li>
              </ul>
            </div>
          </div>
        </div>
      )
    }

    return this.props.children
  }
}

export default ErrorBoundary
