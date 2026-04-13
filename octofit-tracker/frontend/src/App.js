import { NavLink, Route, Routes } from 'react-router-dom';
import './App.css';
import Activities from './components/Activities';
import Leaderboard from './components/Leaderboard';
import Teams from './components/Teams';
import Users from './components/Users';
import Workouts from './components/Workouts';

function App() {
  return (
    <div className="app-shell py-4">
      <main className="container">
        <div className="card shadow-sm border-0 mb-4">
          <div className="card-body d-flex align-items-center gap-3 flex-wrap">
            <img
              src={`${process.env.PUBLIC_URL}/octofitapp-small.png`}
              alt="OctoFit logo"
              className="octofit-logo"
            />
            <div>
              <h1 className="display-6 fw-bold mb-1">OctoFit Tracker</h1>
              <p className="text-secondary mb-0">Track users, teams, workouts, activities, and ranking in one place.</p>
            </div>
          </div>
        </div>

        <nav className="navbar navbar-expand-lg octofit-nav rounded-3 px-3 mb-4">
          <span className="navbar-brand fw-semibold text-white">Navigation</span>
          <div className="navbar-nav nav-pills d-flex flex-row gap-2 flex-wrap">
            <NavLink className="nav-link text-white" to="/activities">
              Activities
            </NavLink>
            <NavLink className="nav-link text-white" to="/leaderboard">
              Leaderboard
            </NavLink>
            <NavLink className="nav-link text-white" to="/teams">
              Teams
            </NavLink>
            <NavLink className="nav-link text-white" to="/users">
              Users
            </NavLink>
            <NavLink className="nav-link text-white" to="/workouts">
              Workouts
            </NavLink>
          </div>
        </nav>

        <Routes>
          <Route path="/" element={<Activities />} />
          <Route path="/activities" element={<Activities />} />
          <Route path="/leaderboard" element={<Leaderboard />} />
          <Route path="/teams" element={<Teams />} />
          <Route path="/users" element={<Users />} />
          <Route path="/workouts" element={<Workouts />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
