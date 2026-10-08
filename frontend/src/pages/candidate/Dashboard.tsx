import { useState, useEffect } from 'react';
import { apiClient } from '../../api/apiClient';
import { useAuth } from '../../contexts/AuthContext';
import { Upload, FileText, Briefcase, CheckCircle, AlertCircle } from 'lucide-react';

export default function CandidateDashboard() {
  const { user } = useAuth();
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadMessage, setUploadMessage] = useState('');
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

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    setUploading(true);
    setUploadMessage('');
    const formData = new FormData();
    formData.append('file', file);

    try {
      await apiClient.post('/resumes/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setUploadMessage('Resume uploaded and processed successfully!');
      setFile(null);
    } catch (error: any) {
      setUploadMessage(error.response?.data?.detail || 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="space-y-8">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Welcome, {user?.name}</h1>
        <p className="text-gray-500 mt-2">Manage your profile and explore recommended jobs.</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        
        {/* Upload Card */}
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 col-span-1 md:col-span-1">
          <div className="flex items-center space-x-3 mb-4">
            <div className="bg-blue-100 p-2 rounded-lg">
              <Upload className="h-6 w-6 text-blue-600" />
            </div>
            <h2 className="text-lg font-bold text-gray-800">Upload Resume</h2>
          </div>
          
          <form onSubmit={handleUpload} className="space-y-4">
            <div className="border-2 border-dashed border-gray-300 rounded-xl p-6 text-center hover:border-primary-500 transition-colors">
              <input
                type="file"
                accept=".pdf,.docx"
                onChange={(e) => setFile(e.target.files?.[0] || null)}
                className="hidden"
                id="resume-upload"
              />
              <label htmlFor="resume-upload" className="cursor-pointer flex flex-col items-center">
                <FileText className="h-8 w-8 text-gray-400 mb-2" />
                <span className="text-sm font-medium text-gray-700">
                  {file ? file.name : 'Click to select PDF or DOCX'}
                </span>
                <span className="text-xs text-gray-500 mt-1">Max 5MB</span>
              </label>
            </div>
            
            <button
              type="submit"
              disabled={!file || uploading}
              className="w-full bg-primary-600 text-white rounded-lg px-4 py-2 font-medium hover:bg-primary-700 transition-all disabled:opacity-50"
            >
              {uploading ? 'Processing AI...' : 'Upload & Process'}
            </button>

            {uploadMessage && (
              <div className={`text-sm p-3 rounded-lg flex items-center ${uploadMessage.includes('successfully') ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'}`}>
                {uploadMessage.includes('successfully') ? <CheckCircle className="h-4 w-4 mr-2" /> : <AlertCircle className="h-4 w-4 mr-2" />}
                {uploadMessage}
              </div>
            )}
          </form>
        </div>

        {/* Jobs List */}
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 col-span-1 md:col-span-2">
          <div className="flex items-center space-x-3 mb-6">
            <div className="bg-purple-100 p-2 rounded-lg">
              <Briefcase className="h-6 w-6 text-purple-600" />
            </div>
            <h2 className="text-lg font-bold text-gray-800">Available Jobs</h2>
          </div>

          <div className="space-y-4">
            {jobs.length === 0 ? (
              <p className="text-gray-500 text-sm">No jobs available right now.</p>
            ) : (
              jobs.map((job) => (
                <div key={job.id} className="border border-gray-100 rounded-xl p-4 hover:shadow-md transition-shadow">
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="font-bold text-lg text-gray-900">{job.title}</h3>
                      <p className="text-gray-600 text-sm">{job.company} • {job.location}</p>
                    </div>
                    <span className="bg-gray-100 text-gray-800 text-xs px-2 py-1 rounded-full font-medium">
                      {job.experience_min}-{job.experience_max} yrs
                    </span>
                  </div>
                  <div className="mt-3 flex flex-wrap gap-2">
                    {job.skills?.slice(0, 4).map((s: any) => (
                      <span key={s.id} className="bg-primary-50 text-primary-700 text-xs px-2 py-1 rounded-md font-medium">
                        {s.skill.name}
                      </span>
                    ))}
                    {job.skills?.length > 4 && (
                      <span className="text-xs text-gray-500 py-1">+{job.skills.length - 4} more</span>
                    )}
                  </div>
                  <div className="mt-4">
                    <button className="text-primary-600 text-sm font-medium hover:text-primary-800">
                      View Details & Match →
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

      </div>
    </div>
  );
}
