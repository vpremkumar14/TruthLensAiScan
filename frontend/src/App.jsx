import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import ImageDetection from './pages/ImageDetection'
import VideoDetection from './pages/VideoDetection'
import About from './pages/About'

function App() {
  return (
    <Router>
      <div className="min-h-screen w-full bg-dark-900 overflow-hidden">
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/image" element={<ImageDetection />} />
          <Route path="/video" element={<VideoDetection />} />
          <Route path="/about" element={<About />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App