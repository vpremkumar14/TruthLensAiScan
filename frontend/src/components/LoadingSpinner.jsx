import { motion } from 'framer-motion'

const LoadingSpinner = () => {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <motion.div
        animate={{ rotate: 360 }}
        transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
        className="w-12 h-12 border-4 border-dark-700 border-t-cyan-400 rounded-full"
      />
      <motion.p
        animate={{ opacity: [0.5, 1, 0.5] }}
        transition={{ duration: 1.5, repeat: Infinity }}
        className="mt-4 text-gray-400 font-medium"
      >
        Analyzing media...
      </motion.p>
    </div>
  )
}

export default LoadingSpinner
