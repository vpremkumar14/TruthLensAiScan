import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'

const Navbar = () => {
  return (
    <motion.nav
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="glass shadow-2xl sticky top-0 z-50"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-20">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <div className="gradient-text-cyan font-black text-2xl tracking-tight">
              TRUTHLENSE AI SCAN
            </div>
          </Link>

          {/* Nav Links */}
          <div className="hidden md:flex space-x-10 items-center">
            <NavLink to="/" label="HOME" />
            <NavLink to="/image" label="IMAGE DETECTION" />
            <NavLink to="/video" label="VIDEO DETECTION" />
            <NavLink to="/about" label="ABOUT" />
          </div>

          {/* CTA Button */}
          <Link
            to="/image"
            className="btn-cyan px-6 py-2 text-sm font-bold tracking-wide hidden md:inline-block"
          >
            GET STARTED
          </Link>

          {/* Mobile Menu Button */}
          <div className="md:hidden flex items-center">
            <button className="p-2 rounded-lg hover:bg-dark-700 transition">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </motion.nav>
  )
}

const NavLink = ({ to, label }) => {
  return (
    <Link
      to={to || '#'}
      className="text-gray-300 hover:text-cyan-400 transition duration-300 relative group text-sm font-semibold tracking-wide"
    >
      {label}
      <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-gradient-to-r from-cyan-400 to-cyan-300 group-hover:w-full transition-all duration-300"></span>
    </Link>
  )
}

export default Navbar
