# AgriSaarthi Web Application

A modern, responsive web interface for the AgriSaarthi AI-powered agricultural assistant.

## Features

- 🌾 **Category-based Chat**: Choose from 5 specialized agricultural categories
- 🔄 **Streaming Responses**: Real-time streaming chat responses
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile devices
- 🎨 **Modern UI**: Built with Next.js 15 and Tailwind CSS
- ⚡ **Fast Performance**: Optimized with Next.js App Router

## Categories Available

1. **Crop Info** 🌾 - Crop selection, management, and science-based farming advice
2. **Fertilizers** 🌱 - Fertilizer recommendations, application rates, and management
3. **Market Prices** 📊 - Current market prices, trends, and selling strategies
4. **Government Schemes** 🏛️ - Information about agricultural schemes and subsidies
5. **Other** 🔍 - General agricultural advice and farming best practices

## Tech Stack

- **Frontend**: Next.js 15 with App Router
- **Styling**: Tailwind CSS
- **Language**: TypeScript
- **State Management**: React Hooks
- **API Integration**: Fetch API with streaming support

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn
- AgriSaarthi Backend API running on `http://localhost:8000`

### Installation

1. Install dependencies:

   ```bash
   npm install
   # or
   yarn install
   ```

2. Start the development server:

   ```bash
   npm run dev
   # or
   yarn dev
   ```

3. Open [http://localhost:3000](http://localhost:3000) in your browser

## API Endpoints Used

- `GET /agents/categories` - Fetch available agent categories
- `POST /chat` - Non-streaming chat responses
- `POST /chat/stream` - Streaming chat responses

## Project Structure

```
web/
├── app/
│   ├── globals.css          # Global styles and Tailwind imports
│   ├── layout.tsx           # Root layout component
│   └── page.tsx             # Main chat interface
├── tailwind.config.ts       # Tailwind CSS configuration
├── postcss.config.js        # PostCSS configuration
└── package.json             # Dependencies and scripts
```

## Features

### Chat Interface

- **Real-time Chat**: Interactive chat with AI agricultural experts
- **Category Selection**: Choose specialized agents for different topics
- **Streaming Toggle**: Switch between streaming and regular responses
- **Chat History**: View all previous conversations
- **Auto-scroll**: Automatically scrolls to latest messages

### Responsive Design

- **Mobile First**: Optimized for mobile devices
- **Grid Layout**: Responsive grid system for different screen sizes
- **Touch Friendly**: Optimized for touch interactions

### User Experience

- **Loading States**: Visual feedback during API calls
- **Error Handling**: Graceful error handling and user feedback
- **Smooth Animations**: CSS transitions and animations
- **Accessibility**: Proper ARIA labels and keyboard navigation

## Customization

### Colors

The application uses a custom color palette defined in `tailwind.config.ts`:

- Primary colors (green theme for agriculture)
- Secondary colors (gray theme for UI elements)

### Icons

Each category has a unique emoji icon that can be customized in the `getCategoryIcon` function.

### Styling

All styling is done with Tailwind CSS utility classes for easy customization.

## Development

### Adding New Categories

1. Add the category to the backend API
2. Update the `getCategoryIcon` function in `page.tsx`
3. Add appropriate styling in the category selection sidebar

### Modifying the Chat Interface

The chat interface is built with reusable components and can be easily modified by updating the JSX structure and Tailwind classes.

## Deployment

### Build for Production

```bash
npm run build
npm start
```

### Environment Variables

Ensure your backend API URL is correctly configured in the fetch calls.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is part of the AgriSaarthi agricultural assistance platform.