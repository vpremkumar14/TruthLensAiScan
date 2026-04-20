import { useState } from 'react'
import { motion } from 'framer-motion'
import FileUpload from '../components/FileUpload'
import ResultCard from '../components/ResultCard'
import LoadingSpinner from '../components/LoadingSpinner'
import { detectVideo } from '../utils/api'
import robotBg from '../assets/hero-bg.png'

const VideoDetection = () => {
  const [file, setFile] = useState(null)
  const [preview, setPreview] = useState(null)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleFileSelect = async (selectedFile) => {
    if (!selectedFile) return

    setFile(selectedFile)
    setError(null)
    setResult(null)

    // Preview video
    const url = URL.createObjectURL(selectedFile)
    setPreview(url)

    // API call
    setLoading(true)
    try {
      const data = await detectVideo(selectedFile)
      setResult(data)
    } catch (err) {
      setError(err.message || 'Error analyzing video. Please try again.')
      console.error('Error:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-dark-900 py-10 md:py-12 px-4 md:px-8 relative">

      {/* ✅ FIXED BACKGROUND (LOCKED HEIGHT) */}
      <div className="absolute top-0 left-0 w-full h-screen z-0 pointer-events-none">

        {/* Gradient */}
        <div className="absolute inset-0 bg-gradient-to-r from-dark-900 via-dark-900/90 to-transparent"></div>

        {/* Robot Image */}
        <div
          className="absolute inset-0 opacity-30"
          style={{
            backgroundImage: `url(${robotBg})`,
            backgroundPosition: 'right center',
            backgroundRepeat: 'no-repeat',
            backgroundSize: 'contain',
          }}
        ></div>
      </div>

      <div className="max-w-6xl mx-auto px-2 md:px-6 relative z-10">

        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex flex-col items-center text-center mb-10 md:mb-12"
        >
          <h1 className="text-3xl md:text-5xl font-bold mb-3 md:mb-4 gradient-text">
            Video Detection
          </h1>

          <p className="text-sm md:text-base text-gray-400 max-w-xl">
            Upload a video to detect deepfake content using AI analysis
          </p>
        </motion.div>

        {/* Upload */}
        <FileUpload
          onFileSelect={handleFileSelect}
          accept="video/*"
          loading={loading}
        />

        {/* File Info */}
        {file && (
          <div className="glass p-4 md:p-6 rounded-xl mt-6 max-w-2xl mx-auto text-center">
            <p className="font-semibold text-sm md:text-base">{file.name}</p>
            <p className="text-xs md:text-sm text-gray-400">
              {(file.size / 1024 / 1024).toFixed(2)} MB
            </p>
          </div>
        )}

        {/* Loading */}
        {loading && <LoadingSpinner />}

        {/* Error */}
        {error && (
          <div className="text-red-400 mt-4 text-center text-sm md:text-base">
            ⚠ {error}
          </div>
        )}

        {/* Result */}
        {result && !loading && (
          <ResultCard
            prediction={result.prediction}
            confidence={result.confidence}
            explanation={result.explanation}
            explanationImage={result.explanation_image}
            imageUrl={preview}
            type="video"
          />
        )}

      </div>
    </div>
  )
}

export default VideoDetection