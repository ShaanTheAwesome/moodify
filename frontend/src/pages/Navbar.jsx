import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Navbar() {

  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const navigate = useNavigate();

  // Handles login request
  const handleLogin = () => {
    window.location.href = "http://127.0.0.1:8000/api/login"
  };

  // Handles logout request
  const handleLogout = () => {
    window.location.href = "http://127.0.0.1:8000/api/logout"
  };

  const handleGenres = () => {
    window.location.href = "http://127.0.0.1:8000/api/genres"
  }

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/auth/status", {
      credentials: "include"
    }).then(res => res.json())
      .then(data => {
        setIsLoggedIn(data.status);
      })
      .catch(() => {
        setIsLoggedIn(false)
      })
  }, [])

  const transform = "transform transition-transform duration-150 ease-out hover:scale-120";

  return (
    <div className="bg-black text-xl font-bold text-white flex px-14 py-8 justify-between items-center">
      <a href="/" className={`${transform} hover:text-green-400`}>
        Spotify Thing
      </a>


        {!isLoggedIn ? (
          <button className={`bg-[#00C407] hover:bg-green-600 text-white px-6 py-2 rounded-lg hover:cursor-pointer ${transform}`} onClick={handleLogin}>
            Login with Spotify
          </button>
        ) : (
          <div className={`flex items-center space-x-12`}>
            <a className={`hover:text-green-400 hover:cursor-pointer ${transform}`} onClick={handleGenres}>
              Genres
            </a>
            <a href="/dashboard" className={`hover:text-green-400 hover:cursor-pointer ${transform}`}>
              Dashboard
            </a>
            <button className={`bg-[#ff0000] hover:bg-red-700 text-white px-6 py-2 rounded-lg hover:cursor-pointer ${transform}`} onClick={handleLogout}>
              Logout
            </button>
          </div>
        )}
    </div>
  )
}