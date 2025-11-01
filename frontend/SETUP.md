# Frontend Setup Guide

## Quick Start

### Windows

```bash
cd frontend
npm install
npm run dev
```

### Linux/Mac

```bash
cd frontend
npm install
npm run dev
```

## Installation Steps

1. **Install Node.js**
   - Download from https://nodejs.org/
   - Verify installation: `node --version` (should be 18+)

2. **Install Dependencies**
   ```bash
   cd frontend
   npm install
   ```

3. **Start Backend API**
   - The frontend requires the backend API to be running
   - In a separate terminal:
   ```bash
   cd ..
   python run_api.py
   ```

4. **Start Frontend Dev Server**
   ```bash
   npm run dev
   ```

5. **Open Browser**
   - Navigate to http://localhost:3000
   - You should see the Macro-Aware Earnings Intelligence interface

## Troubleshooting

### Port 3000 already in use
```bash
# Change port in vite.config.js or kill the process
npx kill-port 3000
npm run dev
```

### API Connection Issues
- Ensure backend is running at http://localhost:8000
- Check CORS settings in backend/api.py
- Verify API_BASE_URL in frontend/src/api.js

### Build Errors
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Tailwind Not Working
```bash
# Rebuild Tailwind
npx tailwindcss -i ./src/index.css -o ./dist/output.css
```

## Development Tips

- **Hot Reload**: Vite provides instant hot module replacement
- **API Proxy**: Vite proxies `/api/*` requests to backend
- **Dark Mode**: Default is dark mode (Bloomberg Terminal style)
- **Console Logs**: Check browser console for API errors

## Production Deployment

### Build
```bash
npm run build
```

### Preview Build
```bash
npm run preview
```

### Deploy
The `dist/` folder can be deployed to:
- Netlify
- Vercel
- GitHub Pages
- AWS S3 + CloudFront
- Any static hosting service

Remember to set the `VITE_API_URL` environment variable to your production API URL.
