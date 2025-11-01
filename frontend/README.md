# Fintech AI Frontend

Modern React frontend for the Macro-Aware Earnings Intelligence platform.

## Features

- **Bloomberg Terminal Aesthetic** - Professional dark theme with terminal-inspired design
- **Real-time Analysis** - Analyze earnings calls with AI-powered sentiment analysis
- **Macro Integration** - View market regime and trading recommendations
- **Responsive Design** - Works on desktop and mobile
- **Dark Mode** - Toggle between light and dark themes
- **API Integration** - Seamless connection to FastAPI backend

## Tech Stack

- **React 18** - Modern React with hooks
- **Vite** - Lightning-fast build tool
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client for API requests
- **Recharts** - Charting library (for future visualizations)

## Getting Started

### Prerequisites

- Node.js 18+ installed
- Backend API running at `http://localhost:8000`

### Installation

```bash
cd frontend
npm install
```

### Development

Start the development server:

```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

### Build for Production

```bash
npm run build
```

Built files will be in the `dist/` directory.

### Preview Production Build

```bash
npm run preview
```

## Environment Variables

Create a `.env` file in the `frontend/` directory:

```
VITE_API_URL=http://localhost:8000
```

## Project Structure

```
frontend/
├── src/
│   ├── App.jsx           # Main application component
│   ├── main.jsx          # Application entry point
│   ├── api.js            # API client functions
│   └── index.css         # Global styles + Tailwind
├── public/               # Static assets
├── index.html            # HTML template
├── vite.config.js        # Vite configuration
├── tailwind.config.js    # Tailwind configuration
└── package.json          # Dependencies
```

## API Integration

The frontend communicates with the FastAPI backend via the API client in `src/api.js`:

- `analyzeCompany(ticker)` - Analyze a company by ticker
- `getRecentAnalyses(limit)` - Get recent analyses
- `getCompanies()` - List all companies
- `getCompanyDetails(ticker)` - Get company details
- `checkHealth()` - Check API status

## Styling

The app uses a custom Bloomberg Terminal-inspired color palette:

- **Background**: Pure black (#000000)
- **Primary**: Orange (#ff6b35)
- **Success**: Green (#00c853)
- **Danger**: Red (#ff1744)
- **Warning**: Yellow (#ffc400)
- **Info**: Blue (#004e89)

## Features to Add

- [ ] Historical analysis charts
- [ ] Comparison view for multiple tickers
- [ ] Export analysis to PDF
- [ ] Real-time price updates
- [ ] Backtesting visualizations
- [ ] User authentication
- [ ] Saved watchlists

## License

MIT
