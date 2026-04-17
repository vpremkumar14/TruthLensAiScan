import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import robotBg from '../assets/hero-bg.png'

const Home = () => {
  const features = [
    {
      icon: '📸',
      title: 'Image Detection',
      description: 'Analyze single images with advanced deep learning algorithms for detection',
    },
    {
      icon: '🎬',
      title: 'Video Analysis',
      description: 'Frame-by-frame analysis for comprehensive video deepfake detection',
    },
    {
      icon: '⚡',
      title: 'Real-time Processing',
      description: 'Get instant results with GPU-accelerated inference engines',
    },
    {
      icon: '🔍',
      title: 'Detailed Reports',
      description: 'Comprehensive analysis with confidence scores and visual explanations',
    },
  ]

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
      },
    },
  }

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.5 },
    },
  }

  return (
    <div className="min-h-screen bg-dark-900">
      {/* Hero Section with Robot Background */}
      <motion.section
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.8 }}
        className="relative overflow-hidden min-h-screen flex items-center justify-center px-4 md:px-8"
      >
        {/* Background with Robot Image */}
        <div className="absolute inset-0 z-0">
          {/* Base gradient */}
          <div className="absolute inset-0 bg-gradient-to-r from-dark-900 via-dark-800 to-dark-900"></div>
          
          {/* Robot background - positioned on right */}
          <div 
            className="absolute inset-0 opacity-70"
            style={{
              backgroundImage: `url(${robotBg})`,
              backgroundPosition: 'right center',
              backgroundRepeat: 'no-repeat',
              backgroundSize: 'auto 100%',
              backgroundAttachment: 'fixed',
            }}
          ></div>

          {/* Neural network effect overlay */}
          <div className="absolute inset-0 opacity-20" style={{
            backgroundImage: `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1200 800'%3E%3Cline x1='0' y1='0' x2='1200' y2='800' stroke='%2306b6d4' stroke-width='0.5' opacity='0.3'/%3E%3Cline x1='1200' y1='0' x2='0' y2='800' stroke='%2306b6d4' stroke-width='0.5' opacity='0.3'/%3E%3C/svg%3E")`,
          }}></div>

          {/* Glow effects */}
          <div className="absolute top-1/4 right-0 w-96 h-96 bg-cyan-500 rounded-full mix-blend-screen filter blur-3xl opacity-20 animate-blob"></div>
          <div className="absolute bottom-1/4 right-1/4 w-80 h-80 bg-cyan-400 rounded-full mix-blend-screen filter blur-3xl opacity-10 animate-blob animation-delay-2000"></div>
        </div>

        {/* Content - Left aligned */}
        <div className="max-w-6xl mx-auto relative z-10 w-full">
          <div className="max-w-2xl">
            {/* Badge */}
            <motion.div
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="inline-block mb-8"
            >
              <span className="px-4 py-2 rounded-full border border-cyan-400/50 text-cyan-400 text-xs font-semibold bg-cyan-400/5 backdrop-blur-md">
                ✨ AI-POWERED VERIFICATION
              </span>
            </motion.div>

            {/* Main Heading */}
            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.1 }}
              className="text-5xl md:text-6xl lg:text-7xl font-black mb-6 leading-tight"
            >
              <span className="block text-white">Protect the <span className="bg-gradient-to-r from-cyan-400 to-cyan-300 bg-clip-text text-transparent">Truth</span></span>
              <span className="block text-white">Detect the <span className="bg-gradient-to-r from-cyan-400 to-cyan-300 bg-clip-text text-transparent">Fake</span></span>
            </motion.h1>

            {/* Subtitle */}
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="text-lg text-gray-300 mb-10"
            >
              Multi-modal deepfake detection 
            </motion.p>

            {/* CTA Buttons */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.3 }}
              className="flex flex-col sm:flex-row gap-6"
            >
              <Link
                to="/image"
                className="btn-cyan px-8 py-4 text-base font-bold rounded-lg text-center"
              >
                START DETECTION
              </Link>
              <Link
                to="/video"
                className="btn-outline px-8 py-4 text-base font-bold rounded-lg text-center"
              >
                ▶ VIDEO DETECTION
              </Link>
            </motion.div>
          </div>
        </div>
      </motion.section>

      {/* Features Section */}
      <section className="py-20 px-4 md:px-8 bg-dark-800/30">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            transition={{ duration: 0.6 }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-black mb-4">
              <span className="bg-gradient-to-r from-cyan-400 to-cyan-300 bg-clip-text text-transparent">
                Powerful Features
              </span>
            </h2>
            <p className="text-gray-400 text-lg">
              Enterprise-grade deepfake detection technology
            </p>
          </motion.div>

          <motion.div
            variants={containerVariants}
            initial="hidden"
            whileInView="visible"
            className="grid md:grid-cols-2 lg:grid-cols-4 gap-6"
          >
            {features.map((feature, index) => (
              <motion.div
                key={index}
                variants={itemVariants}
                className="group"
              >
                <div className="glass rounded-xl p-8 border border-cyan-500/20 hover:border-cyan-500/50 transition duration-300 h-full">
                  <div className="text-4xl mb-4">{feature.icon}</div>
                  <h3 className="text-lg font-bold mb-3 text-white">{feature.title}</h3>
                  <p className="text-gray-400 text-sm leading-relaxed">{feature.description}</p>
                </div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* CTA Section */}
      <motion.section
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        transition={{ duration: 0.8 }}
        className="py-20 px-4 md:px-8"
      >
        <div className="max-w-4xl mx-auto">
          <div className="glass rounded-2xl p-12 md:p-16 border border-cyan-500/20">
            <h2 className="text-3xl md:text-4xl font-black mb-4 text-white text-center">Ready to Detect Deepfakes?</h2>
            <p className="text-lg text-gray-300 text-center mb-10">
              Upload your media files and get instant AI-powered analysis results.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link 
                to="/image" 
                className="btn-cyan px-8 py-4 text-base font-bold rounded-lg"
              >
                Start Image Detection
              </Link>
              <Link 
                to="/video" 
                className="btn-outline px-8 py-4 text-base font-bold rounded-lg"
              >
                Try Video Detection
              </Link>
            </div>
          </div>
        </div>
      </motion.section>
    </div>
  )
}

export default Home
