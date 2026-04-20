import { motion } from 'framer-motion'

const About = () => {
  const technologies = [
    { name: 'ResNet50', description: 'Deep CNN for image classification' },
    { name: 'PyTorch', description: 'Deep learning framework' },
    { name: 'OpenCV', description: 'Video processing and frame extraction' },
    { name: 'Flask', description: 'Backend API server' },
    { name: 'React', description: 'Frontend UI framework' },
    { name: 'Tailwind CSS', description: 'Modern styling' },
  ]

  const features = [
    {
      title: 'Advanced CNN Architecture',
      description: 'Transfer learning with ResNet50 pre-trained on ImageNet for superior accuracy in detecting AI-generated and deepfake media.',
    },
    {
      title: 'Multi-Modal Analysis',
      description: 'Analyzes both individual images and extracts key frames from videos for comprehensive deepfake detection.',
    },
    {
      title: 'Real-Time Processing',
      description: 'Optimized inference pipeline for quick results without compromising accuracy.',
    },
    {
      title: 'Confidence Scoring',
      description: 'Provides detailed confidence percentages to help users understand the certainty of detection results.',
    },
    {
      title: 'Explainable AI',
      description: 'Offers explanations for detection results, helping users understand why content was flagged.',
    },
    {
      title: 'Professional UI',
      description: 'Modern glassmorphic design with dark theme, smooth animations, and responsive layout.',
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
    <div className="min-h-screen py-12 px-4 md:px-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="text-center mb-16"
        >
          <h1 className="text-5xl md:text-6xl font-bold mb-6">
            <span className="gradient-text">About TruthLens</span>
          </h1>
          <p className="text-xl text-gray-400 max-w-3xl mx-auto">
            TruthLens AI Scan is a cutting-edge application designed to detect deepfakes using advanced deep learning techniques.
          </p>
        </motion.div>

        {/* Mission Section */}
        <motion.section
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          transition={{ duration: 0.8 }}
          className="glass rounded-2xl p-12 mb-16"
        >
          <h2 className="text-3xl font-bold mb-4 gradient-text">Our Mission</h2>
          <p className="text-gray-300 text-lg leading-relaxed">
            In an era of sophisticated digital manipulation, distinguishing authentic content from AI-generated or deepfaked media has become increasingly challenging. TruthLens AI Scan aims to empower users with state-of-the-art detection technology, helping them protect themselves from misinformation and digital fraud. Our mission is to make deepfake detection accessible, accurate, and easy to understand for everyone.
          </p>
        </motion.section>

        {/* How It Works */}
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          transition={{ duration: 0.8 }}
          className="mb-16"
        >
          <h2 className="text-3xl font-bold mb-8 gradient-text">How It Works</h2>
          <div className="grid md:grid-cols-3 gap-6">
            {[
              {
                step: '1',
                title: 'Upload Media',
                description: 'Select and upload an image or video for analysis',
              },
              {
                step: '2',
                title: 'AI Analysis',
                description: 'Our CNN model analyzes the media for AI artifacts and inconsistencies',
              },
              {
                step: '3',
                title: 'Results',
                description: 'Get instant feedback with confidence score and detailed explanation',
              },
            ].map((item, index) => (
              <motion.div
                key={index}
                variants={itemVariants}
                initial="hidden"
                whileInView="visible"
                className="glass rounded-xl p-8 text-center"
              >
                <div className="text-4xl font-bold text-cyan-400 mb-4">{item.step}</div>
                <h3 className="text-xl font-semibold mb-2">{item.title}</h3>
                <p className="text-gray-400">{item.description}</p>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Features */}
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          transition={{ duration: 0.8 }}
          className="mb-16"
        >
          <h2 className="text-3xl font-bold mb-8 gradient-text">Key Features</h2>
          <motion.div
            variants={containerVariants}
            initial="hidden"
            whileInView="visible"
            className="grid md:grid-cols-2 gap-6"
          >
            {features.map((feature, index) => (
              <motion.div
                key={index}
                variants={itemVariants}
                className="glass rounded-xl p-6"
              >
                <h3 className="text-lg font-semibold mb-3 text-cyan-400">✓ {feature.title}</h3>
                <p className="text-gray-400">{feature.description}</p>
              </motion.div>
            ))}
          </motion.div>
        </motion.div>

        {/* Technology Stack */}
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          transition={{ duration: 0.8 }}
          className="mb-16"
        >
          <h2 className="text-3xl font-bold mb-8 gradient-text">Technology Stack</h2>
          <motion.div
            variants={containerVariants}
            initial="hidden"
            whileInView="visible"
            className="grid md:grid-cols-2 lg:grid-cols-3 gap-6"
          >
            {technologies.map((tech, index) => (
              <motion.div
                key={index}
                variants={itemVariants}
                className="glass rounded-lg p-5 border border-primary-500/20 hover:border-cyan-400/50 transition"
              >
                <h3 className="font-semibold text-cyan-400 mb-2">{tech.name}</h3>
                <p className="text-gray-400 text-sm">{tech.description}</p>
              </motion.div>
            ))}
          </motion.div>
        </motion.div>

        {/* Technical Details */}
        <motion.section
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          transition={{ duration: 0.8 }}
          className="glass rounded-2xl p-12 mb-16"
        >
          <h2 className="text-2xl font-bold mb-6 gradient-text">Technical Approach</h2>
          <div className="space-y-4 text-gray-300">
            <p>
              <span className="text-cyan-400 font-semibold">Model Architecture:</span> We use ResNet50, a deep convolutional neural network with 50 layers, pre-trained on ImageNet. This transfer learning approach allows us to leverage knowledge from millions of real images to detect subtle artifacts introduced by generative AI models.
            </p>
            <p>
              <span className="text-cyan-400 font-semibold">Input Preprocessing:</span> Images are normalized to 224x224 pixels with standard ImageNet mean and standard deviation. Videos are analyzed by extracting key frames at regular intervals (every 5 frames) and processing each frame independently.
            </p>
            <p>
              <span className="text-cyan-400 font-semibold">Output:</span> The model provides a binary classification (Real/Fake) along with a confidence score (0-1) indicating the model's certainty about the prediction. Confidence scores above 0.95 are considered high confidence results.
            </p>
          </div>
        </motion.section>

        {/* Call to Action */}
        <motion.section
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          transition={{ duration: 0.8 }}
          className="text-center"
        >
          <h2 className="text-3xl font-bold mb-4">Ready to Detect?</h2>
          <p className="text-gray-400 mb-8">
            Start analyzing images and videos for deepfakes content today.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a href="/image" className="btn-primary">
              Scan Image
            </a>
            <a href="/video" className="px-6 py-3 rounded-lg font-semibold border border-cyan-400 text-cyan-400 hover:bg-cyan-400/10 transition">
              Scan Video
            </a>
          </div>
        </motion.section>
      </div>
    </div>
  )
}


export default About
