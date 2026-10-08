import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext.tsx';
import Navbar from './components/Navbar.tsx';
import Login from './pages/auth/Login.tsx';
import Register from './pages/auth/Register.tsx';
import CandidateDashboard from './pages/candidate/Dashboard.tsx';
import RecruiterDashboard from './pages/recruiter/Dashboard.tsx';
import JobScreening from './pages/recruiter/JobScreening.tsx';

const ProtectedRoute = ({ children, allowedRoles }: { children: React.ReactNode, allowedRoles?: string[] }) => {
  const { user, loading } = useAuth();
  
  if (loading) return <div className="flex items-center justify-center h-screen">Loading...</div>;
  if (!user) return <Navigate to="/login" />;
  if (allowedRoles && !allowedRoles.includes(user.role)) return <Navigate to="/" />;
  
  return <>{children}</>;
};

function AppRoutes() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50 flex flex-col">
        <Navbar />
        <main className="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 lg:p-8">
          <Routes>
            <Route path="/" element={<Navigate to="/login" />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            
            <Route path="/candidate/*" element={
              <ProtectedRoute allowedRoles={['candidate']}>
                <Routes>
                  <Route path="dashboard" element={<CandidateDashboard />} />
                </Routes>
              </ProtectedRoute>
            } />
            
            <Route path="/recruiter/*" element={
              <ProtectedRoute allowedRoles={['recruiter', 'admin']}>
                <Routes>
                  <Route path="dashboard" element={<RecruiterDashboard />} />
                  <Route path="jobs/:jobId/screening" element={<JobScreening />} />
                </Routes>
              </ProtectedRoute>
            } />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

function App() {
  return (
    <AuthProvider>
      <AppRoutes />
    </AuthProvider>
  );
}

export default App;
