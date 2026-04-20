import { useState } from 'react'
import { motion } from 'framer-motion'
import FileUpload from '../components/FileUpload'
import ResultCard from '../components/ResultCard'
import LoadingSpinner from '../components/LoadingSpinner'
import { detectImage } from '../utils/api'
import robotBg from '../assets/hero-bg.png'

const ImageDetection = () => {
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

    const reader = new FileReader()
    reader.onloadend = () => {
      setPreview(reader.result)
    }
    reader.readAsDataURL(selectedFile)

    setLoading(true)
    try {
      const data = await detectImage(selectedFile)
      setResult(data)
    } catch (err) {
      setError(err.message || 'Error analyzing image. Please try again.')
      console.error('Error:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-dark-900 py-12 px-4 md:px-8">

      {/* 🔥 FIXED BACKGROUND (WILL NOT CHANGE AFTER UPLOAD) */}
      <div className="fixed inset-0 z-0 pointer-events-none">

        {/* Gradient */}
        <div className="absolute inset-0 bg-gradient-to-r from-dark-900 via-dark-900/90 to-transparent"></div>

        {/* Robot */}
        <div 
          className="absolute inset-0 opacity-30"
          style={{
            backgroundImage: `url(${robotBg})`,
            backgroundPosition: 'right center', // 🔥 better alignment
            backgroundRepeat: 'no-repeat',
            backgroundSize: 'contain',          // 🔥 prevents stretching
          }}
        ></div>

      </div>

      <div className="max-w-6xl mx-auto relative z-10">
        
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl font-bold mb-4 gradient-text">
            Image Detection
          </h1>
          <p className="text-gray-400">
            Upload an image to detect Deepfake content
          </p>
        </motion.div>

        {/* Upload */}
        <FileUpload
          onFileSelect={handleFileSelect}
          accept="image/*"
          loading={loading}
        />

        {/* File Info */}
        {file && (
          <div className="glass p-6 rounded-xl mt-6">
            <p className="font-semibold">{file.name}</p>
            <p className="text-sm text-gray-400">
              {(file.size / 1024 / 1024).toFixed(2)} MB
            </p>
          </div>
        )}

        {/* Loading */}
        {loading && <LoadingSpinner />}

        {/* Error */}
        {error && (
          <div className="text-red-400 mt-4">
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
            type="image"
          />
        )}

      </div>
    </div>
  )
}

export default ImageDetection