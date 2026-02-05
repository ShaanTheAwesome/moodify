import { useState, useEffect } from "react";

export default function Dashboard() {
  const [profile, setProfile] = useState(null);
  const [topArtists, setTopArtists] = useState([]);
  const [topTracks, setTopTracks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [dots, setDots] = useState("");

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/profile", {
      credentials: "include" // IMPORTANT for auth
    })
      .then(res => {
        if (!res.ok) {
          throw new Error("Not authenticated");
        }
        return res.json();
      })
      .then(data => {
        setProfile(data.profile);
        setTopArtists(data.top_artists.items);
        setTopTracks(data.top_tracks.items);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  useEffect(() => {
    if (!loading) return;

    const interval = setInterval(() => {
      setDots(prev => (prev.length === 3 ? "" : prev + "."));
    }, 500);

    return () => clearInterval(interval);
  }, [loading]);

  if (loading) {
    return <p className="flex flex-col items-center mt-40 h-screen bg-white space-y-8 text-center mt-20 text-8xl font-bold">Loading{dots}</p>;
  }

  if (error) {
    return <p className="text-center mt-20 text-red-500">{error}</p>;
  }

  return (
    <div className="p-10">
      {/* Profile */}
      <div className="flex items-center space-x-6">
        {profile.images?.[0] && (
          <img
            src={profile.images[0].url}
            alt="Profile"
            className="w-24 h-24 rounded-full"
          />
        )}
        <div>
          <h1 className="text-3xl font-bold">{profile.display_name}</h1>
          <p className="text-gray-500">
            Followers: {profile.followers.total}
          </p>
        </div>
      </div>

      {/* Top Artists */}
      <section className="mt-12">
        <h2 className="text-2xl font-bold mb-4">Top Artists</h2>
        <ul className="grid grid-cols-2 md:grid-cols-5 gap-4">
          {topArtists.map(artist => (
            <li key={artist.id} className="text-center">
              {artist.images?.[0] && (
                <img
                  src={artist.images[0].url}
                  alt={artist.name}
                  className="rounded-lg"
                />
              )}
              <p className="mt-2 font-semibold">{artist.name}</p>
            </li>
          ))}
        </ul>
      </section>

      {/* Top Tracks */}
      <section className="mt-12">
        <h2 className="text-2xl font-bold mb-4">Top Tracks</h2>
        <ul className="space-y-2">
          {topTracks.map(track => (
            <li key={track.id}>
              🎵 {track.name} — {track.artists[0].name}
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}
