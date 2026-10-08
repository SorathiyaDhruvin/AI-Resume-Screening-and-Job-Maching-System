import { useState, useEffect } from 'react';
import { apiClient } from '../../api/apiClient';
import { Link } from 'react-router-dom';
import { Briefcase, Users, Plus, Star } from 'lucide-react';

export default function RecruiterDashboard() {
  const [jobs, setJobs] = useState<any[]>([]);

  useEffect(() => {
    fetchJobs();
  }, []);

  const fetchJobs = async () => {
    try {
      const res = await apiClient.get('/jobs');
      setJobs(res.data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="space-y-8">
      <header className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Recruiter Dashboard</h1>
          <p className="text-gray-500 mt-2">Manage jobs and review AI-matched candidates.</p>
        </div>
        <button className="bg-primary-600 text-white rounded-lg px-4 py-2.5 font-medium hover:bg-primary-700 transition-colors flex items-center shadow-sm">
          <Plus className="h-5 w-5 mr-2" />
          Create Job
        </button>
      </header>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 flex items-center space-x-4">
          <div className="bg-blue-100 p-4 rounded-xl text-blue-600">
            <Briefcase className="h-8 w-8" />
          </div>
          <div>
            <p className="text-gray-500 text-sm font-medium">Active Jobs</p>
            <h3 className="text-2xl font-bold text-gray-900">{jobs.length}</h3>
          </div>
        </div>
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 flex items-center space-x-4">
          <div className="bg-purple-100 p-4 rounded-xl text-purple-600">
            <Users className="h-8 w-8" />
          </div>
          <div>
            <p className="text-gray-500 text-sm font-medium">Total Candidates</p>
            <h3 className="text-2xl font-bold text-gray-900">-</h3>
          </div>
        </div>
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 flex items-center space-x-4">
          <div className="bg-green-100 p-4 rounded-xl text-green-600">
            <Star className="h-8 w-8" />
          </div>
          <div>
            <p className="text-gray-500 text-sm font-medium">Avg Match Score</p>
            <h3 className="text-2xl font-bold text-gray-900">-</h3>
          </div>
        </div>
      </div>

      {/* Active Jobs */}
      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
        <div className="px-6 py-5 border-b border-gray-100 flex justify-between items-center bg-gray-50/50">
          <h2 className="text-lg font-bold text-gray-800">Your Postings</h2>
        </div>
        <div className="divide-y divide-gray-100">
          {jobs.length === 0 ? (
            <div className="p-8 text-center text-gray-500">
              No jobs posted yet. Create your first job posting!
            </div>
          ) : (
            jobs.map((job) => (
              <div key={job.id} className="p-6 hover:bg-gray-50 transition-colors flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                  <h3 className="font-bold text-lg text-gray-900">{job.title}</h3>
                  <div className="text-sm text-gray-500 mt-1 flex items-center gap-3">
                    <span>{job.company}</span>
                    <span>•</span>
                    <span>{job.location}</span>
                    <span>•</span>
                    <span>{job.experience_min}-{job.experience_max} yrs</span>
                  </div>
                  <div className="mt-3 flex flex-wrap gap-2">
                    {job.skills?.slice(0, 5).map((s: any) => (
                      <span key={s.id} className="bg-gray-100 text-gray-700 text-xs px-2 py-1 rounded-md font-medium">
                        {s.skill.name}
                      </span>
                    ))}
                  </div>
                </div>
                <div className="flex gap-3 shrink-0">
                  <button className="bg-white border border-gray-200 text-gray-700 hover:bg-gray-50 hover:text-gray-900 px-4 py-2 rounded-lg text-sm font-medium transition-colors">
                    Edit
                  </button>
                  <Link to={`/recruiter/jobs/${job.id}/screening`} className="bg-primary-50 text-primary-700 hover:bg-primary-100 px-4 py-2 rounded-lg text-sm font-medium transition-colors">
                    Screen Candidates
                  </Link>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
