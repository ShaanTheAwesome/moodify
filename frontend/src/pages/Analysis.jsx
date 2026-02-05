import { motion } from "framer-motion";

// Controls staggering of items
// Applies transition to everything
const container = {
  hidden:{},
  visible:{
    transition: {
      staggerChildren: 0.3, // Controls delay between items
    }
  }
};

// Controls item transition
const item = {
  hidden: {
    opacity: 0,
    y: 30,
  },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.6, ease: "ease-out"
    },
  }
};

export default function Analysis() {

  const transform = "transform transition-transform duration-150 ease-out hover:scale-115";

  return (
    <div>
      <motion.main className="flex flex-col items-center mt-40 h-screen bg-white space-y-8" variants={container} initial="hidden" animate="visible">
        <motion.h1 className='text-8xl font-bold' variants={item}>Analysis</motion.h1>
        <motion.p className='text-2xl text-[#8C8C8C]' variants={item}>Reviews you're spotify listening activity and judges your mood</motion.p>
        <motion.button className={`${transform} flex space-y-0 bg-[#00C407] text-white font-bold text-4xl px-20 py-10 rounded-full hover:scale-110 hover:cursor-pointer`} variants={item}>Analyse</motion.button>
      </motion.main>
    </div>
  )
}
