import { motion } from 'framer-motion'

const ResultCard = ({
  prediction,
  confidence,
  explanation,
  imageUrl,
  explanationImage,
  type = 'image'
}) => {

  const isReal = prediction && prediction.toLowerCase().includes('real')

  const severityColor = isReal ? 'text-green-400' : 'text-red-500'
  const bgColor = isReal ? 'border-green-500/30' : 'border-red-500/30'

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className={`glass rounded-2xl p-5 md:p-8 border ${bgColor} mt-8`}
    >

      {/* ✅ RESPONSIVE GRID */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 md:gap-8">

        {/* Preview Section */}
        {imageUrl && (
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            className="flex flex-col items-center gap-4"
          >

            {/* Original */}
            {type === 'image' ? (
              <img
                src={imageUrl}
                alt="Original"
                className="rounded-xl w-full max-h-64 md:max-h-96 object-cover shadow-xl"
              />
            ) : (
              <video
                src={imageUrl}
                className="rounded-xl w-full max-h-64 md:max-h-96 object-cover shadow-xl"
                controls
              />
            )}

            {/* Heatmap */}
            {explanationImage && (
              <div className="w-full text-center">
                <p className="text-xs md:text-sm text-gray-400 mb-2">
                  AI Focus Areas
                </p>
                <img
                  src={`http://localhost:5000/${explanationImage}`}
                  alt="AI Explanation"
                  className="rounded-xl w-full max-h-64 md:max-h-96 object-cover shadow-lg border border-cyan-400/30"
                />
              </div>
            )}

          </motion.div>
        )}

        {/* Results Section */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.3 }}
          className="flex flex-col justify-center"
        >

          {/* Badge */}
          <div className="mb-4 md:mb-6">
            <span className={`inline-block px-3 md:px-4 py-2 rounded-full text-xs md:text-sm font-bold ${severityColor} border ${severityColor.replace('text', 'border')}`}>
              {isReal ? '✓ AUTHENTIC' : '✗ DETECTED AS FAKE'}
            </span>
          </div>

          {/* Confidence */}
          <div className="mb-6 md:mb-8">
            <h3 className="text-base md:text-lg font-semibold mb-2 md:mb-3 text-gray-200">
              Confidence Score
            </h3>

            <div className="bg-dark-800 rounded-lg p-3 md:p-4">
              <div className="flex justify-between mb-2">
                <span className="text-xl md:text-2xl font-bold text-cyan-400">
                  {(confidence * 100).toFixed(1)}%
                </span>
              </div>

              <div className="w-full bg-dark-700 rounded-full h-2 md:h-3 overflow-hidden">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${confidence * 100}%` }}
                  transition={{ duration: 1 }}
                  className={`h-full rounded-full ${
                    isReal
                      ? 'bg-gradient-to-r from-green-400 to-teal-500'
                      : 'bg-gradient-to-r from-red-400 to-orange-500'
                  }`}
                />
              </div>
            </div>
          </div>

          {/* Explanation */}
          <div>
            <h3 className="text-base md:text-lg font-semibold mb-2 md:mb-3 text-gray-200">
              Analysis
            </h3>

            <p className="text-sm md:text-base text-gray-400 bg-dark-800 rounded-lg p-3 md:p-4 leading-relaxed">
              {explanation || "Model analyzed facial patterns and inconsistencies to determine authenticity."}
            </p>
          </div>

        </motion.div>
      </div>
    </motion.div>
  )
}

export default ResultCard