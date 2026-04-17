import { motion } from 'framer-motion'

const FileUpload = ({ onFileSelect, accept, loading }) => {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.4 }}
      className="w-full"
    >
      <div className="relative">
        <input
          type="file"
          accept={accept}
          onChange={(e) => onFileSelect(e.target.files[0])}
          className="hidden"
          id="file-input"
          disabled={loading}
        />
        <label
          htmlFor="file-input"
          className="flex flex-col items-center justify-center w-full h-64 border-2 border-dashed border-primary-500 rounded-2xl cursor-pointer glass-dark hover:border-cyan-400 transition duration-300 group"
        >
          <div className="flex flex-col items-center justify-center pt-5 pb-6">
            <svg className="w-12 h-12 text-cyan-400 group-hover:scale-110 transition duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
            <p className="mt-2 text-sm text-gray-400">
              <span className="font-semibold text-cyan-400">Click to upload</span> or drag your file
            </p>
            <p className="text-xs text-gray-500 mt-1">PNG, JPG, GIF up to 100MB</p>
          </div>
        </label>
      </div>
    </motion.div>
  )
}

export default FileUpload
