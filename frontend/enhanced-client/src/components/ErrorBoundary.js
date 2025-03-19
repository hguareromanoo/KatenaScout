/**
 * Error Boundary Component to catch rendering errors
 */
import React, { Component } from 'react';
import { AlertTriangle } from 'lucide-react';

class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    // Update state so the next render will show the fallback UI
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    // Log the error to the console
    console.error("Error caught by ErrorBoundary:", error, errorInfo);
    this.setState({ errorInfo });
    
    // You could also log this to an error reporting service
    // logErrorToService(error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      // Use custom fallback UI if provided, otherwise use default
      if (this.props.fallback) {
        return this.props.fallback;
      }
      
      // Default fallback UI
      return (
        <div className="bg-red-900 bg-opacity-20 p-6 rounded-lg border border-red-700 m-4">
          <div className="flex items-center mb-4">
            <AlertTriangle className="text-red-500 mr-2" size={24} />
            <h2 className="text-lg font-bold text-red-300">Oops! Algo deu errado</h2>
          </div>
          <p className="text-red-200 mb-4">
            Ocorreu um erro ao renderizar este componente. Detalhes adicionais foram registrados no console.
          </p>
          <button 
            className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded text-white"
            onClick={() => window.location.reload()}
          >
            Recarregar Página
          </button>
          {process.env.NODE_ENV === 'development' && (
            <details className="mt-4 p-2 bg-black bg-opacity-30 rounded">
              <summary className="text-red-300 cursor-pointer">Detalhes Técnicos</summary>
              <pre className="mt-2 p-2 text-xs text-red-300 overflow-auto max-h-60 whitespace-pre-wrap bg-black bg-opacity-50 rounded">
                {this.state.error && this.state.error.toString()}
                {this.state.errorInfo && this.state.errorInfo.componentStack}
              </pre>
            </details>
          )}
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;